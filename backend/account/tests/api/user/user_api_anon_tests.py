from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from account.models import User
from account.views import UserViewSet


class UserAPIAnonTests(APITestCase):
    fixtures = ['init_groups_and_permissions.json', 'users_test.json']
    factory = APIRequestFactory()

    def setUp(self):
        self.user = User.objects.all().first()

    def test_create_user(self):
        view = UserViewSet.as_view({'post': 'create'})
        request_data = {
            'email': 'example@gmail.com',
            'password': 'Q@werty123!',
            'first_name': 'Adam',
            'last_name': 'Kowalski',
        }
        request = self.factory.post(
            reverse(
                'user-list',
            ),
            request_data,
        )

        response = view(request)
        response.render()
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_users_without_permissions(self):
        view = UserViewSet.as_view({'get': 'list'})
        request = self.factory.get(
            reverse(
                'user-list',
            ),
        )

        response = view(request)
        response.render()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_user_without_permissions(self):
        view = UserViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(
            reverse(
                'user-detail',
                kwargs={'pk': self.user.id},
            ),
        )

        response = view(request, pk=self.user.id)
        response.render()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_user_without_permissions(self):
        view = UserViewSet.as_view({'put': 'update'})
        request_data = {
            'password': 'Q@werty1234!',
            'first_name': 'Daniel',
            'last_name': 'Bąk',
        }
        request = self.factory.put(
            reverse(
                'user-detail',
                kwargs={'pk': self.user.id},
            ),
            request_data,
        )

        response = view(request, pk=self.user.id)
        response.render()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_partial_update_user_without_permissions(self):
        view = UserViewSet.as_view({'patch': 'partial_update'})
        request_data = {
            'password': 'Q@werty1234!',
            'first_name': 'Daniel',
            'last_name': 'Bąk',
        }
        request = self.factory.patch(
            reverse(
                'user-detail',
                kwargs={'pk': self.user.id},
            ),
            request_data,
        )

        response = view(request, pk=self.user.id)
        response.render()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_destroy_user_without_permissions(self):
        view = UserViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(
            reverse(
                'user-detail',
                kwargs={'pk': self.user.id},
            ),
        )

        response = view(request, pk=self.user.id)
        response.render()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
