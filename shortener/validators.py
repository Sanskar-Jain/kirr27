from django.core.validators import URLValidator, validate_slug
from django.core.exceptions import ValidationError

def validate_url(value):
	url_validator = URLValidator()
	value1_invalid = False
	value2_invalid = False

	try:
		url_validator(value)
	except:
		value1_invalid = True

	value2 = 'http://' + value

	try:
		url_validator(value2)
	except:
		value2_invalid = True

	if value1_invalid and value2_invalid:
		raise ValidationError("Invalid URL")

	if "http://" not in value and "https://" not in value:
		value = "http://" + value

	return value

def validate_shortcode(value):
	valid = True

	try:
		validate_slug(value)
	except:
		valid = False

	if not value or len(value)<1:
		raise ValidationError('Too Short - Minimum Length allowed is 6 charachters.')
	if len(value)>15:
	 	raise ValidationError('Too Long - Minimum Length allowed is 15 charachters.')

	if not valid:
		raise ValidationError('Invalid code - Only Alphanumeric charachters, underscores and hyphens are allowed.')

	return value