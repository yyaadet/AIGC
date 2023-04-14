from django import template

from stable_diffusion_webui.models import PromptWordStat


register = template.Library()


@register.inclusion_tag("tags/multiple_check.html")
def multiple_check(input_id, label, options):
    """Multiple check

    Args:
        input_id (str): input id
        label (str): input label name 
        options (dict): [{'name': str, 'value': str}] 

    Returns:
        dict: context for rendering
    """
    new_options = options.copy()
    prompt_word_stats = PromptWordStat.objects.filter(category=input_id)
    word_hit_map = {}
    word_ratio_map = {}
    for p in prompt_word_stats:
        word_hit_map[p.word] = p.hit
        word_ratio_map[p.word] = round(p.ratio * 100, 2)

    for i in range(len(new_options)):
        new_options[i]['hit'] = word_hit_map.get(new_options[i]['name'], '')
        new_options[i]['percentage'] = word_ratio_map.get(new_options[i]['name'], '')

    return {'input_id': input_id, 'label': label, 'options': options}