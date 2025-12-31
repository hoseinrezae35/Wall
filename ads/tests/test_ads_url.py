from django.urls import resolve, reverse
from rest_framework.test import APITestCase
from .. import views
from ..models import Ad


class TestUrls(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ad = Ad.objects.create(title='Iphone', caption='Nice')

    def test_ad_list_url(self):
        url = reverse('ads:ad_list')
        self.assertEqual(resolve(url).func.view_class, views.AdView)

    def test_ad_create_url(self):
        url = reverse('ads:added')
        self.assertEqual(resolve(url).func.view_class, views.CreatedView)

    def test_ad_detail_url(self):
        url = reverse('ads:detail', kwargs={'pk': self.ad.id})
        self.assertEqual(resolve(url).func.view_class, views.DetailAdView)

    def test_ad_search_url(self):
        url = reverse('ads:search')
        self.assertEqual(resolve(url).func.view_class, views.AdSearchView)
