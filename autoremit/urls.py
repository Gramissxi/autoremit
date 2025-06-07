from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('remitos.urls')),  # Esto apunta a tu app remito
    
]





