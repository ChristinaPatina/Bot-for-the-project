import json
with open("data.json") as read_file:
    data = json.load(read_file)

keys=list(data.keys())

f = open('multidomen_dialogues.txt', 'w')

for k in range(len(data)):
    list_ = []
    for i in range(len(data[keys[k]]["log"])):
        list_.append(data[keys[k]]["log"][i]["text"])
    for index in list_:
        f.write(index + '\n')
    f.write('***\n')
f.close()
