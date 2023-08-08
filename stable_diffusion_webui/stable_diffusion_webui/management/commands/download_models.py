from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from stable_diffusion_webui.sd_model import SDModel

from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler, DiffusionPipeline


class Command(BaseCommand):
    help = "Download all models"

    def handle(self, *args, **options):
        SDModel().initial_models()