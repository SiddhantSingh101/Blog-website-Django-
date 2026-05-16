from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Post


class PostAPITests(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username="author",
            email="author@example.com",
            password="pass12345",
        )
        self.other_user = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="pass12345",
        )
        self.post = Post.objects.create(
            title="First post",
            content="Hello from the API",
            author=self.author,
        )

    def test_posts_can_be_listed_without_login(self):
        response = self.client.get(reverse("api_post_list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], self.post.title)

    def test_login_is_required_to_create_post(self):
        response = self.client.post(
            reverse("api_post_list"),
            {"title": "New post", "content": "Created through REST"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_create_post(self):
        self.client.force_authenticate(user=self.author)

        response = self.client.post(
            reverse("api_post_list"),
            {"title": "New post", "content": "Created through REST"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"], self.author.id)

    def test_only_author_can_delete_post(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.delete(reverse("api_post_detail", args=[self.post.id]))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())
