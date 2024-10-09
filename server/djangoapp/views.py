# pylint: disable-all
# Uncomment the required imports before adding the code
# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

@csrf_exempt
def login_user(request):
    """Handle user login."""
    # Get username and password from request body
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    
    # Authenticate user
    user = authenticate(username=username, password=password)
    
    if user is not None:
        login(request, user)
        response_data = {
            "userName": username,
            "status": "Authenticated"
        }
    else:
        response_data = {
            "userName": username
        }
    
    return JsonResponse(response_data)


def logout_request(request):
    """Handle user logout."""
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    """Handle user registration."""
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    # Check if user already exists
    if User.objects.filter(username=username).exists():
        logger.debug(f"{username} is already registered.")
        return JsonResponse({
            "userName": username,
            "error": "Already Registered"
        })
    
    # Create user if not already registered
    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email,
    )
    
    login(request, user)
    return JsonResponse({
        "userName": username,
        "status": "Authenticated"
    })


def get_dealerships(request, state="All"):
    """Retrieve list of dealerships."""
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    """Retrieve reviews for a specific dealer."""
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response['sentiment']
        
        return JsonResponse({"status": 200, "reviews": reviews})

    return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_details(request, dealer_id):
    """Retrieve details for a specific dealer."""
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})

    return JsonResponse({"status": 400, "message": "Bad Request"})


def add_review(request):
    """Submit a review."""
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({
                "status": 401,
                "message": f"Error: {e} in posting review"
            })

    return JsonResponse({"status": 403, "message": "Unauthorized"})


def get_cars(request):
    """Retrieve car data."""
    count = CarMake.objects.count()
    if count == 0:
        initiate()
    
    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        for car_model in car_models
    ]
    
    return JsonResponse({"CarModels": cars})
