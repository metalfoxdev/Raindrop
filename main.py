import os
import requests
import json
import zipfile
import pickle
from termcolor import colored
import pyfiglet
from datetime import datetime
import sys
import time

version = "1.0"
seperator = "----------------------------------------"
spacer = "                                        "
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def cs():
    os.system("cls||clear")

def json_extract(obj, path):
    '''
    Extracts an element from a nested dictionary or
    a list of nested dictionaries along a specified path.
    If the input is a dictionary, a list is returned.
    If the input is a list of dictionary, a list of lists is returned.
    obj - list or dict - input dictionary or list of dictionaries
    path - list - list of strings that form the path to the desired element
    '''
    def extract(obj, path, ind, arr):
        '''
            Extracts an element from a nested dictionary
            along a specified path and returns a list.
            obj - dict - input dictionary
            path - list - list of strings that form the JSON path
            ind - int - starting index
            arr - list - output list
        '''
        key = path[ind]
        if ind + 1 < len(path):
            if isinstance(obj, dict):
                if key in obj.keys():
                    extract(obj.get(key), path, ind + 1, arr)
                else:
                    arr.append(None)
            elif isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        extract(item, path, ind, arr)
            else:
                arr.append(None)
        if ind + 1 == len(path):
            if isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        arr.append(item.get(key, None))
            elif isinstance(obj, dict):
                arr.append(obj.get(key, None))
            else:
                arr.append(None)
        return arr
    if isinstance(obj, dict):
        return extract(obj, path, 0, [])
    elif isinstance(obj, list):
        outer_arr = []
        for item in obj:
            outer_arr.append(extract(item, path, 0, []))
        return outer_arr
def degToCompass(num):
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return arr[(val % 16)]
def wc_extract(wc):
    wc = str(wc)
    if wc == "0":
        return colored("-Clear Sky-", "light_yellow")
    elif wc == "1":
        return colored("-Mainly Clear-", "blue")
    elif wc == "2":
        return colored("-Partly Cloudy-", "light_blue")
    elif wc == "3":
        return colored("-Overcast-", "dark_grey")
    elif wc == "45":
        return colored("-Fog-", "light_grey")
    elif wc == "48":
        return colored("-Rime Fog-", "dark_grey")
    elif wc == "51":
        return colored("-Light Drizzle-", "cyan")
    elif wc == "53":
        return colored("-Moderate Drizzle-", "light_blue")
    elif wc == "55":
        return colored("-Heavy Drizzle-", "blue")
    elif wc == "56":
        return colored("-Light Freezing Drizzle-", "white")
    elif wc == "57":
        return colored("-Heavy Freezing Drizzle-", "white")
    elif wc == "61":
        return colored("-Light Rain-", "cyan")
    elif wc == "63":
        return colored("-Moderate Rain-", "light_blue")
    elif wc == "65":
        return colored("-Heavy Rain-", "blue")
    elif wc == "66":
        return colored("-Light Freezing Rain-", "white")
    elif wc == "67":
        return colored("-Heavy Freezing Rain-", "white")
    elif wc == "71":
        return colored("-Light Snow-", "white")
    elif wc == "73":
        return colored("-Moderate Snow-", "white")
    elif wc == "75":
        return colored("-Heavy Snow-", "white")
    elif wc == "77":
        return colored("-Snow Grains-", "light_grey")
    elif wc == "80":
        return colored("-Light Rain Showers-", "cyan")
    elif wc == "81":
        return colored("-Moderate Rain Showers-", "light_blue")
    elif wc == "82":
        return colored("-Heavy Rain Showers-", "blue")
    elif wc == "85":
        return colored("-Light Snow Showers-", "white")
    elif wc == "86":
        return colored("-Heavy Snow Showers-", "white")
    elif wc == "95":
        return colored("-Thunderstorms-", "yellow")
    elif wc == "96":
        return colored("-Thunderstorms with Light Hail-", "yellow")
    elif wc == "99":
        return colored("-Thunderstorms with Heavy Hail-", "light_red")

