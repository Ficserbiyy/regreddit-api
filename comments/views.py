from django.shortcuts import render
from django.http import JsonResponse


def comment_list(request):
    return JsonResponse(
        {
            "message": "Welcome to comments!"
        }
    )

