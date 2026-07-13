from rest_framework import serializers

from .models import Post, Category, Tag, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_date', 'parent', 'replies']

    def get_replies(self, obj):
        if obj.parent is None:
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False,
    )
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'title',
            'text',
            'slug',
            'category',
            'tags',
            'created_date',
            'published_date',
            'image',
            'thumbnail_img',
            'comments',
        ]
        read_only_fields = [
            'id',
            'author',
            'created_date',
            'published_date',
        ]
        extra_kwargs = {
            'image': {'write_only': True},
            'thumbnail_img': {'write_only': True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.category is not None:
            data['category'] = CategorySerializer(instance.category).data
        else:
            data['category'] = None

        data['tags'] = TagSerializer(instance.tags.all(), many=True).data

        data['image_url'] = instance.image.url if instance.image else None
        data['thumbnail_url'] = instance.thumbnail_img.url if instance.thumbnail_img else None

        return data

    def get_comments(self, obj):
        root_comments = obj.comments.filter(parent=None).order_by('-created_date')
        return CommentSerializer(root_comments, many=True).data