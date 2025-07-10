from django.urls import path
from . import views
from .views import calculate_brokerage
from .views import submit_broker_suggestion


urlpatterns = [
    path('', views.home, name='home'),  # Homepage with form
    path('contact/', views.contact_view, name='contact'),  # AJAX contact form
    path('blog/', views.blog_page, name='blog-page'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog-detail'),
    path('api/blogs/', views.blog_list, name='blog-list'),
    path('api/brokers/', views.broker_list, name='broker-list'),
    path('compare/', views.broker_comparison_page, name='broker-comparison'),
    path('api/calculate/', calculate_brokerage, name='calculate-brokerage'),  # DRF API for brokerage
    path('api/suggest-broker/', submit_broker_suggestion, name='suggest-broker'),
]

