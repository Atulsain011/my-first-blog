from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from urllib.parse import urlencode

from .models import Post, Category, Tag


class PostAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='apiuser',
            password='strong-pass-123',
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Initial title',
            text='Initial content',
            published_date=timezone.now(),
        )

    def _get_posts(self, response):
        if isinstance(response.data, dict) and 'results' in response.data:
            return response.data['results']
        return response.data

    def test_list_posts(self):
        url = reverse('api_post_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        posts = self._get_posts(response)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]['title'], 'Initial title')

    def test_list_posts_html(self):
        url = reverse('api_post_list')
        response = self.client.get(url, HTTP_ACCEPT='text/html')
        self.assertEqual(response.status_code, 200)

    def test_create_post_requires_authentication(self):
        url = reverse('api_post_list')
        response = self.client.post(url, {'title': 'New title', 'text': 'New content'})

        self.assertEqual(response.status_code, 403)

    def test_create_post_accepts_form_data(self):
        self.client.force_authenticate(user=self.user)

        url = reverse('api_post_list')
        response = self.client.post(
            url,
            urlencode({'title': 'Form title', 'text': 'Form content'}),
            content_type='application/x-www-form-urlencoded',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'Form title')

    def test_create_post_accepts_multipart_requests(self):
        self.client.force_authenticate(user=self.user)

        url = reverse('api_post_list')
        response = self.client.post(
            url,
            {'title': 'Multipart title', 'text': 'Multipart content'},
            format='multipart',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'Multipart title')

    def test_create_post_accepts_ids_and_returns_nested_relationships(self):
        self.client.force_authenticate(user=self.user)

        category = Category.objects.create(name='Technology', slug='technology')
        tag_one = Tag.objects.create(name='Python', slug='python')
        tag_two = Tag.objects.create(name='Django', slug='django')

        response = self.client.post(
            reverse('api_post_list'),
            {
                'title': 'Nested relationships',
                'text': 'Content with ids',
                'category': category.pk,
                'tags': [tag_one.pk, tag_two.pk],
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['category']['name'], 'Technology')
        self.assertEqual(response.data['category']['slug'], 'technology')
        self.assertEqual(response.data['tags'][0]['name'], 'Python')
        self.assertEqual(response.data['tags'][1]['name'], 'Django')

    def test_search_posts_by_title(self):
        Post.objects.create(
            author=self.user,
            title='Searchable title',
            text='Some unique content',
            published_date=timezone.now(),
        )

        url = reverse('api_post_list') + '?search=Searchable'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        posts = self._get_posts(response)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]['title'], 'Searchable title')

    def test_search_posts_by_text(self):
        url = reverse('api_post_list') + '?search=Initial+content'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        posts = self._get_posts(response)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]['id'], self.post.id)

    def test_search_posts_phrase_matching(self):
        # Create a post containing "the" and "man" but not "the man" as a phrase
        Post.objects.create(
            author=self.user,
            title='Another post with the and man',
            text='He is a romantic person in the town of Manjeri',
            published_date=timezone.now(),
        )

        # Search for "the man" as a phrase
        url = reverse('api_post_list') + '?search=the+man'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        posts = self._get_posts(response)
        # It should not match the new post since it doesn't contain the exact phrase "the man"
        for post in posts:
            self.assertNotEqual(post['title'], 'Another post with the and man')

    def test_search_posts_by_extended_fields(self):
        category = Category.objects.create(name='Gadgets', slug='gadgets')
        tag = Tag.objects.create(name='Gaming', slug='gaming')
        second_user = get_user_model().objects.create_user(
            username='arjun',
            password='strong-pass-123',
        )
        post = Post.objects.create(
            author=second_user,
            title='Tech News',
            text='Some interesting content',
            category=category,
            published_date=timezone.now(),
        )
        post.tags.add(tag)

        # Search by author username
        url = reverse('api_post_list') + '?search=arjun'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        posts = self._get_posts(response)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]['title'], 'Tech News')

        # Search by category name
        url = reverse('api_post_list') + '?search=Gadgets'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        posts = self._get_posts(response)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]['title'], 'Tech News')

        # Search by tag name
        url = reverse('api_post_list') + '?search=Gaming'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        posts = self._get_posts(response)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]['title'], 'Tech News')

    def test_filter_posts_by_author(self):
        second_user = get_user_model().objects.create_user(
            username='seconduser',
            password='strong-pass-123',
        )
        Post.objects.create(
            author=second_user,
            title='Another title',
            text='Another content',
            published_date=timezone.now(),
        )

        response = self.client.get(reverse('api_post_list') + '?author=seconduser')

        self.assertEqual(response.status_code, 200)
        posts = self._get_posts(response)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]['title'], 'Another title')

    def test_filter_posts_by_slug(self):
        Post.objects.create(
            author=self.user,
            title='Slug test',
            text='Slug content',
            slug='my-post',
            published_date=timezone.now(),
        )

        response = self.client.get(reverse('api_post_list') + '?slug=my-post')

        self.assertEqual(response.status_code, 200)
        posts = self._get_posts(response)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]['slug'], 'my-post')

    def test_filter_posts_by_multiple_parameters(self):
        category = Category.objects.create(name='Tech', slug='tech')
        Post.objects.create(
            author=self.user,
            title='Multi filter match',
            text='Matching content',
            category=category,
            published_date=timezone.now(),
        )
        url_non_matching = reverse('api_post_list') + '?category=tech&author=nonexistent'
        response_none = self.client.get(url_non_matching)
        self.assertEqual(response_none.status_code, 200)
        posts_none = self._get_posts(response_none)
        self.assertEqual(len(posts_none), 0)

        url_matching = reverse('api_post_list') + f'?category=tech&author={self.user.username}'
        response_one = self.client.get(url_matching)
        self.assertEqual(response_one.status_code, 200)
        posts_one = self._get_posts(response_one)
        self.assertEqual(len(posts_one), 1)
        self.assertEqual(posts_one[0]['title'], 'Multi filter match')

    def test_filter_posts_by_tag_normalization(self):
        tag = Tag.objects.create(name='Taj Mahal', slug='taj-mahal')
        post = Post.objects.create(
            author=self.user,
            title='Taj Mahal Visit',
            text='Amazing trip',
            published_date=timezone.now(),
        )
        post.tags.add(tag)

        # Test tags=tajmahal
        response = self.client.get(reverse('api_post_list') + '?tags=tajmahal')
        self.assertEqual(response.status_code, 200)
        posts = self._get_posts(response)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]['title'], 'Taj Mahal Visit')

        # Test tags=taj+mahal
        response = self.client.get(reverse('api_post_list') + '?tags=taj mahal')
        self.assertEqual(response.status_code, 200)
        posts = self._get_posts(response)
        self.assertEqual(len(posts), 1)

        # Test tag=tajmahal
        response = self.client.get(reverse('api_post_list') + '?tag=tajmahal')
        self.assertEqual(response.status_code, 200)
        posts = self._get_posts(response)
        self.assertEqual(len(posts), 1)

    def test_api_does_not_expose_photo_fields(self):
        response = self.client.get(reverse('api_post_list'))
        posts = self._get_posts(response)

        self.assertNotIn('image', posts[0])
        self.assertNotIn('thumbnail_img', posts[0])

    def test_put_update_post(self):
        self.client.force_authenticate(user=self.user)

        put_url = reverse('api_post_detail', kwargs={'slug': self.post.slug})
        put_response = self.client.put(
            put_url,
            {'title': 'Updated by PUT', 'text': 'Updated content'},
            format='json',
        )

        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(put_response.data['title'], 'Updated by PUT')

    def test_partial_update_and_delete_post(self):
        self.client.force_authenticate(user=self.user)

        patch_url = reverse('api_post_detail', kwargs={'slug': self.post.slug})
        patch_response = self.client.patch(
            patch_url,
            {'title': 'Updated title'},
            format='json',
        )

        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_response.data['title'], 'Updated title')

        delete_response = self.client.delete(patch_url)
        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
