import json
from sklearn.model_selection import train_test_split
import re

with open("data.json") as read_file:
    data = json.load(read_file)

with open("dialogue_acts.json") as read_file:
    acts = json.load(read_file)

keys = list(data.keys())
keys_train, keys_test = train_test_split(keys, test_size=0.33, random_state=42)

domain = ['taxi','police','hospital','hotel','attraction','train','restaurant']
name_files = ['taxi.txt','police.txt','hospital.txt','hotel.txt','attraction.txt','train.txt','restaurant.txt','multidomen.txt']
norm_files = ['norm_taxi.txt','norm_police.txt','norm_hospital.txt','norm_hotel.txt','norm_attraction.txt','norm_train.txt','norm_restaurant.txt','norm_multidomen.txt']


def replacement(d, k, i, str):

    kb = []
    kb2 = []
    slots_r = ['address','postcode','phone','name','area','pricerange','type','people','day','time','reference','food']
    slots_hotel = ['address','postcode','phone','name','area','pricerange','type','internet','parking','stars','people','day','stay','reference']
    slots_attr = ['address','postcode','phone','name','area','pricerange','type','people','day']
    slots_train = ['address','postcode','phone','departure', 'destination', 'leaveAt', 'arriveBy','people', 'trainID','day','reference']
    slots_taxi = ['address','postcode','phone','name','departure', 'destination', 'leaveAt', 'arriveBy']
    slots_p = ['address','postcode','phone','department']
    slots_hosp = ['address','postcode','phone']
    slots = []
    slots2=[]
    sl=""

    if d == 'restaurant':
        slots = slots_r
    if d == 'police':
        slots = slots_p
    if d == 'hotel':
        slots = slots_hotel
    if d == 'hospital':
        slots = slots_hosp
    if d == 'taxi':
        slots = slots_taxi
    if d == 'train':
        slots = slots_train
    if d == 'attraction':
        slots = slots_attr
    for s in slots:
        if len(data[k]["log"][i]['metadata']) == 0:
            return str
        else:
            if data[k]["log"][i]['metadata'][d]["semi"].get (s) != None:
                kb.append(data[k]["log"][i]['metadata'][d]["semi"].get(s))
            if data[k]["log"][i]['metadata'][d]["book"].get (s) != None:
                kb.append(data[k]["log"][i]['metadata'][d]["book"].get(s))
                if len(data[k]["log"][i]['metadata'][d]["book"]["booked"]) != 0:
                    for s2 in slots:
                        if data[k]["log"][i]['metadata'][d]["book"]["booked"].get(s2) != None:
                            kb2.append(data[k]["log"][i]['metadata'][d]["book"]["booked"].get(s2))
                            sl = s2
            for kb_i in kb:
                z = '_' + s + '_'
                str = re.sub(kb_i, z, str)

            if len(kb2) != 0:
                for kb2_i in kb2:
                    z = '_' + sl + '_'
                    str = re.sub(kb2_i, z, str)

            kb.clear()
            kb2.clear()

    slots.clear()

    key = k[0:-5]
    keys = list(acts[key].keys())

    for keys_i in keys:
        keys_in_keys = list(acts[key][keys_i].keys())
        for kk_i in keys_in_keys:
            print(len(kk_i))
            for ii in range(len(acts[key][keys_i][kk_i])):
                if acts[key][keys_i][kk_i][ii][0] != "none":
                    if acts[key][keys_i][kk_i][ii][1] != "?":
                        slots2.append(acts[key][keys_i][kk_i][ii][0])
                        if slots2.count(acts[key][keys_i][kk_i][ii][0]) == 2:
                            slots2.remove(acts[key][keys_i][kk_i][ii][0])
        keys_in_keys.clear()

    for s2 in slots2:
        for keys_in in keys:
            keys_in_keys_ = list(acts[key][keys_in].keys())
            for kk_in in keys_in_keys_:
                for ind in range(len(acts[key][keys_in][kk_in])):
                    if acts[key][keys_in][kk_in][ind][0] == s2:
                        kb.append(acts[key][keys_in][kk_in][ind][1])
            keys_in_keys_.clear()

        for kb_i in kb:
            z = '_' + s2 + '_'
            str = re.sub(kb_i, z, str)

    return str


def normalization(one_domain, name_file):

    f = open(name_file, 'w')
    for k in keys_train:
        list_ = []
        count_domain = 0
        need_domain = []
        domen = []
        for j in range(len(domain)):
            if len(list(data[k]["goal"][domain[j]].values())) != 0:
                count_domain += 1
                need_domain.append(j)
        if count_domain == 1 and one_domain == domain[need_domain[0]]:
            domen.append(one_domain)
        elif count_domain > 1 and one_domain == '':
            for n_d in need_domain:
                domen.append(domain[n_d])
        for d in domen:
            if len(list(data[k]["goal"][one_domain].values())) != 0:
                for i in range(len(data[k]["log"])):
                    if i < len(data[k]["log"])-2:
                        string = replacement(d, k, i, data[k]["log"][i]["text"])
                        list_.append(string)
                    else:
                        list_.append(data[k]["log"][i]["text"])
                for index in list_:
                    f.write(index + '\n')
                f.write('***\n')
    f.close()


normalization('restaurant', norm_files[6])