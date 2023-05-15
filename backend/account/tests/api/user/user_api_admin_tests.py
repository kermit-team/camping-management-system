from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from account.models import User
from account.views import UserViewSet


class UserAPIAdminTests(APITestCase):
    
    fixtures = ['init_groups_and_permissions.json', 'users_test.json']
    factory = APIRequestFactory()
    
    def setUp(self):
        self.user = User.objects.filter(groups__name='Administratorzy').first()
           
    def test_get_another_user(self):
        view = UserViewSet.as_view({'get': 'retrieve'})
        another_user = User.objects.filter(groups__name='Recepcjoniści').first()
        request = self.factory.get(
            reverse(
                'user-detail',
                kwargs={'pk': another_user.id},
            ),
        )
        force_authenticate(request=request, user=self.user)
        
        response = view(request, pk=another_user.id)
        response.render()
        assert response.status_code == status.HTTP_200_OK
    
    def test_update_another_user(self):
        view = UserViewSet.as_view({'put': 'update'})
        another_user = User.objects.filter(groups__name='Recepcjoniści').first()
        request_data = {
            'password': 'Q@werty1234!',
            'first_name': 'Daniel',
            'last_name': 'Bąk',
        }
        request = self.factory.put(
            reverse(
                'user-detail',
                kwargs={'pk': another_user.id},
            ),
            request_data,
        )
        force_authenticate(request=request, user=self.user)

        response = view(request, pk=another_user.id)
        response.render()
        
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_partial_update_another_user(self):
        view = UserViewSet.as_view({'patch': 'partial_update'})
        another_user = User.objects.filter(groups__name='Recepcjoniści').first()
        request_data = {
            'password': 'Q@werty1234!',
            'first_name': 'Daniel',
            'last_name': 'Bąk',
        }
        request = self.factory.patch(
            reverse(
                'user-detail',
                kwargs={'pk': another_user.id},
            ),
            request_data,
        )
        force_authenticate(request=request, user=self.user)

        response = view(request, pk=another_user.id)
        response.render()
        
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_destroy_another_user(self):
        view = UserViewSet.as_view({'delete': 'destroy'})
        another_user = User.objects.filter(groups__name='Recepcjoniści').first()
        request = self.factory.delete(
            reverse(
                'user-detail',
                kwargs={'pk': another_user.id},
            ),
        )
        force_authenticate(request=request, user=self.user)
        
        response = view(request, pk=another_user.id)
        response.render()
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
