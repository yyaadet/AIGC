from django.db import models
from django.core.files.storage import FileSystemStorage 
import os

from .utils import list_to_matrix


class GenerateRequest(models.Model):
    request_body = models.JSONField()
    combinations = models.JSONField()
    create_at = models.DateTimeField(auto_now_add=True)

    @property
    def prompt_matrix(self):
        prompts = Prompt.objects.filter(request=self)
        matrix = list_to_matrix(prompts, col=4)
        return matrix
    
    @property
    def prompt_count(self):
        return Prompt.objects.filter(request=self).count()
    
    def prompts(self):
        return Prompt.objects.filter(request=self)
    
    def combination_count(self):
        return len(self.combinations)


class Prompt(models.Model):
    request = models.ForeignKey(GenerateRequest, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.FilePathField()
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "stable_diffusion_webui"

    def media_url(self):
        store = FileSystemStorage()
        filename = os.path.basename(self.image)
        url = store.url(filename)
        return url

