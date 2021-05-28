from django.urls import path
from .views import ProductRUDView, ProductListCreateView, CategoriesListView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='products'),
    path('<int:id>/', ProductRUDView.as_view(), name='product'),
    path('categories/', CategoriesListView.as_view(), name='categories'),
]
