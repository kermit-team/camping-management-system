from django.contrib.auth.models import Group


class GroupService:

    def get_groups(self):
        return Group.objects.all()

    def get_group(self, pk):
        try:
            group = Group.objects.get(pk=pk)
            return group
        except Group.DoesNotExist:
            return None

    def create_group(self, group_data):
        try:
            group = Group.objects.create(**group_data)
            return group
        except Exception:
            return None

    def update_group(self, group_data, pk):
        try:      
            if group_data:                    
                Group.objects.filter(pk=pk).update(**group_data)
            group = Group.objects.get(pk=pk)
            return group
        except Group.DoesNotExist:
            return None

    def delete_group(self, pk):
        try:
            group = Group.objects.get(pk=pk)
            group.delete()
            return True
        except Group.DoesNotExist:
            return None