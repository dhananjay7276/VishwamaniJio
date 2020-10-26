
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic.base import RedirectView
from django.conf.urls.static import static 
from VishwamaniJio import settings


admin.site.site_header = 'Vishwamani Jio admin'
admin.site.site_title = 'Vishwamani Jio admin'
admin.site.index_title = 'Vishwamani Jio administration'
admin.empty_value_display = '**Empty**'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('retailer/', include('Retailer.urls')),
    path('accounts/', include('registration.backends.default.urls')),
    path('', RedirectView.as_view(url ='retailer/'))
] + static ( settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 
