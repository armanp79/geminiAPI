from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse, QueryDict, response
import requests
import json
import uuid
from datetime import datetime, timedelta
from .models import User
import base64
from rest_framework.parsers import JSONParser 
import keys
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
sandboxURL = "https://exchange.sandbox.gemini.com"
redirectURI = "https://tinyurl.com/4w8wp7k7"
apiURL = "https://api.sandbox.gemini.com"
sandboxClientID = keys.sandboxClientID 
sandboxClientSecret = keys.sandboxClientSecret 

def createAccount(request):
    connectionURL = "{}/auth?client_id={}&response_type=code&redirect_uri={}&state=82350325"\
                    "&scope=orders:create,balances:read,history:read,orders:read,crypto:send"\
                    .format(sandboxURL, sandboxClientID, redirectURI)

    
    return JsonResponse({
        "url": connectionURL
    })

def redirect(request):
    
    params = QueryDict(request.get_full_path().split('?')[1])
    code = params['code']
    state = params['state']
    
    tokenURL = "{}/auth/token".format(sandboxURL)
    tokenData = {
        "client_id": sandboxClientID,
        "client_secret": sandboxClientSecret,
        "code": code,
        "redirect_uri": redirectURI,
        "grant_type": "authorization_code"
    }
    

    headers = {'Content-type': 'application/json'}
    response = requests.post(tokenURL, data=json.dumps(tokenData), headers=headers)
    print(response.json())
    response=response.json()
    accessToken = response['access_token']
    refreshToken = response['refresh_token']
    current_time = datetime.now()
    expirationDate = current_time + timedelta(seconds=response['expires_in'])
    id = uuid.uuid1()
    newUser = User(id = id, accessToken=accessToken, refreshToken=refreshToken, expirationDate=expirationDate)
    newUser.save()
    
    return JsonResponse({
        "id": id
    })


def call(url, token, payload):
    encoded_payload = json.dumps(payload).encode()
    b64 = base64.b64encode(encoded_payload)

    request_headers = { 
        "Authorization": token,
        "X-GEMINI-PAYLOAD": b64
    }

    response = requests.post(url,
        data=None,
        headers=request_headers,
        verify=False
    )
    x = response.json()
    return x

@csrf_exempt
def order(request, id):
    if request.method == "POST":
        
        data = JSONParser().parse(request)
        
        
        user = User.objects.get(pk=id)
        token = "Bearer " + user.accessToken
        url = '{}/v1/order/new'.format(apiURL)

        payload = {
            "request": "/v1/order/new",
            "symbol": data["symbol"],
            "amount": data["amount"],
            "price": data["price"],
            "side": data["side"],
            "type": data["type"],
        }

        orderInfo = call(url, token, payload)
    
        return JsonResponse({"orderInfo": orderInfo})
    else:
        return HttpResponse("Endpoint can only handle POST requests")
    




def history(request, id):
    user = User.objects.get(pk=id)
    token = "Bearer " + user.accessToken
    url = '{}/v1/mytrades'.format(apiURL)

    payload =  {"request": "/v1/mytrades"}
    trades = call(url, token, payload)
    
    
    return JsonResponse({"trades": trades})
       