def color_temp(temp, unit):
    if unit == "fahrenheit":
        temp = float(temp)
        if temp >= 86:
            return colored(str(temp), "light_red")
        elif temp >= 68:
            return colored(str(temp), "yellow")
        elif temp >= 50:
            return colored(str(temp), "cyan")
        elif temp >= 32:
            return colored(str(temp), "light_blue")
        elif temp >= 14:
            return colored(str(temp), "blue")
        elif temp <= 14:
            return colored(str(temp), "white")
    else:
        temp = float(temp)
        if temp >= 30:
            return colored(str(temp), "light_red")
        elif temp >= 20:
            return colored(str(temp), "yellow")
        elif temp >= 10:
            return colored(str(temp), "cyan")
        elif temp >= 0:
            return colored(str(temp), "light_blue")
        elif temp >= -10:
            return colored(str(temp), "blue")
        elif temp <= -10:
            return colored(str(temp), "white")
def color_wind(wind, unit):
    wind = float(wind)
    if unit == "mph":
        if wind <= 15:
            return colored(str(wind), "green")
        elif wind <= 35:
            return colored(str(wind), "light_yellow")
        elif wind <= 60:
            return colored(str(wind), "red")
        else:
            return colored(str(wind), "magenta")
    elif unit == "kmh":
        if wind <= 24:
            return colored(str(wind), "green")
        elif wind <= 56:
            return colored(str(wind), "light_yellow")
        elif wind <= 96:
            return colored(str(wind), "red")
        else:
            return colored(str(wind), "magenta")
    elif unit == "ms":
        if wind <= 7:
            return colored(str(wind), "green")
        elif wind <= 16:
            return colored(str(wind), "light_yellow")
        elif wind <= 27:
            return colored(str(wind), "red")
        else:
            return colored(str(wind), "magenta")
    elif unit == "kn":
        if wind <= 13:
            return colored(str(wind), "green")
        elif wind <= 30:
            return colored(str(wind), "light_yellow")
        elif wind <= 52:
            return colored(str(wind), "red")
        else:
            return colored(str(wind), "magenta")
def color_uv(uv):
    uv = float(uv)
    if uv <= 2:
        return colored(str(uv), "green")
    elif uv <= 5:
        return colored(str(uv), "light_yellow")
    elif uv <= 10:
        return colored(str(uv), "red")
    elif uv > 10:
        return colored(str(uv), "magenta")
def create_hourly_entry(hour, temperature, rain,  weathercode, windspeed, winddirection, snowfall, precipitation_probability, snow_depth):
    if hour == "Now":
        if temp_unit == "celsius":
            output = colored(str(hour), "white") + " - " + wc_extract(weathercode).replace("-", "") + colored(", ", "white") + color_temp(temperature, temp_unit) + colored("°C, ", "white") + color_wind(windspeed, wind_unit) + colored(str(wind_unit), "white") + colored(" (", "white") + colored(str(degToCompass(winddirection)), "light_yellow") + colored(")", "white")
        elif temp_unit == "fahrenheit":
            output = colored(str(hour), "white") + " - " + wc_extract(weathercode).replace("-", "") + colored(", ", "white") + color_temp(temperature, temp_unit) + colored("°F, ", "white") + color_wind(windspeed, wind_unit) + colored(str(wind_unit), "white") + colored(" (", "white") + colored(str(degToCompass(winddirection)), "light_yellow") + ")"
    else:
        if temp_unit == "celsius":
            output = colored(str(hour) + ":00 - ", "white") + wc_extract(weathercode).replace("-", "") + colored(", ", "white") + color_temp(temperature, temp_unit) + colored("°C, ", "white") + color_wind(windspeed, wind_unit) + colored(str(wind_unit), "white") + colored(" (", "white") + colored(str(degToCompass(winddirection)), "light_yellow") + colored(")", "white")
        elif temp_unit == "fahrenheit":
            output = colored(str(hour) + ":00 - ", "white") + wc_extract(weathercode).replace("-", "") + colored(", ", "white") + color_temp(temperature, temp_unit) + colored("°F, ", "white") + color_wind(windspeed, wind_unit) + colored(str(wind_unit), "white") + colored(" (", "white")+ colored(str(degToCompass(winddirection)), "light_yellow") + colored(")", "white")
    if not str(rain) == "0.0":
        output += colored(", ", "white") + colored(str(rain), "light_blue") + colored(str(precip_unit), "white") + colored(" (", "white") + colored(str(precipitation_probability), "blue") + colored("%)", "white")
    if not str(snowfall) == "0.0":
        output += colored(", ", "white") + colored(str(snowfall), "blue") + colored("cm", "white") + colored(" (", "white") + colored(str(snow_depth), "light_blue") + colored("m", "white") + colored(")", "white")
    return str(output)

