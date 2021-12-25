import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from config.swagger import urlpatterns as swagger_urlpattern

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += [
        *swagger_urlpattern,
    ]

if settings.TOOLBAR:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
