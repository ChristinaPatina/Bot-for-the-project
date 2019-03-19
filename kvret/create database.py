import json

with open("kvret_train_public.json") as read_file:
    data = json.load(read_file)

f1 = open('db_navigate.txt', 'w')
f2 = open('db_schedule.txt', 'w')
f3 = open('db_weather.txt', 'w')
f1.write('POI' + ',' + 'Category' + ',' + 'Address' + ',' + 'Traffic Info' + ',' + 'Distance' + '\n')
f2.write('Event' + ',' + 'Time' + ',' + 'Date' + ',' + 'Party' + ',' + 'Agenda' + ',' + 'Location' + '\n')
f3.write('Location' + ',' + 'Today' + ',' + 'Monday' + ',' + 'Tuesday' + ',' + 'Wednesday' + ',' + 'Thursday' + ',' + 'Friday' + ',' + 'Saturday' + ',' + 'Sunday' + '\n')

for k in range(len(data)):
    nav_list = []
    sched_list = []
    weather_list = []

    if (data[k]["scenario"]["task"]["intent"] == "navigate"):
        for i in range(len(data[k]["scenario"]["kb"]["items"])):
            nav_list = []
            nav_list.append(data[k]["scenario"]["kb"]["items"][i]["poi"])
            nav_list.append(data[k]["scenario"]["kb"]["items"][i]["poi_type"])
            nav_list.append(data[k]["scenario"]["kb"]["items"][i]["address"])
            nav_list.append(data[k]["scenario"]["kb"]["items"][i]["traffic_info"])
            nav_list.append(data[k]["scenario"]["kb"]["items"][i]["distance"])
            for index in range(len(nav_list)):
                if index == len(nav_list)-1:
                    f1.write(nav_list[index] + '\n')
                else:
                    f1.write(nav_list[index] + ',')

    if (data[k]["scenario"]["task"]["intent"] == "schedule"):
        if not data[k]["scenario"]["kb"]["items"]:
            continue
        else:
            for j in range(len(data[k]["scenario"]["kb"]["items"])):
                sched_list = []
                sched_list.append(data[k]["scenario"]["kb"]["items"][j]["event"])
                sched_list.append(data[k]["scenario"]["kb"]["items"][j]["time"])
                sched_list.append(data[k]["scenario"]["kb"]["items"][j]["date"])
                sched_list.append(data[k]["scenario"]["kb"]["items"][j]["party"])
                sched_list.append(data[k]["scenario"]["kb"]["items"][j]["agenda"])
                sched_list.append(data[k]["scenario"]["kb"]["items"][j]["room"])
                for index in range(len(sched_list)):
                    if index == len(sched_list)-1:
                        f2.write(sched_list[index] + '\n')
                    else:
                        f2.write(sched_list[index] + ',')

    if (data[k]["scenario"]["task"]["intent"] == "weather"):
        for l in range(len(data[k]["scenario"]["kb"]["items"])):
            weather_list = []
            weather_list.append(data[k]["scenario"]["kb"]["items"][l]["location"])
            weather_list.append(data[k]["scenario"]["kb"]["items"][l]["today"])
            weather_list.append(data[k]["scenario"]["kb"]["items"][l]["monday"])
            weather_list.append(data[k]["scenario"]["kb"]["items"][l]["tuesday"])
            weather_list.append(data[k]["scenario"]["kb"]["items"][l]["wednesday"])
            weather_list.append(data[k]["scenario"]["kb"]["items"][l]["thursday"])
            weather_list.append(data[k]["scenario"]["kb"]["items"][l]["friday"])
            weather_list.append(data[k]["scenario"]["kb"]["items"][l]["saturday"])
            weather_list.append(data[k]["scenario"]["kb"]["items"][l]["sunday"])
            for index in range(len(weather_list)):
                if index == len(weather_list)-1:
                    f3.write(weather_list[index] + '\n')
                else:
                    f3.write(weather_list[index] + ';')

f1.close()
f2.close()
f3.close()
