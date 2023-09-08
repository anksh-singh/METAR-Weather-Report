# Weather-Report-METAR

## Please Consider:
- OS which I'm suing - MacOS
- Based on my research & Understanding I'm fetching the METAR data in the following ways:
Received data from METAR : 
 "2023/09/08 11:55
KHUA 081155Z AUTO 02004KT 9SM CLR 17/17 A2994 RMK AO2 SLP135 T01710169 10185 20163 50002"

For "Wind" - 02004KT
    Direction - First 3 digits 
    Speed - Next 2 digits in knots (Converted into mph)

For "Temperature" - 17/17
temperature - 17 C & if it had a prefix like M17/17 then temp - -17
Both cases I'm handling 

For "Last observation time" - 2023/09/08 11:55
Date -  2023/09/08
time - 11:55

Fetch METAR weather data for specific station codes. This API returns wind direction, speed, temperature, and last observation time.

## Project Setup

### Clone the Repository

1. Open the terminal.
2. Run the following command to clone the repository:

    ```bash
    git clone https://github.com/anksh-singh/Weather-Report.git
    ```

#Environment Variables

Create a `.env` file in your project root directory and add the following:

```env
BASE_URL=http://tgftp.nws.noaa.gov/data/observations/metar/stations/

##Install Project Dependencies
Command: pip3 install -r requirements.txt

##install redis & Run it locally 
For me - Command: brew install redis (MacOS)  Note : For other OS it may varies
Run redis locally -  brew services start redis

##Run the local server
Comand: python manage.py runserver

##Access the APIs like this: 
http://127.0.0.1:8000/metar/info?scode=KHUA
http://127.0.0.1:8000/metar/info?scode=KHUA&nocache=1

