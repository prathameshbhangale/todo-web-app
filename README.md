# Todo Project

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.11 or higher
- `pip` for Python package management

### Setup Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/prathameshbhangale/todo-web-app.git
   cd todo-web-app
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Database Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser** (optional but recommended):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

## API Documentation

### Create New todo item

**Request URL:**
```
{{Base}}/todo/tasks/create/
```

**Request Method:**
`POST`

**Request Body:**
```json
{
  "title": "234",
  "description": "desc bla bla bla..."
}
```

**Authorization:**
- **Username**: `admin`
- **Password**: `admin`

**Response:**
```json
{
  "message": "Task created successfully",
  "task": {
    "id": 5,
    "title": "t1",
    "description": "desc bla bla bla...",
    "timestamp": "2024-12-05T09:10:37.688759Z",
    "due_date": null,
    "status": "OPEN",
    "tags": []
  }
}
```


### Get Todo Items

**Request URL:**
```
{{Base}}/todo/tasks
```

**Authorization:**
- **Username**: `admin`
- **Password**: `admin`

**Response:**
```json
{
    "message": "Tasks retrieved successfully",
    "tasks": [
        {
            "id": 1,
            "title": "Updated Task Title",
            "description": "Updated description of the task",
            "timestamp": "2024-12-03T21:21:57.482397Z",
            "due_date": null,
            "status": "OPEN",
            "tags": []
        }
    ]
}
```
### Get Todo Item by ID

**Request URL:**
```
{{Base}}/todo/task?id=1
```

**Authorization:**
- **Username**: `admin`
- **Password**: `admin`

**Response:**
```json
{
    "message": "Task retrieved successfully",
    "task": {
        "id": 1,
        "title": "Updated Task Title",
        "description": "Updated description of the task",
        "timestamp": "2024-12-03T21:21:57.482397Z",
        "due_date": null,
        "status": "OPEN",
        "tags": []
    }
}
```
### Update Todo Item by ID

**Request URL:**
```
{{Base}}/todo/tasks/update/
```

**Request Method:**
`POST`

**Request Body:**
```json
{
    "pk": 1,
    "title": "Updated Task Title",
    "description": "Updated description of the task"
}
```

**Authorization:**
- **Username**: `admin`
- **Password**: `admin`

**Response:**
```json
{
    "message": "Task updated successfully",
    "task": {
        "id": 1,
        "title": "Updated Task Title",
        "description": "Updated description of the task",
        "timestamp": "2024-12-03T21:21:57.482397Z",
        "due_date": null,
        "status": "OPEN",
        "tags": []
    }
}
```
### Delete Todo Item by ID

**Request URL:**
```
{{Base}}/todo/tasks/delete
```

**Request Method:**
`POST`

**Request Body:**
```json
{
    "pk": 4
}
```

**Authorization:**
- **Username**: `admin`
- **Password**: `admin`

**Response:**
```json
{
    "message": "Task deleted successfully"
}
```
