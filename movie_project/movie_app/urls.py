from rest_framework.routers import DefaultRouter
from django.urls import path, include
from movie_app.views import (WatchListAV, WatchListDetailsAV, 
                            StreamPlatformAV, StreamPlatformDetailsAV)
from movie_app.views import ReviewList, ReviewDetails, ReviewCreate
from movie_app.views import StreamPlatformVS, listVS

router = DefaultRouter()
# router.register('stream', StreamPlatformVS, basename='streamplatform')
# router.register('list', listVS, basename='watchlists')

# https://www.imdb.com/title/tt10872600/ratings/?ref_=tt_ov_rt  #--->Real movie url
# http://127.0.0.1:8000/watch/movie_id/reviews/                  #--->Our URL
# Using this specific review we are cloning this thing

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='watch-list'),
    path('<int:pk>/', WatchListDetailsAV.as_view(), name='watch-details'),

    #using router
    # path('', include(router.urls)),
    path('stream/', StreamPlatformAV.as_view(), name='stream'),
    path('stream/<int:pk>', StreamPlatformDetailsAV.as_view(), name='stream-details'),

    # path('review/', ReviewList.as_view(), name='review-list'), 
    # path('review/<int:pk>', ReviewDetails.as_view(), name='review-details'),

    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-list'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetails.as_view(), name='review-details'),
]