from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from stable_diffusion_webui.models import Prompt
from stable_diffusion_webui.utils import medium_options, style_options, artist_options, resolution_options, light_options, \
    color_options



class Command(BaseCommand):
    help = "Complete prompt word of table Prompt"

    def handle(self, *args, **options):
        preserve_mediums = self.get_names(medium_options)
        preserve_styles = self.get_names(style_options)
        preserve_artistes = self.get_names(artist_options)
        preserve_resolutions = self.get_names(resolution_options)
        preserve_lightings = self.get_names(light_options)
        preserve_colors = self.get_names(color_options)
        prompts = Prompt.objects.all()
        for p in prompts:
            terms = [x.strip() for x in p.text.split(",")]
            mediums = []
            styles = []
            artistes = []
            resolutions = []
            lightings = []
            colors = []
            for term in terms:
                if term in preserve_mediums:
                    mediums.append(term)
                if term in preserve_styles:
                    styles.append(term)
                if term in preserve_artistes:
                    artistes.append(term)
                if term in preserve_resolutions:
                    resolutions.append(term)
                if term in preserve_lightings:
                    lightings.append(term)
                if term in preserve_colors:
                    colors.append(term)
            
            p.mediums = mediums
            p.styles = styles
            p.artistes = artistes
            p.resolutions = resolutions
            p.lightings = lightings
            p.colors = colors
            p.save()
            
        self.stdout.write(
            self.style.SUCCESS('Successfully complete {} prompts'.format(len(prompts)))
        )

    def get_names(self, options):
        return set([x["name"] for x in options])