def create_daily_entry(date, month, day, weathercode, temperature_2m_min, temperature_2m_max, uv_index_max, precipitation_sum, precipitation_probability_mean, windgusts_10m_max, temp_unit, precip_unit):
    if temp_unit == "fahrenheit":
        if precip_unit == "mm":
            output = colored(str(date) + "/" + str(month) + ": " + str(day) + " - " , "white") + wc_extract(weathercode).replace("-", "") + colored(", ", "white") + colored(str(temperature_2m_min), "blue") + colored("°F", "white") + colored(" : ", "white") + colored(str(temperature_2m_max), "light_red") + colored("°F", "white") + colored(", ", "white") + color_uv(uv_index_max) + colored(" UV, ", "white") + color_wind(windgusts_10m_max, wind_unit) + " " + colored(str(wind_unit), "white") + colored(", ", "white") +colored(str(precipitation_sum), "light_blue") + colored(str(precip_unit), "white") + colored(" (", "white") + colored(str(precipitation_probability_mean), "blue") + colored("%", "white") + colored(")", "white")
        else:
            precip_inch = str(precipitation_sum / 25.4)
            precip_inch = precip_inch[0:3]
            output = colored(str(date) + "/" + str(month) + ": " + str(day) + " - " , "white") + wc_extract(weathercode).replace("-", "") + colored(", ", "white") + colored(str(temperature_2m_min), "blue") + colored("°F", "white") + colored(" : ", "white") + colored(str(temperature_2m_max), "light_red") + colored("°F", "white") + colored(", ", "white") + color_uv(uv_index_max) + colored(" UV, ", "white") + color_wind(windgusts_10m_max, wind_unit) + " " + colored(str(wind_unit), "white") + colored(", ", "white") + colored(str(precip_inch), "light_blue") + colored(str(precip_unit), "white") + colored(" (", "white") + colored(str(precipitation_probability_mean), "blue") + colored("%", "white") + colored(")", "white")
    elif temp_unit == "celsius":
        if precip_unit == "mm":
            output = colored(str(date) + "/" + str(month) + ": " + str(day) + " - " , "white") + wc_extract(weathercode).replace("-", "") + colored(", ", "white") + colored(str(temperature_2m_min), "blue") + colored("°C", "white") + colored(" : ", "white") + colored(str(temperature_2m_max), "light_red") + colored("°C", "white") + colored(", ", "white") + color_uv(uv_index_max) + colored(" UV, ", "white") + color_wind(windgusts_10m_max, wind_unit) + " " + colored(str(wind_unit), "white") + colored(", ", "white") +colored(str(precipitation_sum), "light_blue") + colored(str(precip_unit), "white") + colored(" (", "white") + colored(str(precipitation_probability_mean), "blue") + colored("%", "white") + colored(")", "white")
        else:
            precip_inch = str(precipitation_sum / 25.4)
            precip_inch = precip_inch[0:3]
            output = colored(str(date) + "/" + str(month) + ": " + str(day) + " - " , "white") + wc_extract(weathercode).replace("-", "") + colored(", ", "white") + colored(str(temperature_2m_min), "blue") + colored("°C", "white") + colored(" : ", "white") + colored(str(temperature_2m_max), "light_red") + colored("°C", "white") + colored(", ", "white") + color_uv(uv_index_max) + colored(" UV, ", "white") + color_wind(windgusts_10m_max, wind_unit) + " " + colored(str(wind_unit), "white") + colored(", ", "white") + colored(str(precip_inch), "light_blue") + colored(str(precip_unit), "white") + colored(" (", "white") + colored(str(precipitation_probability_mean), "blue") + colored("%", "white") + colored(")", "white")
    return str(output)

