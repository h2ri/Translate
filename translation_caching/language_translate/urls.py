from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('language', views.LanguageViewSet, base_name='language')

urlpatterns = [
    #path('', views.index, name='index'),
    path('', include(router.urls)),
    path('translate', views.TranslateView.as_view(), name='translate'),

]