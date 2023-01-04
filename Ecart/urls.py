from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]

admin.site.site_header = "MyEcartStore administration"
admin.site.site_title = "MyEcartStore Admin Portal"
admin.site.index_title = "Welcome to MyEcartStore Admin Portal"