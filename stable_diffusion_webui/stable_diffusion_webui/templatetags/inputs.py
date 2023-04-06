from django import template

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
    return {'input_id': input_id, 'label': label, 'options': options}