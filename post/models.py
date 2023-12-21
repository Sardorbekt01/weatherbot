from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=250, blank=False)
    body = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title