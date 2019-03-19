import json

with open("kvret_train_public.json") as read_file:
    data = json.load(read_file)

f1 = open('navigate.txt', 'w')
f2 = open('schedule.txt', 'w')
f3 = open('weather.txt', 'w')

for k in range(len(data)):
    nav_list = []
    sched_list = []
    weather_list = []
    
    if (data[k]["scenario"]["task"]["intent"]=="navigate"):
        for i in range(len(data[k]["dialogue"])):
            nav_list.append(data[k]["dialogue"][i]["data"]["utterance"]) 
        for index in nav_list:
            f1.write(index + '\n')
        f1.write('***\n')
        
    if (data[k]["scenario"]["task"]["intent"]=="schedule"):
        for i in range(len(data[k]["dialogue"])):
            sched_list.append(data[k]["dialogue"][i]["data"]["utterance"])
        for index in sched_list:
            f2.write(index + '\n')
        f2.write('***\n')
        
    if (data[k]["scenario"]["task"]["intent"]=="weather"):
        for i in range(len(data[k]["dialogue"])):
            weather_list.append(data[k]["dialogue"][i]["data"]["utterance"])
        for index in weather_list:
            f3.write(index + '\n')
        f3.write('***\n')  
        
f1.close()
f2.close()
f3.close()
