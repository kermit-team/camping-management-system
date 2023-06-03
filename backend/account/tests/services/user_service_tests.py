from django.test import TestCase

from account.models import User
from account.services import UserService


class UserServiceTests(TestCase):

    def setUp(self):
        User.objects.create(
            email='patrol0990@gmail.com',
            password='Q@werty123!',
            first_name='Patryk',
            last_name='Jankowski',
        )
        self.last_user = User.objects.create(
            email='adam0990@gmail.com',
            password='Q@werty123!',
            first_name='Adam',
            last_name='Jankowski',
        )

    @staticmethod
    def test_create_user():
        users = User.objects.all()
        user_data = {
            'email': 'adam01@gmail.com',
            'password': 'Q@werty123!',
            'first_name': 'Adam',
            'last_name': 'Kowalski',
        }
        service_response = UserService.create_user(user_data)
        assert service_response['status'] == 'Success'

        created_user = service_response['content']
        assert created_user in users
        assert not created_user.is_active

    @staticmethod
    def test_create_user_with_email_already_used():
        user_data = {
            'email': 'patrol0990@gmail.com',
            'password': 'Q@werty123!',
            'first_name': 'Adam',
            'last_name': 'Kowalski',
        }
        service_response = UserService.create_user(user_data)
        assert service_response['status'] == 'Error'

    @staticmethod
    def test_get_all_users():
        users = list(User.objects.all().order_by('id'))

        service_response = UserService.get_users()
        assert service_response['status'] == 'Success'

        users_collected_via_service = list(service_response['content'])
        assert users == users_collected_via_service

    @staticmethod
    def test_get_all_users_with_order_by():
        users = list(User.objects.all().order_by('-first_name'))

        service_response = UserService.get_users(order_by='-first_name')
        assert service_response['status'] == 'Success'

        users_collected_via_service = list(service_response['content'])
        assert users == users_collected_via_service

    @staticmethod
    def test_get_all_users_with_filters():
        users = list(User.objects.filter(first_name__in=['Patryk']).order_by('id'))

        service_response = UserService.get_users(filters={'first_name__in': ['Patryk']})
        assert service_response['status'] == 'Success'

        users_collected_via_service = list(service_response['content'])
        assert users == users_collected_via_service

    def test_get_user(self):
        user_id = self.last_user.id
        user = User.objects.get(id=user_id)

        service_response = UserService.get_user(pk=user_id)
        assert service_response['status'] == 'Success'

        user_collected_via_service = service_response['content']
        assert user == user_collected_via_service

    def test_get_user_with_invalid_id(self):
        user_id = self.last_user.id + 1
        service_response = UserService.get_user(pk=user_id)
        assert service_response['status'] == 'Error'

    def test_update_user(self):
        user_id = self.last_user.id
        user_new_first_name = 'Grzegorz'
        service_response = UserService.update_user(
            pk=user_id,
            user_data={
                'first_name': user_new_first_name,
            },
        )
        assert service_response['status'] == 'Success'

        updated_user_via_service = service_response['content']
        assert updated_user_via_service.first_name == user_new_first_name

    def test_update_user_with_invalid_id(self):
        user_id = self.last_user.id + 1
        user_new_first_name = 'Grzegorz'
        service_response = UserService.update_user(
            pk=user_id,
            user_data={
                'first_name': user_new_first_name,
            },
        )
        assert service_response['status'] == 'Error'

    def test_destroy_user(self):
        number_of_users = User.objects.all().count()

        user_id = self.last_user.id
        service_response = UserService.delete_user(pk=user_id)

        assert service_response['status'] == 'Success'
        assert number_of_users != User.objects.all().count()

    def test_destroy_user_with_invalid_id(self):
        number_of_users = User.objects.all().count()

        user_id = self.last_user.id + 1
        service_response = UserService.delete_user(pk=user_id)

        assert service_response['status'] == 'Error'
        assert number_of_users == User.objects.all().count()
