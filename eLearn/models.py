from django.db import models
from users.models import CustomUser

class Course(models.Model):
    professor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField()
    uploadDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploadDate']

    def __str__(self):
        return self.name


class Video(models.Model):
    course = models.ForeignKey('Course', related_name='modules', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    videoid = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
