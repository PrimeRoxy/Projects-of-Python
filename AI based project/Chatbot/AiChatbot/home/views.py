from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

import os
import openai

openai.api_key ="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"

# Create your views here.
def chat (request) :
    return render(request, "index.html")
 
def chatAPI(request) :
    if request.method == "POST":
        prompt = request. POST["prompt"]

        response = {"this": "that"}
        response = openai.ChatCompletion.create(
            model="text-davinci-003",
            prompt = prompt,
            temperature=0.6,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        return JsonResponse (response)
    return HttpResponse(" Bad Request")
    

    
#   messages=[
#     {
#       "role": "user",
#       "content": ""
#     }
#   ],