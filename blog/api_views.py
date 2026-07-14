from django.utils import timezone
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    queryset = Post.objects.all().order_by('-created_date')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    
    search_fields = ['title', 'text', 'author__username', 'category__name', 'tags__name']
    
    filterset_fields = [
    'category',
    'author',
    'tags',
    'slug',
    ]

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            published_date=timezone.now()
        )
