# Blog API 📝

A fully-featured Blog API built with **FastAPI** and **PostgreSQL**, complete with user authentication, blog management, comments system, and an admin panel for content moderation.

---

## ✨ Features

- ✅ **User Authentication** - JWT-based registration and login
- ✅ **Blog Management** - Create, read, update, delete blog posts
- ✅ **Comments System** - Add comments to blogs with username tracking
- ✅ **Admin Panel** - Manage users and blogs
  - View all users and blogs
  - Delete inappropriate users and blogs
  - Update user roles and information
  - Edit blog content
- ✅ **Role-Based Access Control** - Admin-only endpoints for content moderation
- ✅ **Password Security** - bcrypt password hashing
- ✅ **JWT Tokens** - 30-minute expiring access tokens
- ✅ **Database Migrations** - Alembic for schema management
- ✅ **OpenAPI Documentation** - Auto-generated Swagger UI with authentication

---

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.136.1
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Password Hashing**: bcrypt
- **Authentication**: JWT (PyJWT)
- **Migration Tool**: Alembic
- **Server**: Uvicorn
- **Validation**: Pydantic 2.13.3

---

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip or conda

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Emon-X/BlogApi.git
cd BlogApi
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
DATABASE_URL = "postgresql://username:password@localhost:5432/mydb"
SECRET_KEY = "your-super-secret-key-with-more-than-32-bytes-length"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ADMIN_USERNAME = "AdminUser"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "securepassword"
```

### 5. Run Database Migrations
```bash
alembic upgrade head
```

### 6. Start the Server
```bash
python main.py
```

The API will be available at `http://localhost:8000`

---

## 📚 API Endpoints

### Authentication (`/auth`)

#### Register User
```http
POST /auth/Register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123",
  "confirm_password": "securepass123"
}

Response: {"Bearer Token : ": "eyJ0eXAiOiJKV1QiLCJhbGc..."}
```

#### Login
```http
POST /auth/Login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepass123"
}

Response: {"Bearer Token : ": "eyJ0eXAiOiJKV1QiLCJhbGc..."}
```

---

### Blog Management (`/blog`) 🔐 *Requires Authentication*

#### Create Blog Post
```http
POST /blog/Create
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "My First Blog Post",
  "description": "This is the content of my blog post"
}
```

#### View User's Blogs
```http
GET /blog/View
Authorization: Bearer <token>

Response: [
  {
    "user_name": "john_doe",
    "user_email": "john@example.com",
    "title": "My First Blog Post",
    "description": "This is the content of my blog post"
  }
]
```

#### Read Specific Blog
```http
GET /blog/Read/{blog_id}
Authorization: Bearer <token>
```

#### Edit Blog
```http
PUT /blog/Edit/{blog_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "Updated description"
}
```

#### Delete Blog
```http
DELETE /blog/Delete/{blog_id}
Authorization: Bearer <token>
```

#### Add Comment
```http
POST /blog/Comment?blog_id={blog_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "comment": "Great blog post!"
}

Response: {
  "id": 1,
  "content": "Great blog post!",
  "username": "john_doe",
  "user_id": 1,
  "blog_id": 1,
  "created_at": "2026-05-08T12:00:00"
}
```

---

### Admin Panel (`/admin`) 🔐 *Requires Admin Role*

#### Get All Users
```http
GET /admin/users
Authorization: Bearer <admin_token>

Response: [
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_active": true,
    "is_admin": false,
    "created_at": "2026-05-08T10:00:00"
  }
]
```

#### Get All Blogs
```http
GET /admin/blogs
Authorization: Bearer <admin_token>

Response: [
  {
    "id": 1,
    "title": "My First Blog",
    "description": "Content here",
    "username": "john_doe",
    "user_id": 1,
    "created_at": "2026-05-08T10:00:00",
    "updated_at": "2026-05-08T10:00:00",
    "comments": [...]
  }
]
```

#### Delete User
```http
DELETE /admin/delete_user/{user_id}
Authorization: Bearer <admin_token>
```

#### Update User
```http
PUT /admin/update_user/{user_id}
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "username": "new_username",
  "email": "newemail@example.com",
  "is_active": true,
  "is_admin": false
}
```

#### Delete Blog
```http
DELETE /admin/delete_blog/{blog_id}
Authorization: Bearer <admin_token>
```

#### Update Blog
```http
PUT /admin/update_blog/{blog_id}
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "Updated content"
}
```

