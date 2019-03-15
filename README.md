# MassBannerGrab

Bannergrab a lot of websites and filter the result for servers and versions.

# How does it work

MassBannerGrab reads a list of urls from a cvs file.
Each line should contain one url. 
You can also use list exports from https://privacyscore.org/browse/

MassBannerGrab uses python requests to get the header of the website on the given url. 
In the next step it analyzes existing server and version data.
Thouse information are compared to the classifications.json file and, if rated critical, shown.

## Examples

### Example 1: Anti-Virus websites

![Alt text](/screenshots/example_1.png?raw=true "Testing anti-virus websites")

### Example 2: German Cities

![Alt text](/screenshots/example_2.png?raw=true "Testing german cities")


## ToDos:

- use /phpinfo.php
- use /test.php
- use /server-info
- use /server-status
