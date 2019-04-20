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
    dif_domain=[]
    count_2 = []
    for j in range(len(domain)):
        if (len(list(data[k]["goal"][domain[j]].values())) != 0):
            count_domain += 1
            need_domain.append(j)
    if count_domain==1:
        f = open(name_files[need_domain[0]], 'a')
    else:
        f = open(name_files[7], 'a')
    for i in range(len(data[k]["log"])):
        string = re.sub("\n", " ", data[k]["log"][i]["text"])
        list_.append(string)
        count = 0
        if count_domain!=1:
            if len(data[k]["log"][i]['metadata']) != 0:
                for d in need_domain:
                    if list(data[k]["log"][i]['metadata'][domain[d]]["semi"].values()).count('') == 0:
                        count+=1
                count_2.append(count)
                if count == 1:
                    for d in need_domain:
                        if list(data[k]["log"][i]['metadata'][domain[d]]["semi"].values()).count('') == 0:
                            dif_domain.append(domain[d])
                            list_.append(domain[d])
                            break
                elif count_2[len(count_2) - 2] == count and count>1:
                    if len(dif_domain)!=0 and list(data[k]["log"][i]['metadata'][dif_domain[len(dif_domain) - 1]]["semi"].values()).count('') == 0:
                        dif_domain.append(dif_domain[len(dif_domain) - 1])
                        list_.append(dif_domain[len(dif_domain) - 1])
                else:
                    for d in need_domain:
                        if list(data[k]["log"][i]['metadata'][domain[d]]["semi"].values()).count('') == 0:
                            if len(dif_domain)!=0 and dif_domain[len(dif_domain) - 1] != domain[d]:
                                dif_domain.append(domain[d])
                                list_.append(domain[d])
                                break

    for index in list_:
        f.write(index + '\n')
    f.write('***\n')
    f.close()
