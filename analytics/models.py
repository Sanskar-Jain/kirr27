from django.db import models

from shortener.models import KirrURL

# Create your models here.

class ClickEventManager(models.Manager):
	def create_event(self,KirrInstance):
		if isinstance(KirrInstance, KirrURL):
			obj, created = self.get_or_create(kirr_url=KirrInstance)
			obj.count += 1
			obj.save()
			return obj.count
		return None


class ClickEvent(models.Model):
	kirr_url = models.OneToOneField(KirrURL, on_delete=models.CASCADE)
	count = models.IntegerField(default=0)
	updated_on = models.DateTimeField(auto_now=True)
	created_on = models.DateTimeField(auto_now_add=True)

	objects = ClickEventManager()

	def __str__(self):
		return str(self.count)