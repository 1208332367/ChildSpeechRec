# -*- coding: utf-8 -*-
from django.http import HttpResponse
from SpeechRec import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def hello(request):
	return HttpResponse("Hello SpeechRec")
