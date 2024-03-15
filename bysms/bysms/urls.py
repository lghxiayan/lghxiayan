from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include  # 注意include模块

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path('sales/', include('sales.urls')),  # 对http访问入口和处理函数，进行关联

                  path('api/mgr/', include('mgr.urls')),

              ] + static('/', document_root='./z_dist')
