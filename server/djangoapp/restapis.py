import requests
import json

from requests import status_codes
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print(f"GET from {url}")
    try:
        # Call to NLU service includes API key
        if "apikey" in kwargs:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, headers={"Content-Type": "application/json"},
                                    params=kwargs, auth=HTTPBasicAuth("apikey", kwargs["apikey"]))

        # Call to Cloudant DB                            
        else: 
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={"Content-Type": "application/json"},
                                    params=kwargs) 
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print(f"With status {status_code}")
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print(f"POST to {url}")
    try:
        # Post review to Cloudant DB
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=json_payload)
    except:
        #If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print(f"With status {status_code}")
    json_data = response.json()
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, **kwargs)
    if json_result:
        # If result contains `status`, an error was produced
        if "status" in json_result:
            return json_result
        else:
            # Get the entries list in JSON as dealers
            dealers = json_result["entries"]
            # For each dealer entry
            for dealer in dealers:
                # Get its content in `dealer` object
                dealer_obj = CarDealer(id=dealer["id"], city=dealer["city"], state=dealer["state"], st=dealer["st"],
                                        address=dealer["address"], zip=dealer["zip"], lat=dealer["lat"], long=dealer["long"],
                                        short_name=dealer["short_name"], full_name=dealer["full_name"])
                results.append(dealer_obj)
    return results


def get_dealer_by_state(url, **kwargs):
    return get_dealers_from_cf(url, **kwargs)



# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, **kwargs)
    if json_result:
        # If result contains `status`, an error ocurred
        if "status" in json_result:
            return json_result
        else:
            # Get the entries list in JSON as reviews
            reviews = json_result["entries"]
            # For each review entry
            for review in reviews:
                # Get its content in `review` object
                review_obj = DealerReview(review["name"], review["dealership"], review["review"], review["purchase"],
                                            review["id"])
                # Attempt to set optional attributes
                if "purchase_date" in review:
                    review_obj.purchase_date = review["purchase_date"]
                if "car_make" in review:
                    review_obj.car_make = review["car_make"]
                if "car_model" in review:
                    review_obj.car_model = review["car_model"]
                if "car_year" in review:
                    review_obj.car_year = review["car_year"]
                
                # Assign Watson NLU review sentiment result
                review_obj.sentiment = analyze_review_sentiment(review_obj.review)
                results.append(review_obj)
            return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiment(reviewText):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/a339c72f-5e27-4b43-8cb3-75a53c5cb7d0/v1/analyze"
    params = dict()
    params["apikey"] = "ZZqJDS2TX3hSrAXBoSYKSf_UB5g-s_MC2HwWeuIbtwFl"
    params["text"] = reviewText
    params["version"] = "2021-03-25"
    params["features"] = ["sentiment"]
    params["return_analyzed_text"] = False
    params["language"] = "en"
    response = get_request(url, **params)
    if "sentiment" in response:
        return response["sentiment"]["document"]["label"]
    else:
        return ""

