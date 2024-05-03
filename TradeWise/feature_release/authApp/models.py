from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)


#
class roles(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Users Profile Roles'


class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class HistoryBase(models.Model):
    updated = models.DateTimeField(auto_now_add=True, null=True)
    fields = models.CharField(max_length=200, blank=True, null=True)
    comments = models.TextField()

    class Meta:
        abstract = True


#
class userRoles(models.Model):
    profile_owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_ownerUR')
    profile_username = models.CharField(max_length=256, null=True, blank=True)
    referred_by_id = models.CharField(max_length=256, null=True, blank=True)
    referred_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    platform = models.CharField(max_length=256, null=True, blank=True)
    profile_roles = models.ManyToManyField(roles)

    def __str__(self):
        return f'Profile Owner: {self.profile_owner}, Profile Username: {self.profile_username}'

    class Meta:
        verbose_name_plural = 'Users, Username and Profiles Roles'


# def save(self):
# 	for role in self.profile_roles.all():
#		add logic to create profiles as soon as multiple profile roles are selected


class loginBannerObjects(models.Model):
    titleOne = models.CharField(max_length=1000, null=True, blank=True)
    contentOne = models.CharField(max_length=1000, null=True, blank=True)
    titleOneImg = models.ImageField(upload_to='login/images', null=True, blank=True)
    titleOneImg_AltTag = models.CharField(max_length=100, null=True, blank=True)

    titleTwo = models.CharField(max_length=1000, null=True, blank=True)
    contentTwo = models.CharField(max_length=1000, null=True, blank=True)
    titleTwoImg = models.ImageField(upload_to='login/images', null=True, blank=True)
    titleTwoImg_AltTag = models.CharField(max_length=100, null=True, blank=True)

    titleThree = models.CharField(max_length=1000, null=True, blank=True)
    contentThree = models.CharField(max_length=1000, null=True, blank=True)
    titleThreeImg = models.ImageField(upload_to='login/images', null=True, blank=True)
    titleThreeImg_AltTag = models.CharField(max_length=100, null=True, blank=True)

    titleFour = models.CharField(max_length=1000, null=True, blank=True)
    contentFour = models.CharField(max_length=1000, null=True, blank=True)
    titleFourImg = models.ImageField(upload_to='login/images', null=True, blank=True)
    titleFourImg_AltTag = models.CharField(max_length=100, null=True, blank=True)

    titleFive = models.CharField(max_length=1000, null=True, blank=True)
    contentFive = models.CharField(max_length=1000, null=True, blank=True)
    titleFiveImg = models.ImageField(upload_to='login/images', null=True, blank=True)
    titleFiveImg_AltTag = models.CharField(max_length=100, null=True, blank=True)

    titleSix = models.CharField(max_length=1000, null=True, blank=True)
    contentSix = models.CharField(max_length=1000, null=True, blank=True)
    titleSixImg = models.ImageField(upload_to='login/images', null=True, blank=True)
    titleSixImg_AltTag = models.CharField(max_length=100, null=True, blank=True)

    bannerImg = models.ImageField(upload_to='login/images', null=True, blank=True)
    bannerImg_AltTag = models.CharField(max_length=100, null=True, blank=True)

    videoID = models.CharField(max_length=1000, null=True, blank=True)
    videoTitle = models.CharField(max_length=1000, null=True, blank=True)
    videoContent = models.CharField(max_length=1000, null=True, blank=True)
    relatedTo = models.OneToOneField(roles, on_delete=models.CASCADE, related_name='loginBannerOb')
    # relatedProfile = models.ForeignKey(roles, on_delete=models.CASCADE, unique=True)
    author = models.CharField(max_length=1000, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return f'Role: {self.relatedTo.name} with title: {self.titleOne}' or '--name not provided--'

    class Meta:
        verbose_name_plural = 'login banner objects'


class UserDeviceTokens(models.Model):
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    user_id = models.BigIntegerField(db_index=True, null=False)
    platform = models.CharField(max_length=10, default='NA')
    token = models.TextField()
    device_id = models.CharField(max_length=300, null=True, blank=True)

    @classmethod
    def clean_tokens(cls, user_id):
        cls.objects.filter(user_id=user_id).delete()

    @classmethod
    def upsert_token(cls, user_id, platform, token, device_id=None):
        obj = cls.objects.filter(user_id=user_id, platform=platform).last()
        if obj and obj.token != token:
            obj.token = token
            obj.save(update_fields=['token', 'updated'])
        elif not obj:
            cls(user_id=user_id, platform=platform, device_id=device_id, token=token).save()

    @classmethod
    def get_user_device_token(cls, user_id, platform=None):
        kwargs = {}
        if platform:
            kwargs = {'platform': platform}
        return cls.objects.filter(user_id=user_id, **kwargs).values('token').order_by('-updated').first()


class UserLogoutHistory(models.Model):
    user_id = models.BigIntegerField(db_index=True, null=False)
    platform = models.CharField(max_length=10, default='NA')
    created_at = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField()

    @classmethod
    def get_last_logout_time(cls, user_id):
        obj = cls.objects.filter(user_id=user_id).last()
        if obj:
            return obj.logout_time.timestamp().__int__()
        else:
            return None

    @classmethod
    def logout(cls, user_id, platform, all_mobile_devices=False):
        if all_mobile_devices:
            cls.logout(user_id, 'ios', False)
            cls.logout(user_id, 'android', False)
        else:
            platform = platform.lower()
            logout_time = datetime.datetime.now()
            cls.objects.create(user_id=user_id, platform=platform, logout_time=logout_time)


class NotificationTemplates(models.Model):
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    body = models.TextField()
    title = models.TextField()
    template_type = models.CharField(max_length=100)
    template_name = models.CharField(max_length=100, unique=True, null=False, blank=False)

    @classmethod
    def fetch_obj(cls, template_name):
        return cls.objects.filter(template_name=template_name).last()


class UserAdvisorHistory(HistoryBase):
    user_id = models.BigIntegerField(db_index=True, null=False)
    advisor_id = models.BigIntegerField(null=False)
    user_type = models.CharField(max_length=100, null=True, default='Registeration')
    identifier = models.CharField(max_length=50, db_index=True, null=True)


class UserAdvisors(BaseModel):
    user_id = models.BigIntegerField(db_index=True, null=False)
    identifier = models.CharField(max_length=50, db_index=True, null=True)
    user_type = models.CharField(max_length=100, null=True, default='Registeration')
    assigned_advisor_id = models.BigIntegerField(null=True, db_index=True)
    updated_by = models.BigIntegerField(null=True)
    comments = models.TextField()
