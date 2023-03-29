import json
from datetime import date
import datetime
import requests
from dateutil.relativedelta import *

"""Gets number of SO question with tag between two dates"""
def get_so_nqs(platform, fromdate, todate):
    fromdate = int(fromdate.timestamp())
    todate = int(todate.timestamp())
    
    payload = {'tagged': platform, 'site': 'stackoverflow', 'filter': 'total', 'fromdate': fromdate, 'todate': todate}
    r = requests.get('https://api.stackexchange.com/2.3/search', params=payload)
    
    
    try:
        return r.json()['total']
    except:
        return 0

def lambda_handler(event, context):
    APIGATEWAY_ENDPOINT = "https://06efiaq9xl.execute-api.eu-west-1.amazonaws.com/test/platforms"
    platforms = {'AWSLambda':"aws-lambda",
                'MicrosoftAzureFunctions': "azure-functions",
                "GoogleCloudFunctions": "google-cloud-functions",
                "Fission": "kubernetes-fission",
                "Knative": "knative",
                "Nuclio": 'nuclio',
                'OpenFaaS': 'openfaas',
                'ApacheOpenwhisk': 'openwhisk',
                'Kubeless': 'kubeless'
    }
    
    todate = datetime.datetime.today()
    fromdate = todate+relativedelta(months=-36)
    triples = []
    for plt in platforms:
        n_so_qs = get_so_nqs(platforms[plt], fromdate, todate)
        triples.extend([
            {"graph":(plt), "s": ('faas:StackoverflowQuestions') ,"p": 'dul:hasDataValue', "o": n_so_qs},
            {"graph":(plt), "s": ('faas:StackoverflowQuestions') ,"p": 'faas:hasSource', "o": "Stackoverflow API"}])
 
    
    for triple in triples:
        response = requests.put(url=APIGATEWAY_ENDPOINT, params=triple)
        if response.status_code != 200:
            print(response.json()) 