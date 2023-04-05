from django.db import models



class Prompt(models.Model):
    text = models.TextField()
    image = models.FilePathField()
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "stable_diffusion_webui"

