from __future__  import print_function
import requests
import json

# chevk object for input type
def check_o(o):
    if type(o) == int:
        return o
    elif ':' in o:
        return o
    else:
        o = f'"{o}"'
        return o

def lambda_handler(event, context):
    # payload
    params = event['queryStringParameters']
    params["o"] = check_o(params['o'])
    if 'graph' not in params:
        # generate query w/ params
        query = "PREFIX faas: <http://www.semanticweb.org/stijn/ontologies/2022/4/faasdss#> \
            PREFIX dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#> \
            INSERT DATA   {{ GRAPH <http://aws.amazon.com/neptune/vocab/v01/FaaSonto_base>  {{ {s} {p} {o} .}} }}"
    
        # query = query.format(s=params["s"], p = params["p"], o=params["o"] if ':' in params["o"] else f'"{params["o"]}"')
        query = query.format(**params)
    else: 
        # generate query w/ params
        query = "PREFIX faas: <http://www.semanticweb.org/stijn/ontologies/2022/4/faasdss#> \
                PREFIX dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#> \
                INSERT DATA {{ GRAPH faas:{graph}  {{ {s} {p} {o} .}} }}"
        
        # query = query.format(graph=params['graph'],s=params["s"], p = params["p"], o=params["o"] if ':' in params["o"] else f'"{params["o"]}"')
        query = query.format(graph=params['graph'],s=params["s"], p = params["p"], o=params["o"] )
    print(query)
    
    url = 'https://database-1-sg-instance-1ca.csbkotxlmqjb.eu-west-1.neptune.amazonaws.com:8182/sparql'
    data = {'update': query}
    response = requests.post(url=url, data=data)
    
    print(response.json())

    lambda_response = {
    "isBase64Encoded": False,
    "statusCode":response.status_code,
    "headers": { "Access-Control-Allow-Origin": "*"},
    "body": json.dumps(response.json())
    }
    
    print(type(lambda_response))
    
    return lambda_response


