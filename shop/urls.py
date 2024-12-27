from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('create/', views.order_create, name='order_create'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.get_user, name='get_user'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login'),
    path('update/', views.update_user, name='update'),
    path('past/', views.past_orders, name='past'),
    path('remove/<int:product_id>/', views.cart_remove, name='remove'),
    path('increase/<int:product_id>/', views.cart_increase, name='increase'),
    path('confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
]
