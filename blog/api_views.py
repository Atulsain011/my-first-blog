import json
from urllib.parse import quote_plus

from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, BaseParser

from .models import Post
from .serializers import PostSerializer


class PlainTextParser(BaseParser):
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read().decode('utf-8')


def _coerce_request_data(request):
    if isinstance(request.data, str):
        try:
            parsed = json.loads(request.data)
        except (TypeError, ValueError):
            parsed = {'text': request.data}

        if isinstance(parsed, dict):
            return parsed

        return {'text': parsed}

    return request.data


@api_view(['GET'])
def api_root(request):
    """List the available blog API endpoints and supported filters."""
    return Response({
        'posts': request.build_absolute_uri(reverse('api_post_list')),
        'post_detail_example': request.build_absolute_uri(
            reverse('api_post_detail', kwargs={'pk': 1})
        ),
        'filters': {
            'search': 'Search title, text, author, category and tags.',
            'category': 'Filter by category name or slug.',
            'tag': 'Filter by tag name or slug.',
        },
    })


@api_view(['GET', 'POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser, PlainTextParser])
def post_list(request):
    if request.method == 'GET':
        filter_type = request.query_params.get('filter_type', '').strip()
        filter_value = request.query_params.get('filter_value', '').strip()

        if filter_type == 'id' and filter_value.isdigit():
            return redirect(reverse('api_post_detail', kwargs={'pk': int(filter_value)}))

        if filter_type in {'category', 'author', 'tag', 'slug', 'search'} and filter_value:
            query_string = f"{filter_type}={quote_plus(filter_value)}"
            return redirect(f"{reverse('api_post_list')}?{query_string}")

        posts = Post.objects.select_related('author', 'category').prefetch_related('tags').order_by('-created_date')
        search = request.query_params.get('search', '').strip()
        category = request.query_params.get('category', '').strip()
        author = request.query_params.get('author', '').strip()
        tag = request.query_params.get('tag', '').strip()
        slug = request.query_params.get('slug', '').strip()

        if filter_type == 'category' and filter_value:
            category = filter_value
        elif filter_type == 'author' and filter_value:
            author = filter_value
        elif filter_type == 'tag' and filter_value:
            tag = filter_value
        elif filter_type == 'slug' and filter_value:
            slug = filter_value
        elif filter_type == 'search' and filter_value:
            search = filter_value

        if search:
            posts = posts.filter(
                Q(title__icontains=search) |
                Q(text__icontains=search) |
                Q(author__username__icontains=search) |
                Q(category__name__icontains=search) |
                Q(tags__name__icontains=search)
            )

        if category:
            posts = posts.filter(
                Q(category__slug__iexact=category) |
                Q(category__name__iexact=category)
            )

        if author:
            posts = posts.filter(author__username__iexact=author)

        if tag:
            posts = posts.filter(
                Q(tags__slug__iexact=tag) |
                Q(tags__name__iexact=tag)
            )

        if slug:
            posts = posts.filter(slug__iexact=slug)

        posts = posts.distinct()

        serializer = PostSerializer(posts, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Please login before creating a post.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = PostSerializer(data=_coerce_request_data(request))

        if serializer.is_valid():
            post = serializer.save(
                author=request.user,
                published_date=timezone.now()
            )

            return Response(
                PostSerializer(post).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@parser_classes([JSONParser, FormParser, MultiPartParser, PlainTextParser])
def post_detail(request, pk):
    post = Post.objects.filter(pk=pk).first()

    if post is None:
        return Response(
            {'detail': 'Post not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Please login first.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        partial = request.method == 'PATCH'

        serializer = PostSerializer(
            post,
            data=_coerce_request_data(request),
            partial=partial
        )

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    if request.method == 'DELETE':
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Please login first.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


post_list.cls.serializer_class = PostSerializer
post_detail.cls.serializer_class = PostSerializer

