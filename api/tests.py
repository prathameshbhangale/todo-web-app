from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from api.models import Task
from api.views import TaskCreateView, TaskDetailView, TaskListView, TaskUpdateView

class TaskE2ETests(APITestCase):
    def setUp(self):
        """Setup a test user and factory."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.factory = APIRequestFactory()

    def test_create_task(self):
        """Step 1: Create a task."""
        view = TaskCreateView.as_view()
        data = {
            'title': 'E2E Test Task',
            'description': 'This is an end-to-end test task.'
        }
        request = self.factory.post('/todo/tasks/', data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request)

        print("Response Status Code (Create):", response.status_code)
        print("Response Data (Create):", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['task']['title'], 'E2E Test Task')
        self.task_id = response.data['task']['id']

    def test_retrieve_task_list(self):
        """Step 2: Retrieve the list of tasks."""
        # Ensure a task exists
        self.test_create_task()

        view = TaskListView.as_view()
        request = self.factory.get('/todo/tasks/', format='json')
        force_authenticate(request, user=self.user)
        response = view(request)

        print("Response Status Code (Retrieve):", response.status_code)
        print("Response Data (Retrieve):", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(task['id'] == self.task_id for task in response.data['tasks']))

    def test_update_task(self):
        """Step 3: Update a task."""
        # Ensure a task exists
        self.test_create_task()

        view = TaskUpdateView.as_view()
        data = {
            'pk': self.task_id,
            'title': 'Updated E2E Test Task',
            'description': 'Updated description.'
        }
        request = self.factory.post('/todo/tasks/update/', data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request)

        print("Response Status Code (Update):", response.status_code)
        print("Response Data (Update):", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['task']['title'], 'Updated E2E Test Task')

    def test_delete_task(self):
        """Step 4: Delete a task."""
        # Ensure a task exists
        self.test_create_task()

        view = TaskDeleteView.as_view()
        data = {'pk': self.task_id}
        request = self.factory.delete('/todo/tasks/delete/', data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request)

        print("Response Status Code (Delete):", response.status_code)
        print("Response Data (Delete):", response.data)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TaskCreateViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.valid_task_data = {
            "title": "Test Task",
            "description": "Task description here."
        }

        self.invalid_task_data = {
            "title": "",
            "description": "Task description here."
        }

    def test_create_task_success(self):
        factory = APIRequestFactory()
        request = factory.post('/todo/tasks/create/', self.valid_task_data, format='json')

        force_authenticate(request, user=self.user)

        view = TaskCreateView.as_view()
        response = view(request)

        print("Response Status Code:", response.status_code)
        print("Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Task created successfully')
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().title, 'Test Task')

    def test_create_task_failure(self):
        factory = APIRequestFactory()
        request = factory.post('/todo/tasks/create/', self.invalid_task_data, format='json')

        force_authenticate(request, user=self.user)

        view = TaskCreateView.as_view()
        response = view(request)

        print("Response Status Code:", response.status_code)
        print("Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Failed to create task')
        self.assertIn('errors', response.data)
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_unauthenticated(self):
        factory = APIRequestFactory()
        request = factory.post('/todo/tasks/create/', self.valid_task_data, format='json')

        response = self.client.post('/todo/tasks/create/', self.valid_task_data, format='json')

        print("Response Status Code:", response.status_code)
        print("Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



class TaskDetailViewTests(APITestCase):
    def setUp(self):
        """Setup a test user and initial task data."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.task = Task.objects.create(
            title="Test Task",
            description="Task description here."
        )

        self.valid_task_data = {
            "id": self.task.id
        }

        self.invalid_task_data = {
            "id": 99999  # A task ID that doesn't exist
        }

    def test_get_task_success(self):
        """Test retrieving a task with a valid ID."""
        factory = APIRequestFactory()
        request = factory.get(f'/todo/tasks/detail/?id={self.valid_task_data["id"]}', format='json')

        force_authenticate(request, user=self.user)

        view = TaskDetailView.as_view()
        response = view(request)

        print("Response Status Code:", response.status_code)
        print("Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Task retrieved successfully')
        self.assertEqual(response.data['task']['title'], self.task.title)

    def test_get_task_failure_invalid_id(self):
        """Test retrieving a task with an invalid ID."""
        factory = APIRequestFactory()
        request = factory.get(f'/todo/tasks/detail/?id={self.invalid_task_data["id"]}', format='json')

        force_authenticate(request, user=self.user)

        view = TaskDetailView.as_view()
        response = view(request)

        print("Response Status Code:", response.status_code)
        print("Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Task not found')

    def test_get_task_missing_id(self):
        """Test retrieving a task without providing an ID."""
        factory = APIRequestFactory()
        request = factory.get('/todo/tasks/detail/', format='json')

        force_authenticate(request, user=self.user)

        view = TaskDetailView.as_view()
        response = view(request)

        print("Response Status Code:", response.status_code)
        print("Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'ID parameter is required')

    def test_get_task_unauthenticated(self):
        """Test retrieving a task without authentication."""
        factory = APIRequestFactory()
        request = factory.get(f'/todo/tasks/detail/?id={self.valid_task_data["id"]}', format='json')

        response = self.client.get(f'/todo/tasks/detail/?id={self.valid_task_data["id"]}', format='json')
        print("Response Status Code:", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



class TaskListViewTests(APITestCase):
    def setUp(self):
        """Setup a test user and initial tasks data."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.task1 = Task.objects.create(
            title="Test Task 1",
            description="Task description here."
        )

        self.task2 = Task.objects.create(
            title="Test Task 2",
            description="Another task description."
        )

        self.valid_task_data = {}

    def test_get_tasks_success(self):
        """Test retrieving all tasks."""
        factory = APIRequestFactory()
        request = factory.get('/todo/tasks', format='json')  

        force_authenticate(request, user=self.user)

        view = TaskListView.as_view()
        response = view(request)

        print("Response Status Code:", response.status_code)
        print("Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Tasks retrieved successfully')
        self.assertEqual(len(response.data['tasks']), 2) 
        self.assertEqual(response.data['tasks'][0]['title'], self.task1.title)
        self.assertEqual(response.data['tasks'][1]['title'], self.task2.title)


class TaskUpdateViewTests(APITestCase):
    def setUp(self):
        """Setup a test user, and initial task data for testing."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task = Task.objects.create(title='Old Task', description='Old description')

        self.valid_task_data = {
            'pk': self.task.pk,
            'title': 'Updated Task',
            'description': 'Updated description'
        }

        self.invalid_task_data = {
            'pk': self.task.pk,
            'title': ''  # Empty title, invalid data
        }

        self.invalid_task_no_pk = {
            'title': 'No Task ID'
        }

    def test_update_task_success(self):
        """Test updating a task with valid data."""
        factory = APIRequestFactory()
        request = factory.post('/todo/tasks/update/', self.valid_task_data, format='json')

        force_authenticate(request, user=self.user)

        view = TaskUpdateView.as_view()
        response = view(request)

        print("Response Status Code:", response.status_code)
        print("Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Task updated successfully')
        self.assertEqual(response.data['task']['title'], 'Updated Task')
        self.assertEqual(response.data['task']['description'], 'Updated description')

    def test_update_task_failure_invalid_data(self):
        """Test updating a task with invalid data (e.g., empty title)."""
        factory = APIRequestFactory()
        request = factory.post('/todo/tasks/update/', self.invalid_task_data, format='json')

        force_authenticate(request, user=self.user)

        view = TaskUpdateView.as_view()
        response = view(request)

        print("Response Status Code:", response.status_code)
        print("Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Failed to update task')
        self.assertIn('errors', response.data)

    def test_update_task_missing_pk(self):
        """Test updating a task with no 'pk' provided."""
        factory = APIRequestFactory()
        request = factory.post('/todo/tasks/update/', self.invalid_task_no_pk, format='json')

        force_authenticate(request, user=self.user)

        view = TaskUpdateView.as_view()
        response = view(request)

        print("Response Status Code:", response.status_code)
        print("Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Task ID is required')

    def test_update_task_not_found(self):
        """Test updating a task that does not exist."""
        invalid_task_data = {
            'pk': 9999,  # Non-existent task ID
            'title': 'Non-existent task',
            'description': 'Should not be found'
        }

        factory = APIRequestFactory()
        request = factory.post('/todo/tasks/update/', invalid_task_data, format='json')

        force_authenticate(request, user=self.user)

        view = TaskUpdateView.as_view()
        response = view(request)

        print("Response Status Code:", response.status_code)
        print("Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Task not found')

    def test_update_task_unauthenticated(self):
        """Test updating a task without authentication."""
        factory = APIRequestFactory()
        request = factory.post('/todo/tasks/update/', self.valid_task_data, format='json')

        response = self.client.post('/todo/tasks/update/', self.valid_task_data, format='json')

        print("Response Status Code:", response.status_code)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from api.models import Task
from api.views import TaskDeleteView

class TaskDeleteViewTests(APITestCase):
    def setUp(self):
        """Setup a test user and initial task data for testing."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task = Task.objects.create(title='Test Task', description='Test description')

        self.valid_task_data = {
            'pk': self.task.pk
        }

        self.invalid_task_data = {
            'pk': 9999  # Non-existent task ID
        }

        self.invalid_task_no_pk = {}

    def test_delete_task_success(self):
        """Test deleting a task with valid data."""
        factory = APIRequestFactory()
        request = factory.delete('/todo/tasks/delete/', self.valid_task_data, format='json')

        force_authenticate(request, user=self.user)

        view = TaskDeleteView.as_view()
        response = view(request)

        print("Response Status Code:", response.status_code)
        print("Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'], 'Task deleted successfully')
        self.assertEqual(Task.objects.count(), 0)  # Ensure the task is deleted

    def test_delete_task_failure_no_id(self):
        """Test deleting a task with no 'pk' provided."""
        factory = APIRequestFactory()
        request = factory.delete('/todo/tasks/delete/', self.invalid_task_no_pk, format='json')

        force_authenticate(request, user=self.user)

        view = TaskDeleteView.as_view()
        response = view(request)

        print("Response Status Code:", response.status_code)
        print("Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Task ID is required')

    def test_delete_task_not_found(self):
        """Test deleting a task that does not exist."""
        factory = APIRequestFactory()
        request = factory.delete('/todo/tasks/delete/', self.invalid_task_data, format='json')

        force_authenticate(request, user=self.user)

        view = TaskDeleteView.as_view()
        response = view(request)

        print("Response Status Code:", response.status_code)
        print("Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Task not found')

    def test_delete_task_unauthenticated(self):
        """Test deleting a task without authentication."""
        factory = APIRequestFactory()
        request = factory.delete('/todo/tasks/delete/', self.valid_task_data, format='json')

        response = self.client.delete('/todo/tasks/delete/', self.valid_task_data, format='json')

        print("Response Status Code:", response.status_code)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
