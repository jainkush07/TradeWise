from django.urls import path
from . import views

app_name = 'cartApp'

urlpatterns = [
    path('pay/', views.initiate_payment, name='pay'),
    path('callback/', views.callback, name='callback'),
    path('proceed-to-gateway/', views.process_to_pg_view, name='process_to_pg_url'),
    path('cart/', views.CartDetailsView.as_view(), name='cart_details'),
    path('cart/item/<str:uid>/', views.CartItemView.as_view(), name='cart_item_view'),
    path('cart/item/', views.CartAddItemView.as_view(), name='cart_item_add_view'),
    path('tradebook/', views.TradebookGetAPIview.as_view(), name='TradebookGetAPIviewURL'),
    path('tradebook/sampleInvoice/', views.sampleInvoiceView.as_view(), name='TradebookGetAPIviewURL'),
    path('tradebook/InvoiceGeneration/', views.InvoiceGenerationView.as_view(), name='InvoiceGenerationUrl'),
    path('web/cart/', views.cart_detail_view, name='web_cart_details'),
    path('web/cart/item/<str:uid>/', views.cart_items_view, name='web_cart_item_view'),
    path('web/cart/item/', views.cart_add_item_view, name='web_cart_item_add_view'),

]
