from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ('can_manage_managers', 'Can add, edit, and delete managers'),
        ]

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

@receiver(post_save, sender=User)
def create_or_update_manager_profile(sender, instance, created, **kwargs):
    if created or not hasattr(instance, 'managerprofile'):
        ManagerProfile.objects.create(user=instance)
    instance.managerprofile.save()

class UploadedExcel(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name
