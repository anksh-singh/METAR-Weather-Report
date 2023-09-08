from django.shortcuts import render
from django.http import JsonResponse
import requests,re
from rest_framework.decorators import api_view
from decouple import config
from django.core.cache import cache

# Create your views here.


#for testing purpose
def ping(request):
    return JsonResponse({'data': 'pong'})


def retrieve_weather_report(station_code):
    extracted_report = {}
    if station_code: 
        url = f"{config('BASE_URL')}{station_code}.TXT"
        # print("bsss",config('BASE_URL'))
        metar_report = requests.get(url)
        
        # print('resp', response.text)
        # if response.status_code != 200:
        #     return JsonResponse({"message" : "Error while fetching weather details"}, status=404)
        metar_str = metar_report.text
        
        wind_pattern = r"(\d{3})(\d{2})KT"
        temp_pattern =r" (\-?\w+|\w+)/(\-?\w+|\w+) "
        date_time_pattern = r"(\d{4}/\d{2}/\d{2}) (\d{2}:\d{2})"

        wind_match = re.search(wind_pattern, metar_str)
        temp_match = re.search(temp_pattern, metar_str)
        date_time_match = re.search(date_time_pattern, metar_str)
       
    
        if date_time_match:
            date = date_time_match.group(1)
            time = date_time_match.group(2)
            # print("datetimee",date,time)
            # extracted_data['Last_observation'] = f"{date} at {time} GMT"

        if wind_match:
            wind_direction = wind_match.group(1)
            wind_speed_knots = int(wind_match.group(2))
            wind_speed_mph = round(wind_speed_knots * 1.15078, 2)
        else:
            wind_direction, wind_speed_knots, wind_speed_mph = "Not found", "Not found", "Not found"

       
            
        return extracted_report
            
    
    
@api_view(['GET'])
def fetch_weather_details(request):
    if station_code := request.GET.get('scode', None):
        no_cache = request.GET.get('nocache', '0') == '1'

        cache_key = f"metar_{station_code}"
        if no_cache or not cache.get(cache_key):
            data = retrieve_weather_report(station_code)
            cache.set(cache_key, data, timeout=3)  # Cache for 5 minutes
        else:
            data = cache.get(cache_key)

        return JsonResponse({'data': data})
    