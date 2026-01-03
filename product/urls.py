
from django.urls import path
from product import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product-detail/<int:pk>', views.product_detail, name='product_detail'),
    path('product-grid/', views.product_grid, name='product_grid'),
]
