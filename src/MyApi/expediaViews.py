import re
import string

import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.



@api_view(["GET"])
def expedia(request):
    try:

        url = "https://www.expedia.com/" + request.query_params.get('url')

        headers = {
            'authority': 'scrapeme.live',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        title = soup.find('h1', class_='uitk-cell all-cell-shrink all-b-padding-half uitk-type-display-700').text

        address = soup.find('div', attrs={'data-stid': 'content-hotel-address'}).text
        lat, lng = extract_lat_lng(soup)

        j = -1
        description = ""

        nodes = soup.find_all('h2', attrs={'class': 'uitk-type-heading-600'})

        for node in nodes :
            #key = node.find('h2', attrs={'class': 'uitk-type-heading-600'}).text
            if node.text == 'About this property':
                for piece in node.find_all('div', attrs={'data-stid': 'content-markup'}):
                    description += piece.text
                break

        languages = ""

        j = -1
        lang = soup.find_all('div', class_='uitk-layout-columns-item uitk-layout-columns-item-force-no-break')
        for i in range(len(lang)):
            if not (lang[i].find('h3', class_='uitk-type-heading-500') is None) and lang[i].find('h3', class_='uitk-type-heading-500').text == "Languages spoken":
                j = i
                break

        if not j == -1:
            lang = lang[j].find('ul').find_all('li')
            languages = ""
            for i in range(len(lang)):
                languages += " " + lang[i].text

        stars = soup.find('div', class_='uitk-rating').find('span', class_='is-visually-hidden')
        if stars is not None:
            stars = stars.text.split()[0]
        else:
            stars = " "

        Object = {
            "title": title,
            "description": description,
            "lat": lat,
            "lng": lng,
            "stars": stars,
            "address": address,
            "languages": languages}

        return JsonResponse(Object, safe=False)

    except ValueError as e:

        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


def extract_lat_lng(soup):
    parent = soup.find('div', attrs={'itemprop': 'geo'})
    lat = ""
    lng = ""
    if parent is not None:
        lat = parent.find('meta', attrs={'itemprop': 'latitude'}).get('content')
        lng = parent.find('meta', attrs={'itemprop': 'longitude'}).get('content')
    return lat, lng
