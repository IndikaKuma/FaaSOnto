import json
import requests

def lambda_handler(event, context):
    repos = {'ApacheOpenwhisk': "https://github.com/apache/openwhisk",
             'Fission': "https://github.com/fission/fission",
             'Knative': "https://github.com/knative/serving",
             'Kubeless': "https://github.com/vmware-archive/kubeless",
             'Nuclio': "https://github.com/nuclio/nuclio",
             'OpenFaaS': "https://github.com/openfaas/faas"}
    github_data = {}
    for repo in repos:
        
        api_url = repos[repo].replace('https://github.com', 'https://api.github.com/repos')
        response = requests.get(api_url)
        response = response.json()
        
        forks = response['forks']
        stars = response['watchers']
        issues = response['open_issues']
        
        github_data[repo] = {"GitHubForks":forks, "GitHubStars": stars, "GitHubIssues":issues}


    
    triples = []
    for repo in github_data:
        for value in github_data[repo]:
            triples.extend([{"graph":(repo), "s": ('faas:' + value) ,"p": 'dul:hasDataValue', "o": github_data[repo][value]},
                            {"graph":(repo), "s": ('faas:' + value) ,"p": 'dul:hasSource', "o": "Github API"}])
    print(triples)
    
    APIGATEWAY_ENDPOINT = "https://06efiaq9xl.execute-api.eu-west-1.amazonaws.com/test/platforms"
    for triple in triples:
        response = requests.put(url=APIGATEWAY_ENDPOINT, params=triple)
        if response.status_code != 200:
            print(response.json()) 

