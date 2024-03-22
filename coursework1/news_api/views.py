from os import stat
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Author, Story
from datetime import datetime
import json

# Create your views here.

@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"message": "Welcome!"}, status=200)
    else:
        return JsonResponse({"error": "Invalid login attempt."}, status=401)

@csrf_exempt
@require_http_methods(["POST"])
def logout_user(request):
    logout(request)
    return JsonResponse({"message": "Goodbye!"}, status=200)

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def post_story(request):
    data = json.loads(request.body)
    try:
        author = Author.objects.get(username=request.user.username)
        # 'Data' - parsed JSON containing the story details
        Story.objects.create(
            headline=data['headline'],
            category=data['category'],
            region=data['region'],
            details=data['details'],
            author=author
        )
        return JsonResponse({"message": "Story posted successfully."}, status=201)
    except Author.DoesNotExist:
        # If no Author instance is found for user
        return HttpResponse("Unable to post story: Author instance not found for the logged-in user.", status=400)
    except KeyError as e:
        return HttpResponse(f"Missing data: {e}", status=400)
    except Exception as e:
        return HttpResponse(f"Unable to post story: {str(e)}", status=503, content_type="text/plain")

@csrf_exempt
def stories(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Please log in to post stories."}, status=401)
        
        data = json.loads(request.body)
        author = Author.objects.get(username=request.user.username)
        
        Story.objects.create(
            headline=data['headline'],
            category=data['category'],
            region=data['region'],
            details=data['details'],
            author=author
        )
        return JsonResponse({"message": "Story posted successfully."}, status=201)

    elif request.method == "GET":
        story_cat = request.GET.get('story_cat', '*')
        story_region = request.GET.get('story_region', '*')
        story_date_str = request.GET.get('story_date', '*')
        
        filters = {}
        if story_cat != '*':
            filters['category'] = story_cat
        if story_region != '*':
            filters['region'] = story_region
        if story_date_str != '*':
            filters['date__gte'] = datetime.strptime(story_date_str, "%d/%m/%Y").date()
        
        stories = Story.objects.filter(**filters)
        stories_data = [{
            "key": str(story.id),
            "headline": story.headline,
            "story_cat": story.category,
            "story_region": story.region,
            "author": story.author.name,
            "story_date": story.date.strftime("%d/%m/%Y"),
            "story_details": story.details
        } for story in stories]
        
        if stories:
            return JsonResponse({"stories": stories_data}, safe=False, status=200)
        else:
            return HttpResponse("No stories found matching the criteria.", status=404)

    else:
        return HttpResponse("Method not allowed", status=405)

@csrf_exempt
@require_http_methods(["DELETE"])
@login_required
def delete_story(request, story_id):
    try:
        # Story to be deleted
        story = Story.objects.get(pk=story_id, author__username=request.user.username)
        story.delete()
        return JsonResponse({"message": "Story deleted successfully."}, status=200)
    except Story.DoesNotExist:
        return HttpResponse("Story not found or not authorized to delete.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500, content_type="text/plain")

