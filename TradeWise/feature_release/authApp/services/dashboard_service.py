from django.db.models import Q
from django.core.cache import cache
from employeeApp.models import employeePersonalDetails
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from planifyMain.paginators import StandardResultsSetPagination
from authApp.models import userRoles, UserAdvisors, UserAdvisorHistory, roles
from investorApp.services.kyc.constants import UserRoleTypes
from . user_service import UserService


class DashboardService:

    def __init__(self, user):
        self.user = user

    @staticmethod
    def fetch_employee_users():
        key = 'employees_user_data'
        data = cache.get(key)
        if not data:
            employee_users = employeePersonalDetails.objects.all()
            data = []
            for emp in employee_users:
                if emp.profileOwner.email and emp.profileOwner.is_active and (
                        'planify.in' in emp.profileOwner.email or 'planify.in' in emp.profileOwner.username):
                    data.append({
                        "id": emp.profileOwner.id,
                        "firstname": emp.firstName,
                        "lastname": emp.lastName,
                        "email": emp.profileOwner.email or emp.profileOwner.username
                    })
            cache.set(key, data, 120)
        return data

    def fetch_comment_logs(self, user_ids):
        user_comment_map = {}
        comments = UserAdvisorHistory.objects.filter(user_id__in=user_ids).values('updated', 'comments',
                                                                                  'advisor_id',
                                                                                  'user_id').order_by('-id')
        for comment in comments:
            if not user_comment_map.get(comment['user_id']):
                user_comment_map[comment['user_id']] = []
            user_comment_map[comment['user_id']].append(
                {
                    'advisor_id': comment['advisor_id'],
                    'comment': comment['comments'].split('comments=')[-1],
                    'created': str(comment['updated'])
                }
            )
        return user_comment_map

    def fetch_users_data(self, filters=None, limit=5000, fetch_type='advisor', page=1, page_size=30):
        users_data = []
        user_advisors = None
        user_advisor_mp = {}
        employee_users = []
        user_ids = []
        if filters:
            if filters.get('q'):
                kw = Q(username=filters.get('q')) | Q(email=filters.get('q'))
            elif filters.get('employee_user_id'):
                user_advisors = UserAdvisors.objects.filter(assigned_advisor_id=filters.get('employee_user_id')).values(
                    'user_id', 'assigned_advisor_id', 'comments')
                for user in user_advisors:
                    user_ids.append(user['user_id'])
                kw = Q(id__in=user_ids)
            else:
                kw = Q(profile_ownerUR__name=filters.get('user_role', 'INVESTOR'))
            users = User.objects.select_related('profile_ownerUR').filter(kw).order_by('-id')[:limit]
        else:
            users = User.objects.select_related('profile_ownerUR').all().order_by('-id')
            if limit:
                users = users[: limit]
        paginator = Paginator(users, page_size)
        users = paginator.get_page(page).object_list
        if not user_ids:
            for user in users:
                user_ids.append(user.id)
        user_comment_map = {}
        if fetch_type == 'advisor':
            user_comment_map = self.fetch_comment_logs(user_ids)
            employee_users = self.fetch_employee_users()
            if not user_advisors:
                user_advisors = UserAdvisors.objects.filter(user_id__in=user_ids).values('user_id',
                                                                                         'assigned_advisor_id',
                                                                                         'comments')
            for advisor_data in user_advisors:
                user_advisor_mp[advisor_data['user_id']] = {'advisor': advisor_data['assigned_advisor_id'],
                                                            'comments': advisor_data['comments']}
        all_roles = roles.objects.all()
        all_roles_list = []
        for role in all_roles:
            all_roles_list.append(role.name)
        for user in users:
            source = ''
            if hasattr(user, 'profile_ownerUR'):
                user_roles = list(user.profile_ownerUR.profile_roles.values_list('name', flat=True))
                try:
                    source = user.profile_ownerUR.platform
                except:
                    pass
            else:
                user_roles = []
            user_data = {'user_id': user.id, 'email': user.email,
                         'user_name': user.username if user.username != user.email else '', 'user_roles': user_roles,
                         'date_joined': str(user.date_joined),
                         'name': f'{user.first_name or ""} {user.last_name or ""}', 'source':source}
            if user_advisor_mp.get(user.id):
                user_data.update(user_advisor_mp.get(user.id))
                if user_data.get('advisor_id', '') is None:
                    user_data['advisor_id'] = -1
            if user_comment_map.get(user.id):
                user_data['comment_log'] = user_comment_map.get(user.id)
                if not user_data.get('comments') and user_data['comment_log']:
                    user_data['comments'] = user_data['comment_log'][0]
            users_data.append(user_data)
        data = {'all_roles': all_roles_list, 'users': users_data, 'employee_users': employee_users,
                'num_pages': paginator.num_pages, 'count': paginator.count, 'page': page}
        return data

    def _get_user_roles(self, user):
        user_roles = list(
            userRoles.objects.filter(profile_owner=user).values_list('profile_roles__name', flat=True))
        return user_roles

    def update_user_advisor_data(self, data):
        old_comments = ''
        fields_updated = []
        if data and (data.get('user_id') or data.get('identifier')):
            if data.get('user_id'):
                obj, _ = UserAdvisors.objects.get_or_create(user_id=data.get('user_id'))
            else:
                obj, _ = UserAdvisors.objects.get_or_create(identifier=data.get('identifier'))
            obj.updated_by = self.user.id
            if data.get('employee_user_id') and int(data.get('employee_user_id')):
                emp_data = self.fetch_employee_users()
                validated = False
                for emp in emp_data:
                    if int(data['employee_user_id']) == int(emp['id']):
                        validated = True
                        break
                if validated:
                    if obj.assigned_advisor_id != data['employee_user_id']:
                        if obj.assigned_advisor_id:
                            old_comments = f'assigned_advisor_id={obj.assigned_advisor_id}'
                        obj.assigned_advisor_id = data['employee_user_id']
                        fields_updated.append('assigned_advisor_id')
                else:
                    return {'status': False, 'message': 'invalid employee'}
            if data.get('comments'):
                if obj.comments:
                    fields_updated.append('comments')
                    old_comments = old_comments + ';comments=' + (obj.comments or '')
                obj.comments = data.get('comments')
                if data.get('user_id'):
                    UserAdvisorHistory(user_id=data.get('user_id'), advisor_id=self.user.id,
                                   comments=old_comments, fields=str(fields_updated)).save()
                else:
                    UserAdvisorHistory(user_type=data.get('user_type'), identifier=data.get('identifier'), advisor_id=data.get('employee_user_id'),
                                       comments=old_comments, fields=str(fields_updated)).save()
            obj.save()
            return {'status': True, 'message': 'success'}
        return {'status': False, 'message': 'invalid user', 'data': dict(data)}


    def update_user_role_new(self, data):
        try:
            all_roles = roles.objects.all()
            all_roles_list = []
            for role in all_roles:
                all_roles_list.append(role.name)
            tempID = data.get("user_id")
            tempCurrentRole= []
            removedRoles= []
            try:
                userInst = User.objects.get(pk=tempID)
                roleOfUser, created = userRoles.objects.get_or_create(profile_owner=userInst)
                if created:
                    roleOfUser.save()
                else:
                    for item in roleOfUser.profile_roles.all():
                        tempCurrentRole.append(item.name)
            except:
                pass
            tempNewRole = data.get("new_role")
            if tempNewRole ==  None:
                return {"msg": "Got None in New Role!", "status": False}   
            try:
                userInst = userRoles.objects.get(profile_owner__id = tempID)
                for role in all_roles_list:
                    if role in tempCurrentRole and role not in tempNewRole:
                        currentRoleForUser = roles.objects.get(name = role)
                        try:
                            userInst.profile_roles.remove(currentRoleForUser)
                            tempCurrentRole.remove(role)
                        except:
                            return {"msg": "error while removing or saving the new Role", "status": False}      
                for role in all_roles_list:
                    if role in tempNewRole and role not in tempCurrentRole:
                        if UserService().validate_role(None, role, tempCurrentRole) == 2:
                            if removedRoles:
                                return {"msg": f"User does not have {role} as a family member and these roles {removedRoles} are removed. Please select the correct family role and try again !", "status": False}
                            return {"msg": f"User does not have {role} as a family member. Please select the correct family role !", "status": False}
                        tempCurrentRole.append(role)
                        newRoleForUser = roles.objects.get(name = role)
                        try:
                            userInst.profile_roles.add(newRoleForUser)
                        except:
                            return {"msg": "error while adding or saving the new Role", "status": False}
                userInst.save()
                return {"msg": "Role has been updated successfully!", "status": True}
            except:
                return {"msg": "error while handling the new_role input", "status": False}
        except:
            return {"msg": "got an exception while submitting the request !!", "status": False}