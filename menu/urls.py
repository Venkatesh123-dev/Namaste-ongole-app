from django.urls import path
from .views import *


urlpatterns = [
    path('categories/', CategoryList.as_view(), name="category_list"),
    path('categories/<int:pk>/products', ProductList.as_view(), name="product_list"),
    path('categories/add', AddCategory.as_view(), name="category_add"),
    path('categories/<int:pk>/products/add', AddProduct.as_view(), name="product_add"),
    path('recommended/', RandomProducts.as_view(), name="recommended_products"),
    path('offers/', OfferList.as_view(), name="offer_list"),
    # path('categories/<int:pk>/products/options', ProductOptionsList.as_view(), name="product_option_list"),
]

