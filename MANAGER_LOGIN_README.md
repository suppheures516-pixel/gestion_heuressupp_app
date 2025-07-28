# Manager Login System

This document explains how the manager login system works in the Django Excel application.

## Overview

The system allows managers to log in using credentials provided by administrators. Managers can only log in if their account is marked as active in the system.

## Features

### 1. Manager Authentication Backend
- Custom authentication backend that checks if a manager's account is active
- Located in `pointage/backends.py`
- Only allows login for managers with `is_active=True` in their `ManagerProfile`
- Admin users (without manager profiles) can still log in normally

### 2. Manager Management
- Admins can create, edit, and manage manager accounts
- Each manager has a profile with additional information (phone, department)
- Managers can be activated/deactivated without deleting their account
- Password reset functionality for admins

### 3. Login Interface
- Custom login page with improved UI
- Clear error messages for inactive accounts
- Responsive design with Bootstrap styling

## How It Works

### Manager Creation
1. Admin goes to `/managers/` to view the manager list
2. Clicks "Add Manager" to create a new manager account
3. Fills in the required information (username, email, password, etc.)
4. The system automatically creates a `ManagerProfile` for the new user
5. The manager account is created with `is_active=True` by default

### Manager Login
1. Manager visits `/accounts/login/`
2. Enters their username and password
3. The system checks:
   - If the user exists
   - If the password is correct
   - If the user has a manager profile
   - If the manager profile is active
4. If all checks pass, the manager is logged in and redirected to the home page
5. If the account is inactive, a clear error message is shown

### File Access Control
- **Manager Access**: Managers can only see overtime hours from Excel files they uploaded
- **Admin Access**: Admins can see overtime hours from all uploaded files
- **Data Isolation**: Each manager's data is completely isolated from other managers
- **Secure Processing**: Only authorized files are processed for overtime calculations

### Account Management
- **Activate/Deactivate**: Admins can toggle manager accounts on/off
- **Password Reset**: Admins can reset manager passwords
- **Edit Profile**: Update manager information (name, email, phone, department)
- **Delete Account**: Remove manager accounts completely

## Security Features

1. **Account Status Check**: Inactive managers cannot log in
2. **Password Validation**: Standard Django password validation
3. **Permission-Based Access**: Only admins can manage manager accounts
4. **File Access Control**: Managers can only see overtime hours from files they uploaded
5. **Session Management**: Standard Django session handling

## File Structure

```
pointage/
├── backends.py              # Custom authentication backend
├── models.py                # ManagerProfile model
├── forms.py                 # Manager creation/editing forms
├── views.py                 # Manager management views
├── urls.py                  # URL routing
└── templates/
    ├── registration/
    │   └── login.html       # Custom login page
    └── pointage/
        ├── manager_list.html           # Manager management interface
        ├── manager_form.html           # Create/edit manager form
        └── manager_password_reset.html # Password reset form
```

## Testing

The system includes comprehensive tests in `pointage/tests.py`:

- `test_active_manager_can_login`: Verifies active managers can log in
- `test_inactive_manager_cannot_login`: Verifies inactive managers cannot log in
- `test_admin_user_can_login`: Verifies admin users can still log in
- `test_wrong_password_fails`: Verifies password validation
- `test_nonexistent_user_fails`: Verifies non-existent user handling

Run tests with:
```bash
python manage.py test pointage.tests.ManagerAuthenticationTest
```

## Usage Instructions

### For Administrators

1. **Create a Manager Account**:
   - Go to `/managers/`
   - Click "Add Manager"
   - Fill in the required information
   - Set a secure password
   - Save the account

2. **Provide Login Credentials**:
   - Share the username and password with the manager
   - Inform them to visit `/accounts/login/`

3. **Manage Accounts**:
   - Use the manager list to view all accounts
   - Toggle account status (active/inactive)
   - Reset passwords when needed
   - Edit manager information

### For Managers

1. **First Login**:
   - Visit `/accounts/login/`
   - Enter the username and password provided by admin
   - Click "Se connecter"

2. **If Login Fails**:
   - Check username and password spelling
   - Contact administrator if account is inactive
   - Contact administrator for password reset

## Troubleshooting

### Common Issues

1. **Manager cannot log in**:
   - Check if account is active in manager list
   - Verify username and password
   - Check if manager profile exists

2. **Admin cannot access manager management**:
   - Ensure user has admin privileges
   - Check if user has the required permissions

3. **Authentication errors**:
   - Check Django settings for authentication backend configuration
   - Verify database migrations are applied

### Error Messages

- **"Votre compte manager a été désactivé"**: Account is inactive, contact admin
- **"Nom d'utilisateur ou mot de passe invalide"**: Incorrect credentials
- **"Permission denied"**: User lacks required permissions

## Configuration

The authentication backend is configured in `settings.py`:

```python
AUTHENTICATION_BACKENDS = [
    'pointage.backends.ManagerAuthenticationBackend',
]
```

This ensures only the custom authentication logic is used for all login attempts. 