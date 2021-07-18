from django.db.models.query import Prefetch
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import viewsets
import sys
import traceback
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from rest_framework.decorators import action
from .models import Post, Catagory
from .serializer import PostSerializer, PostDetailSerializer
from rest_framework.permissions import IsAuthenticated


class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class PostListView(ListAPIView):

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = Post.objects.filter(isPublished=True)
        return queryset


class PostDetialView(RetrieveAPIView):

    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get_queryset(self):
        queryset = Post.objects.filter(isPublished=True)\
            .select_related("author") \
            .prefetch_related(Prefetch(
                'category',
                queryset=Catagory.objects.all().only(
                    'name'
                )
            ))
        return queryset


class PostUserView(viewsets.ModelViewSet):
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated, UserPermission]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.filter(
            author=request.user).only("title", "content")
        serializer = self.get_serializer(
            queryset, many=True, fields=('title', 'content'))
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_publish(self, request, slug=None):
        post = self.get_object()
        try:
            if(request.data['publish']):
                post.isPublished = request.data['publish']
                post.save()

            return Response({'response': 'publish toggled succesfully'})
        except Exception as e:
            print(e)
            return Response('error')
