import yaml
import sys
import requests
import uuid
import json

URL = "<URL_COMMANDS>"

if __name__ == "__main__":

    with open("config.yml") as yaml_file:
        config = yaml.load(yaml_file, Loader=yaml.SafeLoader)

    if config == None:
        sys.exit(-1)
    
    for bot in config:
        #print(bot, config[bot])

        headers = {'Content-Type' : 'application/json',
                   'Authorization': config[bot]['auth']}

        payload = {"id": str(uuid.uuid1()),
                   "method": "get",
                   "uri": "/buckets/blip_portal:builder_published_flow"}
        
        print("Pegando fluxo em PRD do {}".format(config[bot]['name']))
        r = requests.post(URL, headers=headers, data=json.dumps(payload), timeout=100)

        if r.status_code != 200:
            error = {'error': 'take connection refused for get status {}'.format(config[bot]['name'])}
            print(error)
            sys.exit(r.status_code)
        else:
            resource = r.json()["resource"]

            print("Salvando fluxo do {} em {}.json".format(config[bot]['name'], bot))

            with open("..\\builder\{}.json".format(bot), 'w') as outfile:
                json.dump(resource, outfile, indent=4)

    print("Fim de execução")