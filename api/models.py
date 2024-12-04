from django.db import models

class Task(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('WORKING', 'Working'),
        ('PENDING_REVIEW', 'Pending Review'),
        ('COMPLETED', 'Completed'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    ]

    # Fields
    title = models.CharField(max_length=100)  
    description = models.TextField(max_length=1000)  
    timestamp = models.DateTimeField(auto_now_add=True)  
    due_date = models.DateField(null=True, blank=True) 
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='OPEN'
    )  
    tags = models.ManyToManyField('Tag', blank=True) 

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True) 

    def __str__(self):
        return self.name
