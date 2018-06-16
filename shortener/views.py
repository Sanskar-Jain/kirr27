from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View

from .models import KirrURL
from .forms import URLForm, CustomURLForm
from analytics.models import ClickEvent

# Create your views here.


class HomeView(View):

	def get(self, request, *args, **kwargs):
		form = URLForm()
		context = {
			'form' : form,
			'page' : 'home'
		}
		return render(request, 'shortener/home.html', context)

	def post(self, request, *args, **kwargs):
		form = URLForm(request.POST)
		context = {
			'form' : form,
			'page' : 'home'
		}
		template = 'shortener/home.html'

		if form.is_valid():
			url = form.cleaned_data.get('url')
			obj, created = KirrURL.objects.get_or_create(url=url)
			context = {
				'object': obj,
				'created': created,
				'page' : 'home'
			}
			if created:
				template = 'shortener/success.html'
			else:
				template = 'shortener/already-exists.html'
		return render(request, template, context)


class CustomURLView(View):

	def get(self, request, *args, **kwargs):
		form = CustomURLForm()
		context = {
			'form' : form,
			'page' : 'custom'
		}
		return render(request, 'shortener/customurl.html', context)

	def post(self, request, *args, **kwargs):
		form = CustomURLForm(request.POST)
		context = {
			'form' : form,
			'page' : 'custom'
		}
		template = 'shortener/customurl.html'

		if form.is_valid():
			url = form.cleaned_data.get('url')
			shortcode = form.cleaned_data.get('shortcode')
			obj_with_url = KirrURL.objects.filter(url=url)
			obj_with_shortcode = KirrURL.objects.filter(shortcode=shortcode)
			if obj_with_url and obj_with_url.count()>=1:
				context = {
					'object': obj_with_url[0],
					'created': False,
					'page' : 'custom'
				}
				template = 'shortener/already-exists.html'
			elif obj_with_shortcode.count()==1:
				context = {
					'form': form,
					'object': None,
					'created': False,
					'page': 'custom',
					'error': 'Shortcode already in use!'
				}
				template = 'shortener/customurl.html'
			else:
				obj = KirrURL()
				obj.url = url
				obj.shortcode = shortcode
				obj.save()
				context = {
					'object': obj,
					'created': True,
					'page' : 'home'
				}
				template = 'shortener/success.html'

		return render(request, template, context)

class URLRedirectView(View):

	def get(self, request, shortcode = None, *args, **kwargs):
		obj = get_object_or_404(KirrURL, shortcode = shortcode)
		print(ClickEvent.objects.create_event(obj))
		return HttpResponseRedirect(obj.url)

