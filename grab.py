import requests
from collections import defaultdict

urls = []
urls.append("http://www.iudicium.de/")     # Apache/2.4.38 (FreeBSD) OpenSSL/1.0.2r mod_fcgid/2.3.9 mod_wsgi/4.6.5 Python/2.7
urls.append("http://www.gietl-verlag.de/") # nginx/1.14.0 (Ubuntu)
urls.append("http://www.patmos.de/")
urls.append("http://www.swiridoff.de/")

def urls_from_file(filename):
    f = open(filename, "r")
    content = f.read()
    lines = content.split("\n")[1:-1]
    urls = set()
    for line in lines:
        urls.add(line.split(";")[0])
    return urls

def analyze(url):
    print("URL\t\t", url)
    header = get_header(url)
    servers = get_servers(header)

    print("Result:")

    for server in servers:
        print("\tFound", server[0] , "in version", server[1])
    print("")
    return servers


def get_header(url):
    r = requests.get(url)
    print("Statuscode:\t", r.status_code)
    return r

def get_servers(header):
    server_list = ""
    if "Server" in header.headers:
        server_list += header.headers['Server']
        print("Server:\t\t", header.headers['Server'])
    if "X-Powered-By" in header.headers:
        server_list += " " + header.headers['X-Powered-By']
        print("X-Powered-By:\t\t", header.headers['X-Powered-By'])

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
        result.add((name, version))
    return result

results = defaultdict(int)
urls = urls_from_file("91.csv")
print(urls)
for url in urls:
    servers = analyze(url)
    print(servers)
    for server in servers:
        results[server[0] + "/" + server[1]] += 1

print(results)
