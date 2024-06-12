from django import template
from minigen.models import MCQPost

register = template.Library()

@register.filter
def get_user_data(form_data, user_id):
    return form_data.filter(user_id=user_id)