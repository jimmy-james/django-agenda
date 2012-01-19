from django import template
register = template.Library()
from django.db import models
Event = models.get_model('agenda', 'event')
from datetime import datetime, timedelta
import logging

class UpcomingEventsNode(template.Node):
    def __init__(self, count, var_name):
        self.count = count
        self.var_name = var_name

    def render(self, context):
        logging.debug("get_upcoming_events %s as %s" % (self.count, self.var_name))
        now = datetime.now()
        upcoming_events = Event.published.all().order_by('event_date').filter(event_date__gte=now - timedelta(days=1))[:self.count]
        logging.debug("now %s" % now)
        logging.debug("upcoming_events %s" % upcoming_events)
        context[self.var_name] = upcoming_events
        return ''

@register.tag(name="get_upcoming_events")
def get_upcoming_events(parser, token):
    # get_upcoming_events <count> as <var_name>
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError, "%r takes 3 arguments" % bits[0]
    return UpcomingEventsNode(bits[1], bits[3])
