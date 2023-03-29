import requests

APIGATEWAY_ENDPOINT = "https://06efiaq9xl.execute-api.eu-west-1.amazonaws.com/test/platforms"
FAASTENER_URL = 'https://raw.githubusercontent.com/faastener/faastener/master/src/assets/data/platforms/'
CRITERIA_MAPPING = {'platform.license': 'License',
 'platform.license.type': 'LicenseType',
 'platform.installation.type': 'InstallationType',
 'platform.installation.targets': 'InstallationTargetHosts',
 'platform.code.availability': 'SourceCodeAvailability',
 'platform.code.repository': 'OpenSourceRepository',
 'platform.code.language': 'ProgrammingLanguage',
 'platform.interface.types': 'InterfaceType',
 'platform.interface.ops.app-mgmt': 'ApplicationManagement',
 'platform.interface.ops.platform-adm': 'PlatformAdministration',
 'platform.github.stars': 'GitHubStars',
 'platform.github.forks': 'GitHubForks',
 'platform.github.issues': 'GitHubIssues',
 'platform.github.commits': 'GitHubCommits',
 'platform.github.contributors': 'GitHubContributors',
 'platform.stackoverflow.questions': 'StackoverflowQuestions',
 'platform.documentation': 'PlatformDocumentation',
 'platform.documentation.functions': 'FunctionsDocumentation',
 'platform.function.runtimes': 'FunctionRuntime',
 'platform.function.runtime-customization': 'RuntimeCustomization',
 'platform.development.ide-support': 'IDEsandTextEditors',
 'platform.function.client-libraries': 'ClientLibraries',
 'platform.quotas.dep-pkg-size': 'DevelopmentPackageSizeQuota',
 'platform.quotas.execution-time': 'DevelopmentExecutionTimeQuota',
 'platform.function.versioning': 'FunctionVersion',
 'platform.function.versioning-app': 'ApplicationVersion',
 'platform.event-source.endpoint.sync-call': 'SynchronousEndpointCall',
 'platform.event-source.endpoint.async-call': 'AsynchronousEndpointCall',
 'platform.event-source.endpoint.customization': 'EndpointCustomization',
 'platform.event-source.endpoint.tls': 'EndpointTLSSupport',
 'platform.event-source.datastore.file-level': 'FileLevel',
 'platform.event-source.datastore.database-mode': 'DatabaseMode',
 'platform.event-source.scheduler': 'Scheduler',
 'platform.event-source.messaging': 'MessageQueue',
 'platform.event-source.streaming': 'StreamProcessingPlatform',
 'platform.event-source.special-purpose-service': 'SpecialPurposeService',
 'platform.event-source.integration': 'EventSourceIntegration',
 'platform.function.orchestrator': 'FunctionOrchestration',
 'platform.function.orchestrator.workflow-definition-type': 'WorkflowDefinition',
 'platform.function.orchestrator.workflow-definition-languages': 'OrchestratingFunctionLanguages',
 'platform.function.orchestrator.control-flow-docs': 'ControlFlowConstructs',
 'platform.function.orchestrator.quotas.execution-time': 'OrchestrationExecutionTimeQuota',
 'platform.function.orchestrator.quotas.io-size': 'OrchestrationTaskIOSizeQuota',
 'platform.testing.functional': 'TestingFunctional',
 'platform.testing.non-functional': 'TestingNonFunctional',
 'platform.debugging.local': 'DebuggingLocal',
 'platform.debugging.remote': 'DebuggingRemote',
 'platform.observability.logging': 'Logging',
 'platform.observability.monitoring': 'Monitoring',
 'platform.observability.integration': 'ToolingIntegration',
 'platform.deployment-automation': 'DeploymentAutomation',
 'platform.ci-cd': 'CICDPipelining',
 'platform.function.marketplaces': 'FunctionMarketplace',
 'platform.function.code-sample-repositories': 'CodeSampleRepository',
 'platform.authentication': 'Authentication',
 'platform.access-control': 'AccessControl'}

# Get platforms data from faastener
url = 'https://raw.githubusercontent.com/faastener/faastener/master/src/assets/data'
response = requests.get(url + '/platforms/platforms.json')
fst_platforms = response.json()

# GENERATES {s:, p:, o:} triples from faastener data

def get_triples(platformName, fst_data):
    namespace = "faas:"
    platform = namespace + platformName.replace(" ", '')
    crits = fst_data['reviewedCriteria'] 
    triples = {}
    for crit in crits:
        value_triples = []
        if len(crits[crit]['values']) != 0:
            values = crits[crit]['values']
            for value in values:
                classname = namespace + value['value'].replace(' ', '') if type(value['value']) == str else value['value']
                label = value['value']
                comment = value['comment'] if 'comment' in value else label
                source = 'FaaStener'
                superclass = namespace + CRITERIA_MAPPING[crit]
                reference = value['reference'] if 'reference' in value else ''

                # exception, 'True' should not become a class
                if classname == True:
                    value_triples.extend([
                                            {"s": platform, "p":namespace + "hasFeature" ,"o": superclass},  
                ])
                
                # exception, 'False' should not become a class
                elif classname == False:
                    pass
                elif type(classname) == int:
                    value_triples.extend([
                                            {"s": superclass, "p":"dul:hasDataValue" ,"o": classname},  
                ])
                else:
                    value_triples.extend([
                                            {"s":classname, "p":"rdfs:subClassOf", "o": superclass}, 
                                            {"s":classname, "p":"rdfs:label", "o": label},
                                            {"s":classname, "p":"rdfs:comment", "o": comment},
                                            {"s":classname, "p":namespace + "hasSource", "o": source},
                                            {"s": platform, "p":namespace + "hasFeature" ,"o": classname,},
                                            {"s": platform, "p":"rdfs:seeAlso" ,"o": reference,}, 


                ])
            triples[crit] = value_triples
    return triples


# for all platforms, retrieve data, generate triples and insert to neptune
for plt in fst_platforms:
    print(plt['id'])
    # get FaaStener data
    fst_data  = requests.get(FAASTENER_URL + plt['id'] +'.json').json()
    
    # generate triples
    triples = get_triples(plt['platformName'], fst_data)
    # PUT requests to API Gateway for all triples
    for criteria in triples:
        # time.sleep(1)
        for triple in triples[criteria]:
            # add graphname to triple
            triple["graph"] = plt['platformName'].replace(' ', '')
            response = requests.put(url=APIGATEWAY_ENDPOINT, params=triple)
            if response.status_code != 200:
                print(response.json()) 
