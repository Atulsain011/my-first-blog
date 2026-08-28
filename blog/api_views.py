import re
import django_filters
from django.utils import timezone
from django import forms
from rest_framework import filters, viewsets
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Category, Tag
from .serializers import PostSerializer
from .pagination import PostPagination

class PostFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), to_field_name='slug', label='Category')
    tag = django_filters.ModelChoiceFilter(field_name='tags', queryset=Tag.objects.all(), to_field_name='slug', widget=forms.HiddenInput(), label='Tag')
    tags = django_filters.ModelMultipleChoiceFilter(field_name='tags__slug', queryset=Tag.objects.all(), to_field_name='slug', label='Tags')
    author = django_filters.ModelChoiceFilter(queryset=Post._meta.get_field('author').remote_field.model.objects.all(), to_field_name='username', label='Author')
    slug = django_filters.CharFilter(field_name='slug', lookup_expr='iexact', label='Slug')

    class Meta:
        model = Post
        fields = ['category', 'tag', 'tags', 'author', 'slug']

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            if 'tags' in data:
                tags_list = data.getlist('tags')
                new_tags = []
                for val in tags_list:
                    norm_val = re.sub(r'[\s_-]+', '', val).lower()
                    matched_slug = None
                    for tag in Tag.objects.all():
                        if re.sub(r'[\s_-]+', '', tag.slug).lower() == norm_val or re.sub(r'[\s_-]+', '', tag.name).lower() == norm_val:
                            matched_slug = tag.slug
                            break
                    if matched_slug:
                        new_tags.append(matched_slug)
                    else:
                        new_tags.append(val)
                data.setlist('tags', new_tags)
            if 'tag' in data:
                val = data.get('tag')
                norm_val = re.sub(r'[\s_-]+', '', val).lower()
                matched_slug = None
                for tag in Tag.objects.all():
                    if re.sub(r'[\s_-]+', '', tag.slug).lower() == norm_val or re.sub(r'[\s_-]+', '', tag.name).lower() == norm_val:
                        matched_slug = tag.slug
                        break
                if matched_slug:
                    data['tag'] = matched_slug
        super().__init__(data, *args, **kwargs)

    def is_valid(self):
        is_val = super().is_valid()
        if not is_val:
            for field in list(self.form.errors.keys()):
                if field in ['category', 'tag', 'tags', 'author']:
                    self.form.errors.pop(field)
                    model = self.filters[field].queryset.model
                    self.form.cleaned_data[field] = model.objects.none() if field == 'tags' else model(pk=-1)
            return not self.form.errors
        return is_val

class PhraseSearchFilter(filters.SearchFilter):
    def get_search_terms(self, request):
        params = request.query_params.get(self.search_param, '')
        params = params.replace('\x00', '')  # strip null bytes
        params = params.strip()
        return [params] if params else []

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_date')
    serializer_class = PostSerializer
    pagination_class = PostPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, PhraseSearchFilter]
    filterset_class = PostFilter
    search_fields = ['title', 'text', 'author__username', 'category__name', 'tags__name']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, published_date=timezone.now())
