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


# API Testing Documentation

This project contains API tests for a TODO web application. The tests cover the `Task` model and its associated views. Below is a detailed description of the test cases and their functionalities.


---

## Test Frameworks and Tools
- **Django REST Framework (DRF)**
- **Unit Testing Framework:** `APITestCase`
- **API Testing Tools:** `APIRequestFactory`, `force_authenticate`

---


# Task Management API Testing

This project contains comprehensive test cases for the **Task Management API**, covering **unit**, **integration**, and **end-to-end (E2E)** testing using **Django Rest Framework (DRF)**'s `APITestCase`.

---

## **Table of Contents**
1. [Overview](#overview)
2. [Testing Strategy](#testing-strategy)
3. [Test Cases](#test-cases)
4. [Running Tests](#running-tests)

---

## **Overview**
The Task Management API allows users to perform CRUD operations on tasks. This project ensures that the API behaves as expected under various scenarios, such as authenticated/unauthenticated access, valid/invalid inputs, and edge cases.

The key features of the test suite include:
- **Unit Tests**: Validate individual API views for specific behaviors.
- **Integration Tests**: Test how different API views interact with each other.
- **E2E Tests**: Simulate a complete workflow (e.g., creating, retrieving, updating, and deleting a task) to verify overall system behavior.

---

## **Testing Strategy**
### **1. Unit Testing**
Focused on testing individual API views like `TaskCreateView`, `TaskListView`, `TaskDetailView`, `TaskUpdateView`, and `TaskDeleteView`.
- Verifies success/failure conditions for each view.
- Includes edge cases like missing fields, invalid IDs, and unauthorized requests.

### **2. Integration Testing**
Ensures that API views interact properly when performing related operations. For example:
- Retrieving a task list after creating multiple tasks.
- Attempting to delete a task that was just created.

### **3. End-to-End Testing**
Simulates real-world scenarios involving multiple API endpoints to validate the workflow. For example:
1. **Create** a task.
2. **Retrieve** the list of tasks.
3. **Update** the created task.
4. **Delete** the task and verify its removal.

---

## **Test Cases**
### **E2E Tests**
Located in `TaskE2ETests`:
- `test_create_task`: Simulates creating a task.
- `test_retrieve_task_list`: Retrieves all tasks after creation.
- `test_update_task`: Updates the created task and verifies changes.
- `test_delete_task`: Deletes the created task and ensures it is removed.

### **Unit Tests**
Located in:
- `TaskCreateViewTests`
- `TaskDetailViewTests`
- `TaskListViewTests`
- `TaskUpdateViewTests`
- `TaskDeleteViewTests`

Each class contains tests for:
- Successful operations (e.g., creating a task).
- Failure cases (e.g., invalid data or unauthorized access).

---

## **Running Tests**
To run the tests, execute the following command in your project directory:

```bash
python manage.py test
```

output:
```bash
Ran 21 tests in 15.608s

OK
Destroying test database for alias 'default'...
```