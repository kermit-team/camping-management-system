from account.models import User


class UserService:

    def get_users(self):
        return User.objects.all()

    def get_user(self, pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except User.DoesNotExist:
            return None

    def create_user(self, user_data):
        try:
            groups = user_data.pop('groups', None)
            user = User.objects.create_user(**user_data)
            if groups:
                user.groups.set(groups)
            return user
        except Exception:
            return None

    def update_user(self, user_data, pk):
        try:
            password = user_data.pop('password', None)
            groups = user_data.pop('groups', None)
            user = User.objects.get(pk=pk)
            
            if password:
                user.set_password(password)
                user.save()
            if groups:
                user.groups.set(groups)
            
            if user_data:                    
                User.objects.filter(pk=pk).update(**user_data)
            user = User.objects.get(pk=pk)
            return user
        except User.DoesNotExist:
            return None

    def delete_user(self, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return True
        except User.DoesNotExist:
            return None