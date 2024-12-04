from django.urls import path
from .views import TaskCreateView, TaskDetailView, TaskListView, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task-list'),     # Retrieve all tasks

    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),    # Create a new task
    path('tasks/create', TaskCreateView.as_view(), name='task-create'),    # Create a new task (no slash)


    path('task/', TaskDetailView.as_view(), name='task-create'),    # Retrieve a single task by ID


    path('tasks/update/', TaskUpdateView.as_view(), name='task-update'),  # Update a task by ID
    path('tasks/update', TaskUpdateView.as_view(), name='task-update-no-slash'),  # Update a task by ID (no slash)

    path('tasks/delete', TaskDeleteView.as_view(), name='task-delete'),  # Delete a task by ID


]

