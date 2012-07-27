# Template and context-related imports
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Context

# JSON for the live search
from django.utils import simplejson

# eve_db models
from eve_db.models import InvType

def home(request):
		"""
		Returns our static home template.
		"""
		return render_to_response('home.haml')

def live_search(request, query='a'):
	
		"""
		This adds a basic live search view to element43.
		The names in the invTypes table are searched with a case insensitive LIKE query and the result is returned as a JSON array of matching names.
		"""
		
		# Prepare lists
		types = []
		type_names = []
		
		# Default to empty array
		types_json = "[]"
		
		# Only if the string is longer than 2 characters start looking in the DB
		if len(query) > 2:
			
				# Load published type objects matching the name
				types = InvType.objects.filter(name__icontains = query, is_published = True)
				
				for single_type in types:
					type_names.append(single_type.name)
				
				# Turn names into JSON
				types_json = simplejson.dumps(type_names)
		
		# Return JSON without using any template
		return HttpResponse(types_json, mimetype = 'application/json')