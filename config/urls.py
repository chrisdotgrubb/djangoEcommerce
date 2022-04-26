import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('user/', include('user.urls', namespace='user')),
    path('checkout/', include('checkout.urls', namespace='checkout')),
    path('order/', include('order.urls', namespace='order')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', include('store.urls', namespace='store')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
