```markdown
# Django ERP Backend with Custom User Model

## Overview

This project is an ERP backend built with Django and Django REST Framework, featuring a custom user model `Employee` with role-based access control. The system supports three user roles:

- **Admin**: Full permissions to add, update, or delete any user.
- **Manager**: Can add, update, or delete employees only within their own department.
- **Employee**: Can view and update their own profile only.

The system manages Departments, Employees, and Projects with secure JWT authentication and detailed API endpoints, all implemented using APIViews.

---

## Features

- Custom user model inheriting from `AbstractUser` with additional fields: `department`, `salary`, `role`.
- Role choices of `Admin`, `Manager`, and `Employee`.
- Automatic assignment of `Admin` role for superusers created via CLI.
- JWT authentication with `djangorestframework-simplejwt`.
- Role-based permissions handled via custom permission classes.
- APIViews for CRUD operations and reports.
- Departments and Projects management.
- Validation to restrict managers within their departments.
- Password hashing with `set_password()` on user creation and update.
- Clear permission enforcement preventing unauthorized access.

---

## Setup Instructions

### 1. Clone repository

```
git clone <repository-url>
cd <repository-directory>
```

### 2. Create Python virtual environment and activate

```
python -m venv env
# Linux/Mac
source env/bin/activate
# Windows
env\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Configure `settings.py`

- Ensure you have:

```
AUTH_USER_MODEL = 'ERP.Employee'

INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework_simplejwt',
    'ERP',
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
```

### 5. Apply migrations

```
python manage.py makemigrations
python manage.py migrate
```

### 6. Create superuser

```
python manage.py createsuperuser
```

- The superuser will be assigned the `Admin` role automatically.

### 7. Run development server

```
python manage.py runserver
```

---

## Usage

### Authentication

- Obtain JWT token:

```
POST /token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

- Use in requests:

```
Authorization: Bearer <access_token>
```

### API Endpoints

| Endpoint                             | Methods         | Description                                       |
|------------------------------------|-----------------|-------------------------------------------------|
| `/employees/`                      | GET, POST       | List/create employees (role-restricted)         |
| `/employees/<id>/`                 | GET, PUT, DELETE| Retrieve/update/delete a single employee         |
| `/departments/`                   | GET, POST       | List/create departments                           |
| `/departments/<id>/`              | GET, PUT, DELETE| Retrieve/update/delete a department               |
| `/projects/`                     | GET, POST       | List/create projects                              |
| `/projects/<id>/`                | GET, PUT, DELETE| Retrieve/update/delete a project                   |
| `/reports/employees-by-department/` | GET          | List employees grouped by department              |
| `/reports/salary-cost-per-department/` | GET        | Salary cost summarized by department              |
| `/reports/active-projects/`        | GET           | List of active projects                           |

---

## Important Details

- Password is **required on creation** and optional on update.
- Managers cannot assign Admin roles or employees outside their departments.
- Employees can only view and update their own profiles.
- Admins have full access to all resources.
- Passwords are handled securely using Django’s `set_password()` method.
- The project uses APIViews with custom permissions for precise role-based control.

---

## Project Structure Highlights

- `ERP/models.py` - Custom `Employee`, `Department`, `Project` models and custom user manager.
- `ERP/serializers.py` - DRF serializers with validation.
- `ERP/permissions.py` - Custom permission classes enforcing roles.
- `ERP/views.py` - APIViews implementing business logic and CRUD.
- `ERP/urls.py` - URL routing mapped to APIViews.
- `settings.py` - Configuration for custom user model and REST framework.

---

## Admin Panel

To manage users, departments, and projects via the Django admin:

- Register your models in `ERP/admin.py`.
- Customize admin forms if needed to display and manage roles and departments.

---

## Troubleshooting

- If you cannot authenticate, verify password is set correctly with `set_password()`.
- Check user roles in the database if permission errors occur.
- Superuser role must be `Admin` for full control.
- Ensure you include JWT tokens with API requests under `Authorization` header.

---

## Contribution

- Fork the repository and create feature branches.
- Follow existing code style for consistency.
- Submit pull requests for review and merge.

---

Feel free to reach out for questions or further customization!

---

This README should help you get started quickly and understand the full project capabilities and usage.

[1](https://gitlab.com/thorgate-public/django-project-template/-/blob/master/README.md)
[2](https://docs.readme.com/main/docs/python-django-api-metrics)
[3](https://cubettech.com/resources/blog/the-essential-readme-file-elevating-your-project-with-a-comprehensive-document/)
[4](https://bulldogjob.com/readme/how-to-write-a-good-readme-for-your-github-project)
[5](https://www.drupal.org/docs/develop/managing-a-drupalorg-theme-module-or-distribution-project/documenting-your-project/readmemd-template)
[6](https://forum.djangoproject.com/t/structuring-large-complex-django-projects-and-using-a-services-layer-in-django-projects/1487)
[7](https://www.youtube.com/watch?v=m3nYd_IFZuU)
[8](https://www.upgrad.com/blog/django-projects-on-github/)
[9](https://themeselection.com/django-project-ideas/)