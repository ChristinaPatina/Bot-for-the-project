import json
from sklearn.model_selection import train_test_split

with open("data.json") as read_file:
    data = json.load(read_file)

keys=list(data.keys())
keys_train, keys_test = train_test_split(keys, test_size=0.33, random_state=42)
domain=['taxi','police','hospital','hotel','attraction','train','restaurant']
name_files=['taxi.txt','police.txt','hospital.txt','hotel.txt','attraction.txt','train.txt','restaurant.txt','multidomen.txt']

for k in keys_train:
    list_ = []
    count_domain = 0
    need_domain = []
    for j in range(len(domain)):
        if (len(list(data[k]["goal"][domain[j]].values())) != 0):
            count_domain += 1
            need_domain.append(j)
    if count_domain==1:
        f = open(name_files[need_domain[0]], 'a')
    else:
        f = open(name_files[7], 'a')
    for i in range(len(data[k]["log"])):
        list_.append(data[k]["log"][i]["text"])
    for index in list_:
        f.write(index + '\n')
    f.write('***\n')
    f.close()
