from django.db import models

from users.models import Users

class Tasks(models.Model):
    CATEGORY_CHOICES = [
        ('TG', 'TG'),
        ('YouTube', 'YouTube'),
    ]
    
    name = models.CharField(max_length=255, null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    reward = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name

    
class TasksUser(models.Model):
    STATUS_CHOICES = [
        ('done', 'done'),
        ('checked', 'checked'),
    ]
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES)
    
    def get_status_label(self):
        if self.status == 'checked':
            return 'get'
        elif self.status == 'done':
            return 'completed'
        return 'start'
    