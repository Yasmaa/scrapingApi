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
def booking(request):
    try:

        url = "https://www.booking.com/" + request.query_params.get('url')

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

        title = soup.find('h2', class_='fn')
        if (title.find('span') is not None):
            title.span.decompose()
        title = title.text.strip()

        address = soup.find('span', attrs={'class': 'hp_address_subtitle'}).text.strip()
        latLng = soup.find('a', attrs={'id': 'hotel_address'}).get('data-atlas-latlng')
        lat = ""
        lng = ""
        if latLng is not None:
            lat, lng = latLng.split(',')


        about = soup.find('div', id='property_description_content')
        desc = about.find_all('p')
        description = " "
        if not desc is None:

            for p in range(len(desc)):
                description += (desc[p].text)

        j = -1
        tl = soup.find_all('div', class_='facilitiesChecklistSection')
        if not tl is None:
            if not tl is None:
                for i in range(len(tl)):
                    if tl[i].find('h5').text.translate({ord(c): None for c in string.whitespace}) == "Languagesspoken":
                        j = i
                        break

        languages = " "
        if not (j == -1):
            tl = tl[j].find_all('li')
            for i in range(len(tl)):
                languages += tl[i].text.translate({ord(c): None for c in string.whitespace}) + ", "
            languages = languages[:-2]

        stars = soup.find('span', class_="hp__hotel_ratings").find('span', class_="invisible_spoken")
        if not stars is None:
            stars = stars.text.split()[0][0]
        else:
            stars = " "

        Object = {
            "title": title,
            "description": description,
            "stars": stars,
            "address": address,
            "lat": lat,
            "lng": lng,
            "languages": languages}

        return JsonResponse(Object, safe=False)

    except ValueError as e:

        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)



