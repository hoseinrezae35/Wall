from django.urls import path
from . import views

app_name = 'ads'

urlpatterns = [
    path('list', views.AdView.as_view(), name='ad_list'),
    path('added', views.CreatedView.as_view(), name='added'),
    path('detail/<int:pk>', views.DetailAdView.as_view(), name='detail'),
    path('search', views.AdSearchView.as_view(), name='search')
]
