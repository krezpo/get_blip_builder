import yaml
import sys
import requests
import uuid
import json

if __name__ == "__main__":

    with open("config.yml") as yaml_file:
        config = yaml.load(yaml_file, Loader=yaml.SafeLoader)

    if config == None:
        sys.exit(-1)
    
    chatbots = config["chatbots"]
    for chatbot in chatbots:

        headers = {'Content-Type' : 'application/json',
                   'Authorization': chatbots[chatbot]['auth']}

        payload = {"id": str(uuid.uuid1()),
                   "method": "get",
                   "uri": "/buckets/blip_portal:builder_published_flow"}
        
        print("Pegando fluxo em PRD do {}".format(chatbots[chatbot]['name']))
        r = requests.post(config["commands_url"], headers=headers, data=json.dumps(payload), timeout=100)

        if r.status_code != 200:
            error = {'error': 'take connection refused for get status {}'.format(chatbots[chatbot]['name'])}
            print(error)
            sys.exit(r.status_code)
        else:
            resource = r.json()["resource"]

            print("Salvando fluxo do {} em {}.json".format(chatbots[chatbot]['name'], chatbot))

            with open("{}/{}.json".format(config["destionation_folder"], chatbot), 'w') as outfile:
                json.dump(resource, outfile, indent=4)

    print("Fim de execução")