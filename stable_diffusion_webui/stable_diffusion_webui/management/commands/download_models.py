from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler


class Command(BaseCommand):
    help = "Download all models"

    def handle(self, *args, **options):
        for model_id in settings.MODEL_IDS:
            StableDiffusionPipeline.from_pretrained(model_id)
            self.stdout.write(
                self.style.SUCCESS('Successfully download "%s"' % model_id)
            )