from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/', views.cart_update, name='cart_update'),

    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/', views.order_success, name='order_success'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('policies/shipping/', views.shipping_policy, name='shipping'),
    path('policies/returns/', views.returns_policy, name='returns'),
    path('policies/privacy/', views.privacy_policy, name='privacy'),
    path('policies/terms/', views.terms, name='terms'),

    path('theme/<str:mode>/', views.theme_toggle, name='theme_toggle'),
]