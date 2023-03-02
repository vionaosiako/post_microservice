from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import PostSerializier
from rest_framework.response import Response
from .models import Post
import requests
import json
# Create your views here.
class PostAPIView(APIView):
    def get(self, request):
        post = Post.objects.all()
        serializer = PostSerializier(post, many=True)
        return Response([self.formatPost(p) for p in post])
    
    def formatPost(self, post):
        comments = requests.get('http://127.0.0.1:8000/posts/%d/comments' % post.id).json()
        return{
            'id': post.id,
            'title':post.title,
            'description':post.description,
            'comments': comments
        }
    
    def post(self, request):  
        serializer = PostSerializier(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
# class PostViewset(viewsets.ModelViewSet):
#     serializer_class = PostSerializier
#     queryset = Post.objects.all()