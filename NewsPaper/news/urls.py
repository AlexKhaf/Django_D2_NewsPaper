from django.urls import path
from .views import NewsList, NewsDetail, NewsCreateView, NewsDeleteView, NewsUpdateView


urlpatterns = [
    path('', NewsList.as_view(), name='news_home'),
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('add/', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),

]
