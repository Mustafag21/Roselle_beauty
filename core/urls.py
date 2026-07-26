from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('urunler/', views.products_page, name='products'),
    path('urunler/<slug:slug>/', views.product_detail, name='product_detail'),
    path('hizmetler/', views.services_page, name='services'),
    path('hizmetler/<slug:slug>/', views.service_detail, name='service_detail'),
    path('hakkimizda/', views.about_page, name='about'),
    path('iletisim/', views.contact_page, name='contact'),
    path('iletisim/gonder/', views.contact_submit, name='contact_submit'),
    path('blog/', views.blog_page, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('sss/', views.faq_page, name='faq'),
    path('bulten/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('arama/', views.search_page, name='search'),
]
