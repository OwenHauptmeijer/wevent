from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/<string:location>/<int:budget>/<int:attendees>/<string:date>/<string:hour>')
def activities(location, budget, attendees, date, hour):
    import json
    import urllib.request, urllib.parse, urllib.error
    import ssl

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    hour = hour.split(':')
    hour_num = (int(hour[0]) * 100) + int(hour[1])
    if hour_num == 0:
        hour_num = 2400
    date = date.lower()

    # Empty recommendation list that is going to be filled with filtered activity names
    recommendations = dict()

    # Connection to firebase database with json, url depending on location
    url = "https://vuejs-e4bad-default-rtdb.europe-west1.firebasedatabase.app/" + location.lower() + ".json"
    url_open = urllib.request.urlopen(url, context=ctx)
    data = url_open.read().decode()
    js = json.loads(data)

    # Search in restaurant database for key information for recommendations
    for restaurant in js['restaurants']:
        info = js['restaurants'][restaurant]

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
                            recommendations[restaurant] = info
                        elif hour_num < except_from_num or hour_num >= except_till_num:
                            recommendations[restaurant] = info
                        else:
                            continue

    return recommendations
