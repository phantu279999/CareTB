from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.customer import urls as customer_urls
from core.treatment import urls as treatment_urls
from core.product import urls as service_product_urls
from core.hr import urls as human_resource_urls
from core.general import urls as general_urls


schema_view = get_schema_view(
    openapi.Info(
        title="TB Oriental Medicine Clinic API",
        default_version="v1",
        description="API for TB Oriental Medicine Clinic",
    ),
    url="http://localhost:8000/api/v1/",
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('product/', include(service_product_urls)),
    path('hr/', include(human_resource_urls)),
    path('settings/', include(general_urls)),
    path('customer/', include(customer_urls)),
    path('treatment/', include(treatment_urls)),

    # JWT authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