while True:
    if os.path.isfile("raindrop.config"):
        cs()
        gh_version = requests.get("https://raw.githubusercontent.com/metalfoxdev/Raindrop/main/version.txt").content
        gh_version = gh_version.replace("b", "").replace("\n", "").replace("'", "")
        input("")
        if version == str(gh_version):
            pass
        else:
            print("Updating Raindrop...")
            f = open("new_main.py", "wb")
            f.write(requests.get("https://raw.githubusercontent.com/metalfoxdev/Raindrop/main/main.py").content)
            f.close()
            os.remove("main.py")
            os.rename("new_main.py", "main.py")
            cs()
            print("Update complete! \nPress ENTER to close Raindrop, you need to re open it when it closes...")
            input("")
            quit()
        print("loading config...")
        with zipfile.ZipFile("raindrop.config", mode="r") as config:
            config.extractall()
            f = open("latitude.rdd", "rb")
            latitude = pickle.load(f)
            f.close()
            f = open("longitude.rdd", "rb")
            longitude = pickle.load(f)
            f.close()
            f = open("location_name.rdd", "rb")
            location_name = pickle.load(f)
            f.close()
            f = open("precip_unit.rdd", "rb")
            precip_unit = pickle.load(f)
            f.close()
            f = open("temp_unit.rdd", "rb")
            temp_unit = pickle.load(f)
            f.close()
            f = open("wind_unit.rdd", "rb")
            wind_unit = pickle.load(f)
            f.close()
            os.remove("latitude.rdd")
            os.remove("longitude.rdd")
            os.remove("location_name.rdd")
            os.remove("precip_unit.rdd")
            os.remove("temp_unit.rdd")
            os.remove("wind_unit.rdd")
        print("config loaded")
        cs()
        print("retrieving weather...")
        wurl = "https://api.open-meteo.com/v1/forecast?latitude=" + str(latitude) + "&longitude=" + str(longitude) + "&current_weather=true&hourly=temperature_2m,rain,showers,snowfall,snow_depth,weathercode,visibility,windspeed_10m,winddirection_10m,precipitation_probability&daily=weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_sum,rain_sum,showers_sum,snowfall_sum,precipitation_probability_mean,windgusts_10m_max&windspeed_unit=" + wind_unit + "&timezone=auto&temperature_unit=" + temp_unit + "&precipitation_unit=" + precip_unit
        wjson = requests.get(wurl).content
        wjson = json.loads(wjson)
        print("weather retrieved successfully")
        cs()
        mode = "main"
        while True:
            cs()
            print(spacer + colored("Raindrop v" + version, "magenta"))
            if mode == "main":
                print(spacer + colored("Weather data by Open Meteo", "blue"))
                print(" ")
                calendar = datetime.fromisoformat(json_extract(wjson, ["current_weather", "time"])[0])
                print(colored(seperator + "Current Weather for " + str(location_name) + seperator, "white"))
                print(spacer + wc_extract(str(json_extract(wjson, ["current_weather", "weathercode"])[0])))
                if temp_unit == "celsius":
                    print(spacer + colored("Temperature: ", "white") + color_temp(str(json_extract(wjson, ["current_weather", "temperature"])[0]), temp_unit) + colored("°C", "white"))
                else:
                    print(spacer + colored("Temperature: ", "white") + color_temp(str(json_extract(wjson, ["current_weather", "temperature"])[0]), temp_unit) + colored("°F", "white"))
                print(spacer + colored("Wind Direction: ", "white") + colored(str(degToCompass(json_extract(wjson, ["current_weather", "winddirection"])[0])), "green"))
                print(spacer + colored("Wind Speed: ", "white") + color_wind(str(json_extract(wjson, ["current_weather", "windspeed"])[0]), str(wind_unit)) + colored(str(wind_unit), "white"))
                print(" ")
                print(colored(seperator + "Forecasts for " + str(location_name) + seperator, "white"))
                print(spacer + colored("[", "white") + colored("1", "light_green") + colored("]", "white") + colored(" Hourly", "light_yellow"))
                print(spacer + colored("[", "white") + colored("2", "light_green") + colored("]", "white") + colored(" Daily", "light_yellow"))
                ans = input("> ")
                if ans == "quit":
                    cs()
                    quit()
                elif ans == "refresh":
                    cs()
                    print("retrieving weather...")
                    wjson = requests.get(wurl).content
                    wjson = json.loads(wjson)
                    print("weather retrieved successfully")
                    cs()
                elif ans == "1":
                    mode = "hourly"
                    hourly_mode = 1
                    # mode 1 = show hourly weather for current day.
                    # mode 2 = show hourly weather for selected day from within the daily forecast menu
                elif ans == "2":
                    mode = "daily"
                    # implement daily forecast system. Show daily forecast but then give ability to see hourly for each day by selecting results.
                elif ans == "config":
                    cs()
                    print("Are you sure you want to reconfigure Raindrop?")
                    print("[1] Yes")
                    print("[2] No\n")
                    ans = input("> ")
                    if ans == "1":
                        cs()
                        os.remove("raindrop.config")
                        print("config deleted, re-run Raindrop to set it up again!")
                        quit()
                    else:
                        pass
                else:
                    cs()
            elif mode == "hourly":
                if hourly_mode == 1:
                    cs()
                    hourly_output = []
                    temp = []
                    print("loading weather data...")
                    for x in range(len(json_extract(wjson, ["hourly", "time"])[0])):
                        if datetime.fromisoformat(json_extract(wjson, ["hourly", "time"])[0][x]).day == calendar.day:
                            temp.append(str(json_extract(wjson, ["hourly", "time"])[0][x]))
                    for x in range(len(temp)):
                        if datetime.fromisoformat(temp[x]).hour == calendar.hour:
                            hourly_output.append(create_hourly_entry("Now", json_extract(wjson, ["hourly", "temperature_2m"])[0][x], json_extract(wjson, ["hourly", "rain"])[0][x], json_extract(wjson, ["hourly", "weathercode"])[0][x], json_extract(wjson, ["hourly", "windspeed_10m"])[0][x], json_extract(wjson, ["hourly", "winddirection_10m"])[0][x], json_extract(wjson, ["hourly", "snowfall"])[0][x], json_extract(wjson, ["hourly", "precipitation_probability"])[0][x], json_extract(wjson, ["hourly", "snow_depth"])[0][x]))
                        if datetime.fromisoformat(temp[x]).hour > calendar.hour:
                            hourly_output.append(create_hourly_entry(datetime.fromisoformat(temp[x]).hour, json_extract(wjson, ["hourly", "temperature_2m"])[0][x], json_extract(wjson, ["hourly", "rain"])[0][x], json_extract(wjson, ["hourly", "weathercode"])[0][x], json_extract(wjson, ["hourly", "windspeed_10m"])[0][x], json_extract(wjson, ["hourly", "winddirection_10m"])[0][x], json_extract(wjson, ["hourly", "snowfall"])[0][x], json_extract(wjson, ["hourly", "precipitation_probability"])[0][x], json_extract(wjson, ["hourly", "snow_depth"])[0][x]))
                    print("data loaded")
                    cs()
                    print(colored(seperator + "Hourly Forecast" + seperator, "white"))
                    for x in range(len(hourly_output)):
                        print("\n" + spacer + hourly_output[x])
                    ans = input("> ")
                    if ans == "quit":
                        cs()
                        quit()
                    elif ans == "back":
                        cs()
                        mode = "main"
                    elif ans == "refresh":
                        cs()
                        print("retrieving weather...")
                        wjson = requests.get(wurl).content
                        wjson = json.loads(wjson)
                        print("weather retrieved successfully")

                elif hourly_mode == 2:
                    cs()
                    hourly_output = []
                    for x in range(len(json_extract(wjson, ["hourly", "time"])[0])):
                        if datetime.fromisoformat(json_extract(wjson, ["hourly", "time"])[0][x]).day == datetime.fromisoformat(json_extract(wjson, ["daily", "time"])[0][day_choice-1]).day:
                            hourly_output.append(create_hourly_entry(datetime.fromisoformat(json_extract(wjson, ["hourly", "time"])[0][x]).hour, json_extract(wjson, ["hourly", "temperature_2m"])[0][x], json_extract(wjson, ["hourly", "rain"])[0][x], json_extract(wjson, ["hourly", "weathercode"])[0][x], json_extract(wjson, ["hourly", "windspeed_10m"])[0][x], json_extract(wjson, ["hourly", "winddirection_10m"])[0][x], json_extract(wjson, ["hourly", "snowfall"])[0][x], json_extract(wjson, ["hourly", "precipitation_probability"])[0][x], json_extract(wjson, ["hourly", "snow_depth"])[0][x]))
                    print(colored(seperator + "Hourly Forecast for " + days[datetime.fromisoformat(json_extract(wjson, ["daily", "time"])[0][day_choice-1]).weekday()] + ", " + str(datetime.fromisoformat(json_extract(wjson, ["daily", "time"])[0][day_choice-1]).day) + "/" + str(datetime.fromisoformat(json_extract(wjson, ["daily", "time"])[0][day_choice-1]).month) + "/" +  str(datetime.fromisoformat(json_extract(wjson, ["daily", "time"])[0][day_choice-1]).year) + seperator, "white"))
                    for x in range(len(hourly_output)):
                        print("\n" + spacer + hourly_output[x])
                    ans = input("> ")
                    if ans == "quit":
                        cs()
                        quit()
                    elif ans == "back":
                        mode = "daily"
                    elif ans == "refresh":
                        cs()
                        print("retrieving weather...")
                        wjson = requests.get(wurl).content
                        wjson = json.loads(wjson)
                        print("weather retrieved successfully")

            elif mode == "daily":
                cs()
                daily_output = []
                print("loading weather data...")
                for x in range(len(json_extract(wjson, ["daily", "time"])[0])):
                    if datetime.fromisoformat(json_extract(wjson, ["daily", "time"])[0][x]).day == calendar.day:
                        pass
                    else:
                        day_number = datetime.fromisoformat(json_extract(wjson, ["daily", "time"])[0][x]).weekday()
                        day = days[day_number]
                        daily_output.append(create_daily_entry(datetime.fromisoformat(json_extract(wjson, ["daily", "time"])[0][x]).day, datetime.fromisoformat(json_extract(wjson, ["daily", "time"])[0][x]).month, str(day), json_extract(wjson, ["daily", "weathercode"])[0][x], json_extract(wjson, ["daily", "temperature_2m_min"])[0][x], json_extract(wjson, ["daily", "temperature_2m_max"])[0][x], json_extract(wjson, ["daily", "uv_index_max"])[0][x], json_extract(wjson, ["daily", "precipitation_sum"])[0][x], json_extract(wjson, ["daily", "precipitation_probability_mean"])[0][x], json_extract(wjson, ["daily", "windgusts_10m_max"])[0][x], temp_unit, precip_unit))
                print("data loaded")
                cs()
                num_skip = True
                print(colored(seperator + "Daily Forecast" + seperator, "white"))
                for x in range(len(daily_output)):
                    print("\n" + spacer + colored("[", "white") + colored(str(x+1), "light_green") + colored("] ", "white") + daily_output[x])

                ans = input("> ")
                if ans == "quit":
                    cs()
                    quit()
                elif ans == "back":
                    mode = "main"
                elif ans == "refresh":
                    cs()
                    print("retrieving weather...")
                    wjson = requests.get(wurl).content
                    wjson = json.loads(wjson)
                    print("weather retrieved successfully")
                try:
                    if int(ans) == 1 or int(ans) == 2 or int(ans) == 3 or int(ans) == 4 or int(ans) == 5 or int(ans) == 6:
                        cs()
                        day_choice = int(ans)
                        mode = "hourly"
                        hourly_mode = 2
                except ValueError:
                    pass

    else:
        cs()
        print("Hello, and welcome to Raindrop!")
        print("This guided setup will ask questions such as locations and units and set up Raindrop according to your answers!")
        input("Press ENTER to continue...")
        cs()
        loc_chosen = False
        while loc_chosen == False:
            cs()
            print("Firstly, you must search for your location.")
            print("Search for a location below:")
            ans = input("> ")
            cs()
            loc_results = requests.get("https://geocoding-api.open-meteo.com/v1/search?name=" + ans + "&language=en&count=10&format=json").content
            loc_results = json.loads(loc_results)
            try:
                results = loc_results["results"]
            except KeyError:
                print("No Results, reboot Raindrop then try again")
                quit()
            print("Pick a location: \n")
            for x in range(len(results)):
                print(str("[" + str(x+1) + "] " + results[x]["name"] + ", " + results[x]["admin1"] + ", " + results[x]["country"] + " (" + results[x]["timezone"].replace("_", " ") + ")"))
            ans = input("> ")
            try:
                if int(ans) > 10 or int(ans) < 1:
                    cs()
                    print("Invalid index number! Try again!")
                    pass
                else:
                    try:
                        location_name = str(results[int(ans)-1]["name"] + ", " + results[int(ans)-1]["admin1"])
                        latitude = results[int(ans)-1]["latitude"]
                        longitude = results[int(ans)-1]["longitude"]
                        loc_chosen = True
                    except IndexError:
                        pass
            except ValueError:
                pass
        cs()
        print("Choose a unit type for snow and rain precipitation.")
        print("[1] mm")
        print("[2] inch")
        ans = input("> ")
        if ans == "1":
            precip_unit = "mm"
        else:
            precip_unit = "inch"
        cs()
        print("Choose a unit type for temperature measurement.")
        print("[1] Celsius")
        print("[2] Fahrenheit")
        ans = input("> ")
        if ans == "1":
            temp_unit = "celsius"
        else:
            temp_unit = "fahrenheit"
        cs()
        print("Choose a unit type for wind speed measurement")
        print("[1] mph")
        print("[2] kmh")
        print("[3] ms")
        print("[4] kn")
        ans = input("> ")
        if ans == "1":
            wind_unit = "mph"
        elif ans == "2":
            wind_unit = "kmh"
        elif ans == "3":
            wind_unit = "ms"
        else:
            wind_unit = "kn"
        cs()
        print("Your settings are as follows:")
        print(" ")
        print("Location: " + location_name.title())
        print("Precipitation Unit: " + precip_unit)
        print("Temperature Unit: " + temp_unit)
        print("Wind Speed Unit: " + wind_unit)
        print(" ")
        print("If all of the above is correct, press ENTER to write your preferences to a file. If you are unhappy with your preferences, type quit into the command line below and restart Raindrop to begin setup again.")
        ans = input("\n> ")
        if ans == "quit":
            quit()
        else:
            pass
        cs()
        print("Saving preferences...")
        with zipfile.ZipFile("raindrop.config", mode="w") as config:
            f = open("latitude.rdd", "wb")
            pickle.dump(latitude, f)
            f.close()
            f = open("longitude.rdd", "wb")
            pickle.dump(longitude, f)
            f.close()
            f = open("precip_unit.rdd", "wb")
            pickle.dump(precip_unit, f)
            f.close()
            f = open("temp_unit.rdd", "wb")
            pickle.dump(temp_unit, f)
            f.close()
            f = open("wind_unit.rdd", "wb")
            pickle.dump(wind_unit, f)
            f.close()
            f = open("location_name.rdd", "wb")
            pickle.dump(location_name.title(), f)
            f.close()
            config.write("latitude.rdd")
            config.write("longitude.rdd")
            config.write("precip_unit.rdd")
            config.write("temp_unit.rdd")
            config.write("wind_unit.rdd")
            config.write("location_name.rdd")
            os.remove("latitude.rdd")
            os.remove("longitude.rdd")
            os.remove("precip_unit.rdd")
            os.remove("temp_unit.rdd")
            os.remove("wind_unit.rdd")
            os.remove("location_name.rdd")
        cs()
        print("Preferences saved successfully!")
        input("Press ENTER to start Raindrop...")
