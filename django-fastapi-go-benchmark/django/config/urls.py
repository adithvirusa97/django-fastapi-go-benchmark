from django.urls import path
from benchmark.views import health, metrics, user_detail
urlpatterns = [path('health', health), path('metrics', metrics), path('users/<int:user_id>', user_detail)]
