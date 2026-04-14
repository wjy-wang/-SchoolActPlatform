from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger配置
schema_view = get_schema_view(
   openapi.Info(
      title="校园活动发布平台API",
      default_version='v1',
      description="校园活动发布平台API文档",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.activities.urls')),
    path('api/', include('apps.enrollments.urls')),
    path('api/', include('apps.comments.urls')),
    path('api/', include('apps.favorites.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
