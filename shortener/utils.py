import random
import string
from django.conf import settings

SHORTCODE_MIN = getattr(settings, 'SHORTCODE_MIN', 6)


def code_generator(size=SHORTCODE_MIN, chars = string.ascii_lowercase + string.digits):
	return "".join([random.choice(chars) for _ in range(size)])


def create_shortcode(instance, size=SHORTCODE_MIN):
	code = code_generator(size=size)
	Klass = instance.__class__
	if Klass.objects.filter(shortcode=code).exists():
		return create_shortcode(instance,size)
	return code