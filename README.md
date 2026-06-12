# Task Manager API — Assessment Submission

Hi! I built this Task Manager REST API as part of the assessment. This README explains what I built, how to set it up, and the decisions I made while building it.

---

## What This Project Does

This is a **REST API** that lets users:
- Register and log in securely using JWT tokens
- Create, view, update, and delete their personal tasks
- Search and filter tasks by title, description, or status

The system has two roles — **Admin** and **User**:
- **Admin** can see and manage every task in the system
- **User** can only see and manage tasks they personally created

---

## Tech Stack

| What | Which |
|---|---|
| Language | Python 3.9+ |
| Framework | Django 5.2 |
| API Layer | Django REST Framework |
| Authentication | JWT via SimpleJWT (RS256 algorithm) |
| Database | SQLite |
| Environment Config | django-environ |
| Cryptography | cryptography==41.0.7 |

---

## Folder Structure

## 📂 Project Directory Structure

```text
TaskManager/             # Main Root Repository
│
├── TaskEnv/                 # Isolated Python Virtual Environment (Ignored)
├── .gitignore               # Multi-layer path exclusion configuration
├── README.md                # Project documentation and setup manuals
└── TaskManager/             # Core Project Directory
    ├── manage.py            # Django Management script
    ├── TaskManager/         # Configuration App (settings.py, urls.py)
    ├── authentication/      # Authentication App (JWT Login, Registration)
    └── tasks/               # Core Business App (Models, Views, Serializers)


---

## Why I Built It This Way

### JWT with RS256 Algorithm
I used **RS256 asymmetric signing** instead of the default HS256:
- **Private key** signs and creates the token at login
- **Public key** verifies the token on every request
- No database hit needed to validate a token — fully stateless
- More secure because even if the public key is exposed, nobody can create fake tokens without the private key

### UUID for Task IDs
Every task gets a random UUID like `a3f1c2d4-9b2e-4f1a-8c3d-...` instead of `1, 2, 3`.
This prevents **IDOR attacks** — where someone guesses `/tasks/2/` to access another user's task.

### Group-Based Roles (Admin / User)
I used Django's built-in **Groups** to manage roles:
- Every registered user is automatically added to the `User` group
- Admins are manually promoted to the `Admin` group
- `is_admin()` in `permissions.py` checks the group at the view level

### N+1 Query Prevention
All task queries use `.select_related("owner")` so Django fetches tasks and their owners in **one single JOIN query** instead of firing a separate query per task.

### Validators vs Serializers — Kept Separate
- `validators.py` → validates **incoming data** (POST, PUT requests)
- `serializer.py` → formats **outgoing data** (GET responses)

This keeps each file focused on one job and makes the code easier to read.

### Consistent Response Format
Every endpoint returns the same JSON structure:
```json
{
    "success": true,
    "message": "...",
    "data": {}
}
```

### Pagination + Search + Filter
- Tasks are paginated — 10 per page by default
- Search by title or description using `?search=keyword`
- Filter by status using `?status=true` or `?status=false`

### Database Indexes on Task Model
I added indexes on `id`, `created_at`, and `updated_at` fields. This makes lookups and ordering faster as the data grows.

---

## How to Run This Project

### Step 1 — Go into the project folder

```bash
cd D:\CodeSis\TaskManager
```

### Step 2 — Activate virtual environment

**Windows:**
```bash
..\TaskEnv\Scripts\activate
```

**Mac / Linux:**
```bash
source ../TaskEnv/bin/activate
```

### Step 3 — Install all packages

```bash
pip install -r requirements.txt
```

### Step 4 — Create the `.env` file

Create a file named `.env` inside the `TaskManager\` folder:

Generate a strong SECRET_KEY with this command:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 5 — Add RSA Keys

Go to any RSA key generator website and generate a **4096-bit** key pair.

Save the **Private Key** as `private_key.pem` inside `TaskManager\`:

The `settings.py` reads them directly — no conversion needed:
```python
JWT_PRIVATE_KEY = open(os.path.join(BASE_DIR, 'private_key.pem')).read()
JWT_PUBLIC_KEY  = open(os.path.join(BASE_DIR, 'public_key.pem')).read()
```

### Step 6 — Run migrations

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

### Step 7 — Create Admin and User groups

This step is **required before anyone registers**. Without it, registration returns a 500 error.

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import Group
Group.objects.get_or_create(name='User')
Group.objects.get_or_create(name='Admin')
print("Groups created.")
exit()
```

