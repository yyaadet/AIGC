from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler, DiffusionPipeline


class Command(BaseCommand):
    help = "Download all models"

    def handle(self, *args, **options):
        for item in settings.MODEL_IDS:
            model_id = item['id']
            StableDiffusionPipeline.from_pretrained(model_id, resume_download=True)
            self.stdout.write(
                self.style.SUCCESS('Successfully download "%s"' % model_id)
            )