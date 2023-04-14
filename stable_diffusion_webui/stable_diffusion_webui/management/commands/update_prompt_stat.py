from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from stable_diffusion_webui.models import PromptWordStat



class Command(BaseCommand):
    help = "Update prompt stat"

    def handle(self, *args, **options):
        PromptWordStat.update()