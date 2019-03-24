import requests
from bs4 import BeautifulSoup
import re

PHP_HEADLINE_REGEX = "^PHP Version (.*)$"

def get_php_version_from_headline(soup):
    line = soup.select('h1.p')[0].text.strip()
    re_line = re.match(PHP_HEADLINE_REGEX, line)
    version = re_line.group(1)
    return version

def process_tables(soup, list_of_keywords):
    result = {}
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) is 2 and cols[0].text.strip() in list_of_keywords:
                result[cols[0].text.strip()] = cols[1].text.strip()
    return result

def get_curl_version(soup):
    key = "cURL Information"
    result = " "
    content = process_tables(soup, [key])
    if key in content:
        result += "cURL/" + content[key]
    return result

def get_ssl_version(soup):
    # SSL Version
    # OpenSSL Library Version
    # OpenSSL Header Version
    result = ""
    content = process_tables(soup, ["SSL Version", "OpenSSL Library Version", "OpenSSL Header Version"])
    if "SSL Version" in content:
        result += " " + content["SSL Version"]
    '''
    if "OpenSSL Library Version" in content:
        result += " " + content["OpenSSL Library Version"]
    if "OpenSSL Header Version" in content:
        result += " " + content["OpenSSL Header Version"]
    '''
    return result

def get_libssh_version(soup):
    key = "libSSH Version"
    result = " "
    content = process_tables(soup, [key])
    if key in content:
        result += content[key]
    return result

def get_exif_version(soup):
    key = "EXIF Version"
    result = " "
    content = process_tables(soup, [key])
    if key in content:
        result += "EXIF/" + content[key]
    return result

def get_zip_version(soup):
    # Zip version
    # Libzip version
    result = ""
    content = process_tables(soup, ["Zip version", "Libzip version"])
    if "Zip version" in content:
        result += " zip/" + content["Zip version"]
    if "Libzip version" in content:
        result += " libzip/" + content["Libzip version"]
    return result

def process_php_variables(soup):
    key = "$_SERVER['SERVER_SOFTWARE']"
    result = " "
    content = process_tables(soup, [key])
    if key in content:
        result += content[key]
    return result

def process_url(url):
    check_files = ["phpinfo.php", "test.php"]
    result = " "
    for file in check_files:
        get_url = requests.get(url + file)
        if get_url.status_code == requests.codes.ok:
            get_text = get_url.text
            soup = BeautifulSoup(get_text, "html.parser")
            php_version = "PHP/" + get_php_version_from_headline(soup)
            result += php_version
            php_variables = process_php_variables(soup)
            result += php_variables
            zip_versions = get_zip_version(soup)
            result += zip_versions
            exif_version = get_exif_version(soup)
            result += exif_version
            libssh_version = get_libssh_version(soup)
            result += libssh_version
            ssl_version = get_ssl_version(soup)
            result += ssl_version
            curl_version = get_curl_version(soup)
            result += curl_version

    return result
