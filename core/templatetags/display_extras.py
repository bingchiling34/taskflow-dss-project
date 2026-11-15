from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def friendly_date(value):
    if value is None:
        return ""

    local_value = timezone.localtime(value)
    today = timezone.localtime(timezone.now()).date()
    value_day = local_value.date()
    delta_days = (today - value_day).days

    if delta_days < 0:
        return local_value.strftime("%Y-%m-%d")
    if delta_days == 0:
        return "Today"
    if delta_days == 1:
        return "1 day ago"
    if delta_days <= 7:
        return str(delta_days) + " days ago"
    return local_value.strftime("%Y-%m-%d")