### Step 8 — Start the server

```bash
python manage.py runserver
```

API is live at: `http://127.0.0.1:8000`

---

## Promoting a User to Admin

After a user registers, promote them to Admin like this:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User, Group
user = User.objects.get(username='their_username')
user.groups.clear()
user.groups.add(Group.objects.get(name='Admin'))
print(f"{user.username} is now Admin.")
exit()
```

---

## All API Endpoints

### Authentication — `/api/auth/`

| Method | Endpoint | Login Required | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | No | Create a new account |
| POST | `/api/auth/login/` | No | Login and receive JWT tokens |
| POST | `/api/auth/refresh/` | No | Get a new access token |

### Tasks — `/api/`

| Method | Endpoint | Login Required | Who | Description |
|---|---|---|---|---|
| GET | `/api/tasks/` | Yes | Admin | Get ALL tasks from all users |
| GET | `/api/tasks/` | Yes | User | Get only MY tasks |
| GET | `/api/tasks/?search=report` | Yes | Both | Search by title or description |
| GET | `/api/tasks/?status=true` | Yes | Both | Filter completed tasks |
| GET | `/api/tasks/?status=false` | Yes | Both | Filter incomplete tasks |
| GET | `/api/tasks/?page=2` | Yes | Both | Go to page 2 |
| POST | `/api/tasks/` | Yes | Both | Create a new task |
| GET | `/api/tasks-detail/<uuid>/` | Yes | Admin | Get any task by ID |
| GET | `/api/tasks-detail/<uuid>/` | Yes | User | Get my task by ID only |
| PUT | `/api/tasks-detail/<uuid>/` | Yes | Admin/Owner | Update a task |
| DELETE | `/api/tasks-detail/<uuid>/` | Yes | Admin/Owner | Delete a task |

---

## Request Body Examples

### Register
```json
{
    "username": "alice",
    "email": "alice@example.com",
    "password": "mypassword123"
}
```

### Login
```json
{
    "username": "alice",
    "password": "mypassword123"
}
```

### Refresh Token
```json
{
    "refresh": "your-refresh-token-here"
}
```

### Create Task
```json
{
    "title": "Finish the assessment",
    "description": "Complete all endpoints and write README",
    "status": false
}
```

### Update Task — mark as complete
```json
{
    "status": true
}
```

### Update Task — change title or description
```json
{
    "title": "Updated title",
    "description": "Updated description"
}
```

---

## Response Examples

### Register — success
```json
{
    "success": true,
    "message": "User registered successfully.",
    "data": {
        "username": "alice",
        "email": "alice@example.com",
        "role": "User"
    }
}
```

### Login — success
```json
{
    "success": true,
    "message": "Login successful.",
    "data": {
        "user": "alice",
        "tokens": {
            "refresh": "eyJhbGciOiJSUzI1NiJ9...",
            "access": "eyJhbGciOiJSUzI1NiJ9...",
            "expiry_time": 1719999999000
        }
    }
}
```

### Task list — paginated
```json
{
    "success": true,
    "message": "Successfully Fetched Tasks.",
    "data": {
        "page": 1,
        "next_page": "http://127.0.0.1:8000/api/tasks/?page=2",
        "prev_page": null,
        "count": 15,
        "rows_per_page": 10,
        "results": [
            {
                "id": "a3f1c2d4-9b2e-4f1a-8c3d-1e2f3a4b5c6d",
                "owner": "alice",
                "title": "Finish the assessment",
                "description": "Complete all endpoints",
                "status": false,
                "created_at": "2025-01-01T10:00:00Z"
            }
        ]
    }
}
```

### Task not found
```json
{
    "success": false,
    "message": "Task not Found!",
    "errors": "Task id not found or invalid Task Id."
}
```

### Wrong password
```json
{
    "success": false,
    "message": "Invalid credentials.",
    "errors": "Password is incorrect."
}
```

### Validation error
```json
{
    "success": false,
    "message": "Something went wrong while creating the Task.",
    "errors": "Task title is required."
}
```

### Username already taken
```json
{
    "success": false,
    "message": "Username already exists.",
    "errors": "Username already exists."
}
```

