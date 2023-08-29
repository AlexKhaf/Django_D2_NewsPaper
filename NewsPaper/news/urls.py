from django.urls import path
from .views import NewsList, NewsDetail, NewsCreateView, NewsDeleteView, \
    NewsUpdateView, LogoutView, upgrade_me, downgrade_me, CategoryDetail, \
    subscribe, unsubscribe
from django.views.decorators.cache import cache_page

# app_name = 'news'

urlpatterns = [
    path('', NewsList.as_view(), name='news_home'),
    # path('', cache_page(60)(NewsList.as_view()), name='news_home'),
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    # path('<int:pk>/', cache_page(60*5)(NewsDetail.as_view()), name='news_detail'),
    path('add/', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('downgrade/', downgrade_me, name = 'downgrade'),
    path('category/<int:pk>/', CategoryDetail.as_view(), name='category'),
    path('subscribe/<int:pk>/', subscribe, name = 'subscribe'),
    path('unsubscribe/<int:pk>/', unsubscribe, name = 'unsubscribe'),

]
