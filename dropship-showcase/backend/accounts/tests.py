from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User


class SignupTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("signup")

    def test_signup_success(self):
        res = self.client.post(self.url, {
            "name": "Test User",
            "email": "test@example.com",
            "password": "Secure123",
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", res.data)
        self.assertIn("user", res.data)

    def test_signup_duplicate_email(self):
        User.objects.create_user(email="dup@example.com", name="Dup", password="Secure123")
        res = self.client.post(self.url, {
            "name": "Dup",
            "email": "dup@example.com",
            "password": "Secure123",
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_409_CONFLICT)

    def test_signup_weak_password(self):
        res = self.client.post(self.url, {
            "name": "Test",
            "email": "test2@example.com",
            "password": "nouppercase1",
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)


class SigninTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("signin")
        self.user = User.objects.create_user(
            email="login@example.com", name="Login User", password="Secure123"
        )

    def test_signin_success(self):
        res = self.client.post(self.url, {
            "email": "login@example.com",
            "password": "Secure123",
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def test_signin_wrong_password(self):
        res = self.client.post(self.url, {
            "email": "login@example.com",
            "password": "WrongPass1",
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class MeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("me")
        self.user = User.objects.create_user(
            email="me@example.com", name="Me User", password="Secure123"
        )

    def _get_token(self):
        from rest_framework_simplejwt.tokens import RefreshToken
        return str(RefreshToken.for_user(self.user).access_token)

    def test_me_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self._get_token()}")
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["user"]["email"], "me@example.com")

    def test_me_unauthenticated(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
