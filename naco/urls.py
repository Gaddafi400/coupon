from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import Group

from naco import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('coupons.urls')),
    path("", include('django.contrib.auth.urls')),
    path('l/', views.user_logout_view, name='user_logout'),
    path('user_logout_done/', views.user_logout_done, name='user_logout_done'),
]

admin.site.unregister(Group)
admin.site.site_header = 'Naco Coupon System Admin'
admin.site.site_title = 'Naco Admin Portal'
admin.site.index_title = 'Welcome to Naco Coupon Portal'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



