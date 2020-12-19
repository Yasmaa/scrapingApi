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
def tripadvisor(request):
    try:

        url = "https://www.tripadvisor.com/" + request.query_params.get('url')
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

        title = soup.find('h1', class_='_1mTlpMC3').text
        address = soup.find('span', class_='_3ErVArsu jke2_wbp').text

        about = soup.find('div', id='ABOUT_TAB')

        description = ""
        description = about.find('div', class_='cPQsENeY')
        if not (description is None):
            description = description.text

        j = -1

        lg = about.find_all('div', class_='ssr-init-26f')

        if not (lg is None):
            for i in range(len(lg)):
                if (lg[i].find('div', class_='_2jJmIDsg') is not None) and lg[i].find('div', class_='_2jJmIDsg').text == "Languages Spoken":
                    j = i
                    break

        languages = ""
        if not (j == -1):
            languages = lg[j].find('div', class_='_2dtF3ueh')
            if not (languages is None):
                languages = languages.text

        rt = about.find('span', {"class": re.compile(r"\b_31OQP7s_\b")})

        stars = ""
        if not (rt is None):
            stars = about.find('span', {"class": re.compile(r"\b_31OQP7s_\b")})['title'].split()[0]

        Object = {
            "title": title,
            "description": description,
            "stars": stars,
            "address": address,
            "languages": languages}

        return JsonResponse(Object, safe=False)

    except ValueError as e:

        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


