# MassBannerGrab

Read a list of urls from a cvs file.
Each line should contain one url. You can also use lists from https://privacyscore.org/browse/ .

MassBannerGrab uses python requests to get the header of the website on the given url. 
In the next step it analyzes existing server and version data.
Thouse information are compared to the classifications.json file and, if rated critical, shown.

