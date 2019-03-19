import json
with open("data.json") as read_file:
    data = json.load(read_file)

keys=list(data.keys())
domain=['taxi','police','hospital','hotel','attraction','train','restaurant']
name_files=['taxi.txt','police.txt','hospital.txt','hotel.txt','attraction.txt','train.txt','restaurant.txt','multidomen.txt']

for k in range(len(data)):
    list_ = []
    count_domain = 0
    need_domain = []
    for j in range(len(domain)):
        if (len(list(data[keys[k]]["goal"][domain[j]].values())) != 0):
            count_domain += 1
            need_domain.append(j)
    if count_domain==1:
        f = open(name_files[need_domain[0]], 'a')
    else:
        f = open(name_files[7], 'a')
    for i in range(len(data[keys[k]]["log"])):
        list_.append(data[keys[k]]["log"][i]["text"])
    for index in list_:
        f.write(index + '\n')
    f.write('***\n')
    f.close()
