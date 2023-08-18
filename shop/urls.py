from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth

app_name = 'shop'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('shop/<int:page>', views.shop, name='shop'),
    path('shop/<name>/<int:page>/', views.shop_cat, name='shop-cat'),
    path('company/<int:id>/<int:page>/', views.company_shop, name='company-shop'),
    path('product/<int:id>/', views.product, name='product'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove-from-cart'),
    path('reduce-order-quantity/<int:id>/', views.reduce_order_quantity, name='reduce-order-quantity'),
    path('cart/', views.order_summary, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('accounts/login/', views.login_view, name='login_page'),
    path('register/', views.register_view, name='register_page'),
    path('logout/', views.logout_view, name='logout')
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)