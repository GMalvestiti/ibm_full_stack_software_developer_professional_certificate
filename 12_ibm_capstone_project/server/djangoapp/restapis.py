import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    api_key = kwargs.get("api_key")
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
        
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)

    return json_data

def post_request(url, json_payload, **kwargs):
    print(f"POST to {url}")
    try:
        print(json.dumps(json_payload))
        response = requests.post(url, json=json_payload)
        print(f"With status {response.status_code}")
        return response
    except Exception as e:
        print(f"An error occurred while making POST request: {str(e)}")
        return None  # You should decide what to return or how to handle the error


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], state=dealer_doc["state"])
            results.append(dealer_obj)

    return results

def get_dealers_by_id(url, dealer_id):
    # Call get_request with the dealer_id param
    dealers = get_dealers_from_cf(url)  # Assuming this function returns a list of dealer dictionaries
    dealer_obj = None

    # Create a CarDealer object from response
    for dealer in dealers:
        if dealer.id == dealer_id:
            return dealer

def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # For each dealer object
        for review_doc in json_result:
            if review_doc["dealership"] == dealer_id:
                keys = review_doc.keys()

                dealerReview_obj = DealerReview(
                    dealership=review_doc["dealership"], 
                    name=review_doc["name"], 
                    purchase=review_doc["purchase"],
                    purchase_date = review_doc["purchase_date"],
                    review=review_doc["review"],
                    car_make=review_doc["car_make"], 
                    car_model=review_doc["car_model"],
                    car_year=review_doc["car_year"], 
                    sentiment="NULL",
                    id=review_doc["id"])
                dealerReview_obj.sentiment = analyze_review_sentiments(dealerReview_obj.review)
                results.append(dealerReview_obj)
    return results

def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/cd2fd35b-b505-483f-9aa7-55d841e7c4db"
    api_key = "QCbgrz0SnGFbRp-pVqBFMVekbglUhrfnK558tv1iYn8S"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    return(label)