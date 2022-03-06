from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.exceptions import ValidationError
from rest_framework import status
# from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import generics

from movie_app.models import WatchList, StreamPlatform, Review
from movie_app.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from movie_app.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly

from rest_framework.permissions import IsAuthenticated


# Create your views here.
class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        watch_list = WatchList.objects.all()
        serializer = WatchListSerializer(watch_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchListDetailsAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            watch_list = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Not found'}, status= status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(watch_list)
        return Response(serializer.data)

    def put (self, request, pk):
        watch_list = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(watch_list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        watch_list = WatchList.objects.get(pk=pk)
        watch_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Using viewsets for the list of streaming platforms
class StreamPlatformVS(viewsets.ViewSet):
    permission_classes = [IsAdminOrReadOnly]
    
    def list(self, request):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = StreamPlatform.objects.all()
        movie = get_object_or_404(queryset, pk=pk)
        serializer = StreamPlatformSerializer(movie)
        return Response(serializer.data)

class listVS(viewsets.ViewSet):
    def list(self, request):
        queryset = WatchList.objects.all()
        serializer = WatchListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve (self, request, pk=None):
        queryset = WatchList.objects.all()
        watchlist = get_object_or_404(queryset, pk=pk)
        serializer = WatchListSerializer(watchlist)
        return Response(serializer.data)

# API view class to show the complete list of streaming platforms
class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get (self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True, context={'request': request})
        return Response(serializer.data)

    def post (self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamPlatformDetailsAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Not found'}, status= status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put (self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        platform = WatchList.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    
    #overriding queryset = Review.objects.all
    def get_queryset(self, ):
        pk = self.kwargs.get('pk')
        return Review.objects.filter(watchlist=pk)

class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")

        if watchlist.total_rating == 0:
            watchlist.average_rating = serializer.validated_data['rating']
        else:
            watchlist.average_rating = (watchlist.average_rating + serializer.validated_data['rating'])/2
            watchlist.total_rating = watchlist.total_rating + 1
            watchlist.save()

        serializer.save(watchlist=watchlist, review_user=user)

class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]

#  generics and mixins class
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class ReviewDetails(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)