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
    
    def test_create_user(self):
        
        users = User.objects.all()
        user_data = {
            'email': 'adam01@gmail.com',
            'password': 'Q@werty123!',
            'first_name': 'Adam',
            'last_name': 'Kowalski', 
        }
        created_user = UserService.create_user(user_data)
        assert created_user in users
        assert not created_user.is_active
    
    def test_create_user_with_email_already_used(self):
        
        user_data = {
            'email': 'patrol0990@gmail.com',
            'password': 'Q@werty123!',
            'first_name': 'Adam',
            'last_name': 'Kowalski', 
        }
        created_user = UserService.create_user(user_data)
        assert not created_user
    
    def test_get_all_users(self):
        
        users = list(User.objects.all().order_by('id'))
        users_collected_via_service = list(UserService.get_users())
        
        assert users == users_collected_via_service
    
    def test_get_all_users_with_order_by(self):
        
        users = list(User.objects.all().order_by('-first_name'))
        users_collected_via_service = list(UserService.get_users(order_by='-first_name'))
        
        assert users == users_collected_via_service
    
    def test_get_all_users_with_filters(self):
        
        users = list(User.objects.filter(first_name__in=['Patryk']).order_by('id'))
        users_collected_via_service = list(UserService.get_users(filters={'first_name__in': ['Patryk']}))
        
        assert users == users_collected_via_service
    
    def test_get_user(self):
        
        user_id = self.last_user.id
        user = User.objects.get(id=user_id)
        user_collected_via_service = UserService.get_user(pk=user_id)
        
        assert user == user_collected_via_service
    
    def test_get_user_with_invalid_id(self):
        
        user_id = self.last_user.id + 1
        user_collected_via_service = UserService.get_user(pk=user_id)
        
        assert not user_collected_via_service

    def test_update_user(self):
        user_id = self.last_user.id
        user_new_first_name = 'Grzegorz'
        updated_user_via_service = UserService.update_user(
            pk=user_id,
            user_data={
              'first_name': user_new_first_name,
            },
        )
        assert updated_user_via_service.first_name == user_new_first_name
    
    def test_update_user_with_invalid_id(self):
        user_id = self.last_user.id + 1
        user_new_first_name = 'Grzegorz'
        updated_user_via_service = UserService.update_user(
            pk=user_id,
            user_data={
              'first_name': user_new_first_name,
            },
        )
        assert not updated_user_via_service
    
    def test_destroy_user(self):
        number_of_users = User.objects.all().count()
        
        user_id = self.last_user.id
        is_user_deleted = UserService.delete_user(pk=user_id)
        
        assert is_user_deleted
        assert number_of_users != User.objects.all().count()
    
    def test_destroy_user_with_invalid_id(self):
        number_of_users = User.objects.all().count()
        
        user_id = self.last_user.id + 1
        is_user_deleted = UserService.delete_user(pk=user_id)
        
        assert not is_user_deleted
        assert number_of_users == User.objects.all().count()