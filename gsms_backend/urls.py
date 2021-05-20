"""gsms_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from gsms.views import DashboardViewSet, MaterialChangeHistoryViewSet, MaterialViewSet, PackingListChangeHistoryViewSet, PackingListViewSet, TransferLocationViewSet, UserViewSet
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'material', MaterialViewSet)
router.register(r'packing-list', PackingListViewSet)
# router.register(r'pallet', PalletViewSet)
router.register(r'material-change-history', MaterialChangeHistoryViewSet)
router.register(r'packinglist-change-history', PackingListChangeHistoryViewSet)
router.register(r'users', UserViewSet)
router.register(r'transfer-location', TransferLocationViewSet)

router.register(r'dashboard', DashboardViewSet, basename='dashboard')


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
