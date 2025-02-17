from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_request, get_dealers_from_cf, get_dealers_by_id, get_dealer_reviews_from_cf, post_request
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import date, datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def get_about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def get_contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    context = {}
    logout(request)

    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `registration_request` view to handle sign up request
def signup_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://gustavosmalv-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealerships"] = dealerships
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)
    return render(request, 'djangoapp/index.html', context)

def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://gustavosmalv-5000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews?id={0}".format(dealer_id)
        url_dealer = f"https://gustavosmalv-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"

        reviews = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        dealer = get_dealers_by_id(url_dealer, dealer_id=dealer_id)
        context = {
            "reviews":  reviews,
            "dealer_id": dealer_id,
            "dealer": dealer
        }
    return render(request, 'djangoapp/dealer_details.html', context)


def add_review(request, dealer_id):
    # User must be logged in before posting a review
    if request.user.is_authenticated:
        # GET request renders the page with the form for filling out a review
        if request.method == "GET":
            url = f"https://gustavosmalv-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
            # Get dealer details from the API
            context = {
                "cars": CarModel.objects.all().filter(dealer=dealer_id),
                "dealer": get_dealers_by_id(url, dealer_id=dealer_id),
            }
            return render(request, 'djangoapp/add_review.html', context)
        # POST request posts the content in the review submission form to the Cloudant DB using the post_review Cloud Function
        if request.method == "POST":
            form = request.POST
            review = dict()
            review["name"] = f"{request.user.first_name} {request.user.last_name}"
            review["dealership"] = dealer_id
            review["review"] = form["content"]
            review["purchase"] = form.get("purchasecheck")
            car = CarModel.objects.get(pk=form["car"])
            review["car_make"] = car.car_make.name
            review["car_model"] = car.name
            review["car_year"] = car.year.isoformat()
            
            # If the user bought the car, get the purchase date
            if form.get("purchasecheck"):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), '%m/%d/%Y').isoformat()
            else: 
                review["purchase_date"] = None
            
            review["id"] = 10
            
            url = "https://gustavosmalv-5000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review?id={0}".format(dealer_id)
            json_payload = review # {"review": review}  # Create a JSON payload that contains the review data
            
            # POST request with the review
            result = post_request(url, json_payload, dealer_id=dealer_id)
            if int(result.status_code) == 200:
                print("Review posted successfully.")

            # Redirect to dealer details
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

    else:
        # If user isn't logged in, redirect to login page
        print("User must be authenticated before posting a review. Please log in.")
