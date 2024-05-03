from cartApp.models import UserCart, CartItems
from websiteApp.models import buyPreIPOStockList
from django.core.cache import cache
from stockApp.models import stockBasicDetail, stockEssentials
from django.db import transaction
import uuid
import decimal


class CartService:

    def __init__(self, user):
        self.user_id = user.id
        self.user = user

    @staticmethod
    def is_valid_uuid(val):
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False

    def _fetch_item_data(self, item):
        stock_val = self._fetch_stock_price(item.pre_ipo_stock)
        status = item.status
        stock = item.pre_ipo_stock.stockName
        if not self._can_purchase_stock(stock):
            status = 'inactive'
        return {
            "item_uid": item.uid,
            "quantity": item.quantity,
            "pre_ipo_id": item.pre_ipo_stock.id,
            "stock": {
                'id': stock.id,
                'name': stock.stockName,
                # 'logo': item.pre_ipo_stock.stockName.logo,
                'slug': stock.slug,
                'ticker': stock.ticker,
                "value": stock_val,
                'logo': stock.logo.url if stock.logo else '',
            },
            'status': status,
            "value": stock_val * decimal.Decimal(item.quantity)
        }

    def get_cart_details(self):
        user_cart_obj = UserCart.fetch_user_cart(self.user_id)
        cart_id = user_cart_obj.id
        user_cart_items = CartItems.fetch_cart_items(cart_id)
        total_cart_val = 0
        cart_items = []
        for item in user_cart_items:
            if item.quantity > 0:
                stock_val = self._fetch_stock_price(item.pre_ipo_stock)
                if stock_val:
                    total_cart_val += stock_val * decimal.Decimal(item.quantity)
                    cart_items.append(
                        self._fetch_item_data(item)
                    )
        misc_charges_data = self._fetch_cart_misc_charges()
        misc_charges = misc_charges_data.get('total_value', 0)
        benefits_data = self._fetch_user_beneficts()
        benefits = benefits_data.get('total_value', 0)
        total_price = total_cart_val + misc_charges - benefits
        data = {
            'misc_charges': misc_charges_data,
            'benefits': benefits_data,
            'cart_items': cart_items,
            'cart_value': total_cart_val,
            'total_price': total_price,
            'cart_uid': user_cart_obj.uid
        }
        return {'status': True, "data": data}

    def _fetch_cart_misc_charges(self):
        misc_charges = 0
        return {
            "total_value": misc_charges,
            "charges": []
        }

    def _fetch_user_beneficts(self):
        benefits = 0
        benefits_data = {
            "total_value": benefits,
            "benefits": []
        }
        return benefits_data

    def update_item(self, item_uid: str, data: dict):
        resp = {
            'status': False, 'message': 'Invalid data', 'data': {}
        }
        if not self.is_valid_uuid(item_uid):
            return resp
        with transaction.atomic():
            user_cart_obj = UserCart.fetch_user_cart(self.user_id)
            cart_id = user_cart_obj.id

            cart_item = CartItems.fetch_obj(item_uid, cart_id)
            if cart_item:
                cart_item.quantity = data.get('quantity', 0)
                pre_ipo_stock = cart_item.pre_ipo_stock
                if not self._validate_stock_quantity(pre_ipo_stock, cart_item.quantity):
                    resp["message"] = 'Limit exceeded'
                    return resp
                if cart_item.quantity == 0:
                    cart_item.delete()
                else:
                    cart_item.save()
                    # resp["data"] = self._fetch_item_data(cart_item)
                resp['status'] = True
                resp["message"] = "Success"

        return resp

    def add_item(self, data):
        resp = {
            'status': False, 'message': 'Invalid data'
        }
        if not data.get('quantity') and not data.get('amount'):
            return resp
        user_cart_obj = UserCart.fetch_user_cart(self.user_id)
        cart_id = user_cart_obj.id
        if CartItems.fetch_item_count(cart_id) >= 10:
            resp["message"] = "Can only add upto 10 stocks only in the cart"
            return resp
        pk = data.get('stock_id')
        stock = stockBasicDetail.objects.filter(id=pk).last()
        if not stock:
            resp["message"] = 'Invalid Stock'
            return resp
        if not self._can_purchase_stock(stock):
            resp["message"] = 'Can not purchase the stock'
            return resp
        pre_ipo_stock = buyPreIPOStockList.objects.filter(stockName=stock).last()
        if not pre_ipo_stock:
            resp["message"] = 'Stock is not listed'
            return resp
        quantity = data.get('quantity')
        if not quantity:
            current_price = self._fetch_stock_price(pre_ipo_stock)
            if not current_price:
                resp["message"] = 'Stock is not listed'
                return resp
            quantity = data.get('amount') / current_price
        if not self._validate_stock_quantity(pre_ipo_stock, quantity):
            resp["message"] = 'Limit exceeded'
            return resp
        with transaction.atomic():
            cart_item = CartItems.fetch_stock_item(cart_id, pre_ipo_stock.id)
            if not self._validate_stock_quantity(pre_ipo_stock, cart_item.quantity + quantity):
                resp["message"] = 'Limit exceeded'
                return resp
            cart_item.stock = stock
            cart_item.quantity += quantity
            cart_item.save()
            resp["data"] = self._fetch_item_data(cart_item)
        resp["status"] = True
        resp["message"] = "Success"
        return resp

    def _is_item_eligible(self):
        pass

    def _fetch_stock_price(self, pre_ipo_stock):
        return pre_ipo_stock.investorPrice

    def _can_purchase_stock(self, stock: stockBasicDetail.objects, allow_cache=True):
        if stock.isStatusComp == 'Completed':
            return False
        category = ''
        cached_category_key = f'{stock.id}_stock_cat'
        cached_cat = cache.get(cached_category_key)
        if not cached_cat or not allow_cache:
            stock_cat_data = stockEssentials.objects.filter(stockProfileName=stock).values('category__name').last()
            if stock_cat_data and stock_cat_data.get('category__name'):
                category = stock_cat_data.get('category__name')
                cache.set(cached_category_key, category, 60)
        else:
            category = cached_cat
        if category and category.lower() == 'listed':
            return False
        return True

    def _validate_stock_quantity(self, pre_ipo_stock, quantity):
        return True

    def delete_item(self, item_uid: str):
        resp = {
            'status': False, 'message': 'Invalid data'
        }
        if not self.is_valid_uuid(item_uid):
            return resp
        resp = {
            'status': False, 'message': 'No such active item in the cart'
        }
        user_cart_obj = UserCart.fetch_user_cart(self.user_id)
        cart_id = user_cart_obj.id
        with transaction.atomic():
            cart_item = CartItems.fetch_obj(item_uid, cart_id)
            if cart_item and cart_item.quantity:
                cart_item.delete()
                resp['status'] = True
                resp["message"] = "Success"
        return resp

    def cart_checkout(self):
        pass

    def clear_cart(self):
        user_cart_obj = UserCart.fetch_user_cart(self.user_id)
        cart_id = user_cart_obj.id
        user_cart_items = CartItems.fetch_cart_items(cart_id)
        for item in user_cart_items:
            item.delete()
        return {'status': True}
