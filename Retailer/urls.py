from Retailer import views
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView
from rest_framework import routers
from django.urls.conf import include
from django.template.context_processors import request



urlpatterns = [
    path('', views.HomeView.as_view()),
    path('report/', views.ReportListView.as_view()),
    path('report/edit/<int:pk>',views.ReportUpdateView.as_view(success_url="/retailer/home/")),
    path('order/', views.OrderListView.as_view()),
    path('order/create',views.OrderCreateView.as_view(success_url="/retailer/order/")),
    path('notice/', views.NoticeListView.as_view()),
    path('home/',views.HomeView.as_view())
]
