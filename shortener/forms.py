from django import forms
from .validators import validate_url, validate_shortcode

class URLForm(forms.Form):
	url = forms.CharField(
		label = '', 
		validators = [validate_url],
		widget = forms.TextInput(
				attrs = {
					"placeholder": "Long URL",
					"class": "form-control"
				}
			)
		)

class CustomURLForm(forms.Form):
	url = forms.CharField(
		label = '', 
		validators = [validate_url],
		widget = forms.TextInput(
				attrs = {
					"placeholder": "Long URL",
					"class": "form-control"
				}
			)
		)
	shortcode = forms.CharField(
		label = '',
		validators = [validate_shortcode],
		widget = forms.TextInput(
				attrs = {
					"placeholder": "Short Code | Allowed characters are A-Z a-z 0-9 - _",
					"class": "form-control"
				}
			)
		)

	def clean_url(self):
		url = self.cleaned_data.get('url')
		if "http://" not in url and "https://" not in url:
			return "http://" + url
		return url
