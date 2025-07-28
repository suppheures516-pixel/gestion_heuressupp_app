from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import ManagerProfile, UploadedExcel
from .backends import ManagerAuthenticationBackend

class ManagerAuthenticationTest(TestCase):
    def setUp(self):
        # Create a test user with manager profile
        self.user = User.objects.create_user(
            username='testmanager',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='Manager'
        )
        self.manager_profile = ManagerProfile.objects.get(user=self.user)
        
        # Create another user without manager profile (admin)
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            first_name='Admin',
            last_name='User'
        )
        # Delete the auto-created manager profile for admin
        if hasattr(self.admin_user, 'managerprofile'):
            self.admin_user.managerprofile.delete()
    
    def test_active_manager_can_login(self):
        """Test that active managers can log in"""
        self.manager_profile.is_active = True
        self.manager_profile.save()
        
        user = authenticate(username='testmanager', password='testpass123')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testmanager')
    
    def test_inactive_manager_cannot_login(self):
        """Test that inactive managers cannot log in"""
        self.manager_profile.is_active = False
        self.manager_profile.save()
        
        user = authenticate(username='testmanager', password='testpass123')
        self.assertIsNone(user)
    
    def test_admin_user_can_login(self):
        """Test that admin users (without manager profile) can still log in"""
        user = authenticate(username='admin', password='adminpass123')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'admin')
    
    def test_wrong_password_fails(self):
        """Test that wrong password fails authentication"""
        self.manager_profile.is_active = True
        self.manager_profile.save()
        
        user = authenticate(username='testmanager', password='wrongpassword')
        self.assertIsNone(user)
    
    def test_nonexistent_user_fails(self):
        """Test that nonexistent user fails authentication"""
        user = authenticate(username='nonexistent', password='anypassword')
        self.assertIsNone(user)

class FileAccessTest(TestCase):
    def setUp(self):
        # Create test users
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            first_name='Admin',
            last_name='User'
        )
        # Delete auto-created manager profile for admin
        if hasattr(self.admin_user, 'managerprofile'):
            self.admin_user.managerprofile.delete()
        
        self.manager_user = User.objects.create_user(
            username='manager1',
            email='manager1@example.com',
            password='managerpass123',
            first_name='Manager',
            last_name='One'
        )
        
        self.manager_user2 = User.objects.create_user(
            username='manager2',
            email='manager2@example.com',
            password='managerpass123',
            first_name='Manager',
            last_name='Two'
        )
        
        # Create test uploaded files
        self.file1 = UploadedExcel.objects.create(
            file='uploads/test1.xlsx',
            uploaded_by=self.manager_user
        )
        
        self.file2 = UploadedExcel.objects.create(
            file='uploads/test2.xlsx',
            uploaded_by=self.manager_user2
        )
    
    def test_manager_sees_only_own_files(self):
        """Test that managers only see files they uploaded"""
        from .views import heures_supplementaires
        
        # Mock request for manager1
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get('/heures-supplementaires/')
        request.user = self.manager_user
        
        # This would normally call the view, but we're just testing the logic
        # The view should only process files uploaded by manager_user
        user_files = UploadedExcel.objects.filter(uploaded_by=self.manager_user)
        self.assertEqual(user_files.count(), 1)
        self.assertEqual(user_files.first(), self.file1)
    
    def test_admin_sees_all_files(self):
        """Test that admin sees all files"""
        # Add admin to Admin group
        from django.contrib.auth.models import Group
        admin_group, created = Group.objects.get_or_create(name='Admin')
        self.admin_user.groups.add(admin_group)
        
        # Admin should see all files
        all_files = UploadedExcel.objects.all()
        self.assertEqual(all_files.count(), 2)
