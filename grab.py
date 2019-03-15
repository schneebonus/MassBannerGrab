import requests
from collections import defaultdict
import json


requests.packages.urllib3.disable_warnings()

urls = []
urls.append("http://www.iudicium.de/")     # Apache/2.4.38 (FreeBSD) OpenSSL/1.0.2r mod_fcgid/2.3.9 mod_wsgi/4.6.5 Python/2.7
urls.append("http://www.gietl-verlag.de/") # nginx/1.14.0 (Ubuntu)
urls.append("http://www.patmos.de/")
urls.append("http://www.swiridoff.de/")

def get_classifications():
    f = open("classification.json", "r")
    classification_json_raw = str(f.read())
    classifications = json.loads(classification_json_raw)
    return classifications

def urls_from_file(filename):
    f = open(filename, "r")
    content = f.read()
    lines = content.split("\n")[1:-1]
    urls = set()
    for line in lines:
        urls.add(line.split(";")[0])
    return urls

def analyze(url):
    #print("URL\t\t", url)
    header = get_header(url)
    servers = get_servers(url, header)

    #print("Result:")

    for server in servers:
        #print("\tFound", server[0] , "in version", server[1])
        pass
    # print("")
    return servers


def get_header(url):
    r = requests.get(url, verify=False, timeout=5.0)
    #print("Statuscode:\t", r.status_code)
    return r

def get_servers(url, header):
    server_list = ""
    if "Server" in header.headers:
        server_list += header.headers['Server'].replace(",", "")
        # print("Server:\t\t", header.headers['Server'])
    if "X-Powered-By" in header.headers:
        server_list += " " + header.headers['X-Powered-By'].replace(",", "")
        # print("X-Powered-By:\t\t", header.headers['X-Powered-By'])

    result = set()
    servers = server_list.split(" ")
    for server in servers:
        if "/" in server:
            name = server.split("/")[0]
            version = server.split("/")[1]
        elif server.startswith("(") and server.endswith(")"):
            name = server[1:-1]
            version = "unknown"
        else:
            name = server
            version = "unknown"
        result.add((name, version, url))
    return result


def is_critical(name, version, classifications):
    if name in classifications:
        for version_accepted in classifications[name]["accepted"]:
            if version.startswith(version_accepted):
                return False
        for version_critical in classifications[name]["critical"]:
            if version.startswith(version_critical):
                return True
    return False

urls = urls_from_file("vpn.csv")

vuln = []
classifications = get_classifications()

for url in urls:
    try:
        servers = analyze(url)
        # print(url)
        # print(servers)
        for server in servers:
            name = server[0]
            version = server[1]
            url = server[2]
            if is_critical(name, version, classifications):
                print(name, "in version", version, "on", url)
    except Exception as e:
        pass
        #print("Error", e)
