from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="My Django notes",
        default_version='v1',
        description="Test description",
        terms_of_service="https://t.me/almazisheee",
        contact=openapi.Contact(url='https://t.me/almazisheee'),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('documentation/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

        # Authorization
        path('auth/', include('src.accounts.urls')),

        # Products
        path('products/', include('src.products.urls')),
    ]))
]
