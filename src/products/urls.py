from django.urls import path
from .views import ProductRUDView, ProductListCreateView, CategoriesListCreateView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='products'),
    path('<int:id>/', ProductRUDView.as_view(), name='product'),
    path('categories/', CategoriesListCreateView.as_view(), name='categories'),
]
