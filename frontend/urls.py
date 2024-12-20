from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.shop, name='shop'),
    path('chat/', views.chat, name='chat'),
    path('chat/send_message/', views.process_chat_message, name='send_message'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update-quantity/', views.update_quantity, name='update_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/analytics/', views.analytics, name='analytics'),
    path('dashboard/products/', views.products, name='products'), 
]