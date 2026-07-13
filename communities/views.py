from django.shortcuts import render
from django.http import JsonResponse


def community_list(request):
    return JsonResponse(
        {
            "message": "Welcome to Community!"
        }
    )

