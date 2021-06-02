import json
import urllib.request, urllib.parse, urllib.error
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# prompt the user for data to personalize recommendations (for now, later data from vue.js will be used)
location = input("Which city?")
budget = int(input("Price class (1-5)?"))
attendees = int(input("How many attendees?"))
date = input("Which day?")
hour = input("What time?").split(':')
hour_num = (int(hour[0]) * 100) + int(hour[1])
if hour_num == 0:
    hour_num = 2400

# Empty recommendation list that is going to be filled with filtered activity names
recommendations = list()

# Connection to firebase database with json, url depending on location
url = "https://vuejs-e4bad-default-rtdb.europe-west1.firebasedatabase.app/" + location.lower() + ".json"
url_open = urllib.request.urlopen(url, context=ctx)
data = url_open.read().decode()
js = json.loads(data)

# Enable to visualize tree structure of database:
# x = json.dumps(js, indent=4)
# print(x)
# quit()

# Search in restaurant database for key information for recommendations
for restaurant in js['restaurants']:
    info = js['restaurants'][restaurant]

    name = info['id']
    max_people = info['attendees']['max']
    min_people = info['attendees']['min']
    price_class = info['budget']
    available_day = info['dates'][date]

    if price_class <= budget:
        if min_people <= attendees <= max_people:
            if available_day:
                from_time = available_day['from'].split(':')
                from_time_num = (int(from_time[0]) * 100) + int(from_time[1])
                till_time = available_day['till'].split(':')
                till_time_num = (int(till_time[0]) * 100) + int(till_time[1])
                if till_time_num == 0:
                    till_time_num = 2400
                except_time = available_day['except']
                if except_time:
                    except_from = except_time['from'].split(':')
                    except_from_num = (int(except_from[0]) * 100) + int(except_from[1])
                    except_till = except_time['till'].split(':')
                    except_till_num = (int(except_till[0]) * 100) + int(except_till[1])
                else:
                    except_from_num = None
                    except_till_num = None
                if from_time_num <= hour_num < till_time_num:
                    if except_from_num == None and except_till_num == None:
                        recommendations.append(name)
                    elif hour_num < except_from_num or hour_num >= except_till_num:
                        recommendations.append(name)
                    else:
                        continue

print(recommendations)













