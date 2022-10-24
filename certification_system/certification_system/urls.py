from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from event.views import EventViewSet
from category.views import CategoryViewSet
from certificate.views import (
    CertificateViewSet,
    BulkCertificateGenerator,
    EmailSenderView,
)
from django.conf.urls.static import static
from django.conf import settings


router = routers.DefaultRouter()
router.register(r"events", EventViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"certificates", CertificateViewSet)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from authencation.views import BlacklistTokenUpdateView

# router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path(
        "generate-bulk-certificate/",
        BulkCertificateGenerator.as_view(),
        name="generate-bulk-certificate",
    ),
    path("send-email/", EmailSenderView.as_view(), name="send-email"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/token/blacklist/", BlacklistTokenUpdateView.as_view(), name="blacklist"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
