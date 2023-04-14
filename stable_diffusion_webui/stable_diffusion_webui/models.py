from django.db import models
from django.core.files.storage import FileSystemStorage 
import os

from .utils import list_to_matrix


class GenerateRequest(models.Model):
    request_body = models.JSONField()
    combinations = models.JSONField()
    create_at = models.DateTimeField(auto_now_add=True)

    @property
    def prompt_matrix(self, n_col=6):
        prompts = Prompt.objects.filter(request=self)
        matrix = list_to_matrix(prompts, col=n_col)
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
    exclude = models.TextField(null=True, blank=True)
    mediums = models.JSONField(null=True, blank=True)
    styles = models.JSONField(null=True, blank=True)
    artistes = models.JSONField(null=True, blank=True)
    websites = models.JSONField(null=True, blank=True)
    resolutions = models.JSONField(null=True, blank=True)
    colors = models.JSONField(null=True, blank=True)
    lightings = models.JSONField(null=True, blank=True)
    image = models.FilePathField()
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "stable_diffusion_webui"

    def media_url(self):
        store = FileSystemStorage()
        filename = os.path.basename(self.image)
        url = store.url(filename)
        return url
    

class PromptWordStat(models.Model):
    CATEGORY_MEDIUM = "medium"
    CATEGORY_STYLE = "style"
    CATEGORY_ARTIST = "artist"
    CATEGORY_WEBSITE = "website"
    CATEGORY_RESOLUTION = "resolution"
    CATEGORY_COLOR = "color"
    CATEGORY_LIGHTING = "lighting"
    word = models.CharField(max_length=255)
    category = models.CharField(max_length=128)
    hit = models.IntegerField(default=0)
    ratio = models.FloatField(default=0.0)

    class Meta:
        unique_together = (("word", "category"))

    @classmethod
    def update(cls):
        category_word_hit_map = {
            cls.CATEGORY_MEDIUM: {},
            cls.CATEGORY_STYLE: {},
            cls.CATEGORY_ARTIST: {},
            cls.CATEGORY_WEBSITE: {},
            cls.CATEGORY_RESOLUTION: {},
            cls.CATEGORY_COLOR: {},
            cls.CATEGORY_LIGHTING: {},
        } # {category: {word: hit}}
        prompts = Prompt.objects.all()
        for p in prompts:
            items = [
                (p.mediums, cls.CATEGORY_MEDIUM),
                (p.styles, cls.CATEGORY_STYLE),
                (p.artistes, cls.CATEGORY_ARTIST),
                (p.websites, cls.CATEGORY_WEBSITE),
                (p.resolutions, cls.CATEGORY_RESOLUTION),
                (p.colors, cls.CATEGORY_COLOR),
                (p.lightings, cls.CATEGORY_LIGHTING),
            ]
            for item in items:
                if not item[0]:
                    continue
                category = item[1]
                for v in item[0]:
                    if v in category_word_hit_map[category]:
                        category_word_hit_map[category][v] += 1
                    else:
                        category_word_hit_map[category][v] = 1
        # save to db
        for category, word_hit_map in category_word_hit_map.items():
            total_hit = sum([x for _, x in word_hit_map.items()])
            for word, hit in word_hit_map.items():
                if total_hit > 0:
                    ratio = hit / total_hit
                else:
                    ratio = 0
                try:
                    obj = cls.objects.get(category=category, word=word, ratio=ratio)
                except:
                    obj = cls(category=category, word=word, hit=hit, ratio=ratio)
                obj.save()
                

