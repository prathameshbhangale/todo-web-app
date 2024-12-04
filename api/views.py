from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer

class TaskCreateView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Task created successfully',
                'task': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Failed to create task',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        task_id = request.query_params.get('id')
        
        if not task_id:
            return Response({
                'message': 'ID parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            task = Task.objects.get(pk=task_id)
            serializer = TaskSerializer(task)
            return Response({
                'message': 'Task retrieved successfully',
                'task': serializer.data
            }, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({
                'message': 'Task not found'
            }, status=status.HTTP_404_NOT_FOUND)

class TaskListView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response({
            'message': 'Tasks retrieved successfully',
            'tasks': serializer.data
        }, status=status.HTTP_200_OK)

class TaskUpdateView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Extract the 'pk' from the request body
            pk = request.data.get('pk')
            
            if not pk:
                return Response({
                    'message': 'Task ID is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Attempt to get the task with the given 'pk'
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Task updated successfully',
                    'task': serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                'message': 'Failed to update task',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response({
                'message': 'Task not found'
            }, status=status.HTTP_404_NOT_FOUND)

class TaskDeleteView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            pk = request.data.get('pk')
            
            if not pk:
                return Response({
                    'message': 'Task ID is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            task = Task.objects.get(pk=pk)
            task.delete()
            return Response({
                'message': 'Task deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({
                'message': 'Task not found'
            }, status=status.HTTP_404_NOT_FOUND)
