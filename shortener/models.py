from django.db import models
from django.conf import settings
from django.urls import reverse

from django.core.exceptions import ValidationError

from .utils import code_generator, create_shortcode
from .validators import validate_url


# Create your models here.

SHORTCODE_MAX = getattr(settings, 'SHORTCODE_MAX', 15)

class KirrURLManager(models.Manager):

	def all(self,*args,**kwargs):
		return super(KirrURLManager,self).all(*args,**kwargs).filter(isactive=True)

	def get_or_create(self, *args, **kwargs):
		try:
			kwargs['url'] = validate_url(kwargs.get('url'))
		except:
			raise ValidationError("Invalid URL")
		return super(KirrURLManager,self).get_or_create(*args, **kwargs)

	def refresh_shortcodes(self, items=None):
		objects = KirrURL.objects.filter(id__gte=1)
		if items is not None and isinstance(items,int):
			objects = objects.order_by('-id')[:items]
		for obj in objects:
			obj.shortcode = create_shortcode(obj)
			print(obj.shortcode)
			obj.save()
		return "New shortcodes made {codes}".format(codes = objects.count())

class KirrURL(models.Model):
	url = models.CharField(max_length=256, validators = [validate_url])
	shortcode = models.CharField(max_length=SHORTCODE_MAX, blank=True)
	updated_on = models.DateTimeField(auto_now=True)
	created_on = models.DateTimeField(auto_now_add=True)
	isactive = models.BooleanField(default=True)

	objects = KirrURLManager()

	def save(self, *args, **kwargs):
		if not self.shortcode:
			self.shortcode = create_shortcode(self)
		try:
			self.url = validate_url(self.url)
		except:
			raise ValidationError("Invalid URL")
		super(KirrURL,self).save(*args, **kwargs)

	def __str__(self):
		return str(self.url)

	def __unicode__(self):
		return str(self.url)

	def get_short_url(self):
		url_path = reverse('scode', kwargs={'shortcode': self.shortcode})
		return url_path
