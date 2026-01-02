# Mini CRM Application

A full-stack CRM (Customer Relationship Management) application built with Django and Vue.js.

## Tech Stack

### Backend
- **Django 4.2.7** - Python web framework
- **Django REST Framework** - REST API toolkit
- **SQLite** - Database
- **Token Authentication** - Secure API authentication

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vuetify 3** - Material Design component library
- **Vue Router** - Client-side routing
- **Axios** - HTTP client
- **Vite** - Build tool and dev server

## Features

- User authentication (login/logout)
- Dashboard with analytics and statistics
- Contact management (CRUD operations)
- Company management (CRUD operations)
- Deal tracking with pipeline stages
- Task management with priorities
- Beautiful navy blue themed UI
- Responsive design with Material Design components

## Project Structure

```
interview/
├── backend/               # Django backend
│   ├── config/           # Django settings
│   ├── tasks/            # CRM app (models, views, serializers)
│   ├── manage.py
│   └── db.sqlite3
│
└── frontend/             # Vue.js frontend
    ├── src/
    │   ├── assets/       # CSS and static files
    │   ├── components/   # Vue components
    │   ├── plugins/      # Vuetify configuration
    │   ├── router/       # Vue Router setup
    │   ├── services/     # API service layer
    │   ├── views/        # Page components
    │   ├── App.vue       # Root component
    │   └── main.js       # Entry point
    ├── index.html
    ├── package.json
    └── vite.config.js
```

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Option 1: Docker (Recommended)

Run both backend and frontend with a single command:

```bash
docker compose up
```

Access the application:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Django Admin: http://localhost:8000/admin

To stop the containers:
```bash
docker compose down
```

To rebuild after changes:
```bash
docker compose up --build
```

### Option 2: Manual Setup

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # Create admin user
python manage.py runserver
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Usage

1. Navigate to http://localhost:5173
2. Log in with one of these accounts:
   - **Admin:** username=`admin`, password=`admin123`
   - **Manager:** username=`john.smith`, password=`password123`
   - **Sales Rep:** username=`sarah.johnson`, password=`password123`
   - **Viewer:** username=`viewer.user`, password=`password123`
3. Explore the CRM features:
   - View dashboard statistics with AI insights
   - Manage contacts, companies, deals, and tasks
   - View team performance and AI recommendations
   - Test role-based access control

## API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

### Dashboard
- `GET /api/dashboard/stats/` - Get dashboard statistics

### Companies
- `GET /api/companies/` - List all companies
- `POST /api/companies/` - Create a new company
- `GET /api/companies/:id/` - Get company details
- `PUT /api/companies/:id/` - Update a company
- `DELETE /api/companies/:id/` - Delete a company

### Contacts
- `GET /api/contacts/` - List all contacts
- `POST /api/contacts/` - Create a new contact
- `GET /api/contacts/:id/` - Get contact details
- `PUT /api/contacts/:id/` - Update a contact
- `DELETE /api/contacts/:id/` - Delete a contact

### Deals
- `GET /api/deals/` - List all deals
- `POST /api/deals/` - Create a new deal
- `GET /api/deals/:id/` - Get deal details
- `PUT /api/deals/:id/` - Update a deal
- `DELETE /api/deals/:id/` - Delete a deal

### Tasks
- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/:id/` - Get task details
- `PUT /api/tasks/:id/` - Update a task
- `DELETE /api/tasks/:id/` - Delete a task

## Color Scheme

The application uses a professional navy blue color scheme:
- **Primary:** #001f3f (Navy Blue)
- **Secondary:** #0074D9 (Lighter Blue)
- **Accent:** #39CCCC (Teal)
- **Background:** #f5f7fa (Light Gray)

## Database Models

### Company
- name, industry, website, phone, address
- created_at, updated_at
- created_by (User)

### Contact
- first_name, last_name, email, phone
- position, company (FK)
- created_at, updated_at
- created_by (User)

### Deal
- title, amount, stage
- company (FK), expected_close_date
- created_at, updated_at
- assigned_to (User)

### Task
- title, description, status, priority
- due_date, contact (FK), deal (FK)
- created_at, updated_at
- assigned_to (User)

## Development Notes

- No TypeScript - Pure JavaScript throughout
- Token-based authentication with Django authtoken
- CORS configured for local development
- Vuetify 3 Material Design components
- RESTful API architecture
- Vue Router with navigation guards

## License

This project is created for interview purposes.
