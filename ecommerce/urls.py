import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('ecommerce.apps.cart.urls', namespace='cart')),
    path('user/', include('ecommerce.apps.user.urls', namespace='user')),
    path('checkout/', include('ecommerce.apps.checkout.urls', namespace='checkout')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', include('ecommerce.apps.store.urls', namespace='store')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
