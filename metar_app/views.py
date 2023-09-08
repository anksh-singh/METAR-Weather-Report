from django.shortcuts import render
from django.http import JsonResponse
import requests,re
from rest_framework.decorators import api_view
from decouple import config
from django.core.cache import cache

# Create your views here.

@api_view(['GET'])
def fetch_weather_details(request):
    response = {}
    if station_code := request.GET.get('scode', None):
        no_cache = request.GET.get('nocache', '0')
        cache_key = f"metar_data_{station_code}"
        if no_cache == "1":
            data = retrieve_weather_report(station_code)
            cache.set(cache_key, data, 300)       
            # cached_data = cache.get(cache_key)
            # print("cahd", cached_data)
        else:
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                data = cached_data
            else:
                data = retrieve_weather_report(station_code)
 
        return JsonResponse(data)
       

def retrieve_weather_report(station_code):
    extracted_details, response = {}, {}
    if station_code: 
        url = f"{config('BASE_URL')}{station_code}.TXT"
        # metar_report = requests.get(url)
        # # print('resp', metar_report.text)
        # if metar_report.status_code != 200:
        #     return JsonResponse({"message" : "Error while fetching weather details"}, status=403)
        # metar_str = metar_report.text
        metar_str = "2023/09/08 11:55 KHUA 081155Z AUTO 02004KT 9SM CLR 17/17 A2994 RMK AO2 SLP135 T01710169 10185 20163 50002"
        
        wind_pattern = r"(\d{3})(\d{2})KT"
        temp_pattern =r" (\-?\w+|\w+)/(\-?\w+|\w+) "
        date_time_pattern = r"(\d{4}/\d{2}/\d{2}) (\d{2}:\d{2})"

        wind_match = re.search(wind_pattern, metar_str)
        temp_match = re.search(temp_pattern, metar_str)
        date_time_match = re.search(date_time_pattern, metar_str)
       
        if date_time_match:
            date = date_time_match.group(1)
            time = date_time_match.group(2)
            extracted_details['Last_observation'] = f"{date} at {time} GMT"

        if wind_match:
            wind_direction = wind_match.group(1)
            wind_speed_knots = int(wind_match.group(2))
            print("windknott", wind_match)
            wind_speed_mph = round(wind_speed_knots * 1.15078, 2)
        else:
            wind_direction, wind_speed_knots, wind_speed_mph = "Not found", "Not found", "Not found"
        extracted_details["wind"] = {"direction" : f"{wind_direction}degree", "speed" : f"{wind_speed_mph}mph({wind_speed_knots}knots)"}

        if temp_match:
            temp_c_str = temp_match.group(1)
            temp_c =   temp_c_str.replace('M', '-')
            temp_f = round((9/5) * int(temp_c) + 32, 2)
        else:
            temp_c, temp_f = "Not found", "Not found"
        extracted_details['temperature'] = f"{temp_c}C({temp_f} F)"
        
        response["data"] = extracted_details
        response['message'] = "Weather report fetched successfully!"
        return response
            
    
#for testing purpose
def ping(request):
    return JsonResponse({'data': 'pong'})