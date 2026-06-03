from django.urls import path
from .views import (
    FavoriteListView,
    AllFavoriteListView,
    FavoriteCreateView,
    FavoriteDeleteView
)

urlpatterns = [
    path('favorites/', FavoriteListView.as_view(), name='favorite-list'),
    path('favorites/all/', AllFavoriteListView.as_view(), name='all-favorite-list'),
    path('favorites/create/', FavoriteCreateView.as_view(), name='favorite-create'),
    path('favorites/<int:pk>/', FavoriteDeleteView.as_view(), name='favorite-delete'),
]