---

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR UNIQUE NOT NULL,
  email VARCHAR UNIQUE NOT NULL,
  password VARCHAR NOT NULL,
  is_active BOOLEAN DEFAULT true,
  is_admin BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Blogs Table
```sql
CREATE TABLE blogs (
  id SERIAL PRIMARY KEY,
  username VARCHAR NOT NULL,
  user_id INTEGER FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(100) NOT NULL,
  description TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Comments Table
```sql
CREATE TABLE comments (
  id SERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  username VARCHAR,
  user_id INTEGER FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE,
  blog_id INTEGER FOREIGN KEY REFERENCES blogs(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔐 Authentication

### How JWT Works

1. **Register/Login**: User provides credentials
2. **Token Generation**: Server returns JWT token valid for 30 minutes
3. **Protected Requests**: Include token in Authorization header
   ```
   Authorization: Bearer <your_token_here>
   ```
4. **Token Validation**: Server verifies token signature and expiration

### Token Structure
```
Header: {"typ": "JWT", "alg": "HS256"}
Payload: {
  "username": "john_doe",
  "email": "john@example.com",
  "exp": 1234567890
}
Signature: HMACSHA256(base64Header.base64Payload, SECRET_KEY)
```

---

## 👨‍💼 Admin Panel Usage

### Default Admin User
The admin user is automatically created on first app startup using environment variables:
- **Email**: `mdemon@gmail.com` (from `.env`)
- **Password**: `admin123` (from `.env`)

### Making Someone an Admin

1. Login as admin
2. Call `PUT /admin/update_user/{user_id}` with:
   ```json
   {
     "is_admin": true
   }
   ```

### Admin Permissions
- ✅ View all users
- ✅ View all blogs
- ✅ Delete any user
- ✅ Delete any blog
- ✅ Update user information and roles
- ✅ Update blog content

---

## 📁 Project Structure

```
BlogApi/
├── main.py                          # Entry point
├── requirements.txt                 # Python dependencies
├── .env                            # Environment configuration
├── README.md                       # This file
├── alembic.ini                     # Alembic configuration
├── alembic/
│   ├── versions/                   # Migration files
│   └── env.py                      # Alembic environment setup
├── app/
│   ├── __init__.py
│   ├── app.py                      # FastAPI app setup
│   ├── dependencis.py              # Dependencies (old auth)
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py                   # Database configuration
│   │   ├── schemes/                # SQLAlchemy models
│   │   │   ├── user.py             # User & Comment models
│   │   │   └── blog.py             # Blog model
│   │   └── repository/             # Data access layer
│   │       ├── base.py             # Base repository
│   │       └── user.py             # User repository
│   ├── models/                     # Pydantic models
│   │   ├── auth.py                 # Auth request/response models
│   │   ├── blogs.py                # Blog request/response models
│   │   └── admin.py                # Admin response models
│   ├── routes/                     # API endpoints
│   │   ├── auth.py                 # Authentication routes
│   │   ├── blog.py                 # Blog management routes
│   │   └── admin.py                # Admin panel routes
│   ├── security/                   # Security utilities
│   │   ├── auth.py                 # JWT token handling
│   │   └── hash.py                 # Password hashing
│   ├── services/                   # Business logic
│   │   └── admin.py                # Admin user creation
│   └── utils/                      # Utilities
│       ├── protected_routes.py      # JWT validation
│       └── admin_check.py           # Admin role validation
```

---

## 🔄 Database Migrations

### View Migration History
```bash
alembic current
```

### Create New Migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback Migrations
```bash
alembic downgrade -1  # Rollback one migration
```

---

## 🐛 Troubleshooting

### Port 8000 Already in Use
```bash
# Find and kill process
lsof -i :8000 | awk 'NR>1 {print $2}' | xargs kill -9
```

### Database Connection Error
- Verify PostgreSQL is running
- Check DATABASE_URL in .env
- Ensure database exists

### Token Expired
- Generate a new token by logging in again
- Token expires after 30 minutes (configurable in .env)

### Admin User Not Created
- Check ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD in .env
- Restart the application

---

## 📖 API Documentation

Once the server is running, access interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Emon** - [@emon-x](https://github.com/emon-x)

---

## 🙏 Acknowledgments

- FastAPI documentation and community
- SQLAlchemy ORM
- PostgreSQL database
- JWT authentication standards

---

## 📞 Support

For issues and questions, please open an issue on the GitHub repository.

Happy blogging! 🎉
