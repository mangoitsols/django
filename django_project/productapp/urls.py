from django.contrib import admin
from django.urls import path,include
from productapp import views

app_name = 'productapp'
urlpatterns = [
    path('', views.index,name='home'),
    path('contact/', views.contact,name='contact'),
    path('about/', views.about,name='about'),
    path('privacy/', views.privacy,name='privacy'),
    path('products/', views.products, name='products'),
    path('products/<int:id>/', views.product_detail,name='product_detail'),
    path('products/add/', views.ProductCreateView.as_view(), name='add_product'),
    path('products/update/<int:pk>/', views.ProductUpdateView.as_view(), name='update_product'),
    path('products/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='delete_product'),
    path('products/mylisting/', views.my_listing, name='mylisting'),
    path('cart/', views.show_cart, name='show_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_failed/', views.payment_failed, name='payment_failed'),
    path('paypal/', include("paypal.standard.ipn.urls")),
]