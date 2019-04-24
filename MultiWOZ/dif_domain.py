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
    counter = 0
    for i in range(len(data[k]["log"])):
        string = re.sub("\n", " ", data[k]["log"][i]["text"])
        list_.append(string)
        count = 0
        if count_domain!=1:
            if len(data[k]["log"][i]['metadata']) != 0:
                for d in domain:
                    if len(list(data[k]["log"][i]['metadata'][d]["semi"].values()))!=0 and list(data[k]["log"][i]['metadata'][d]["semi"].values()).count('') == 0:
                        count+=1
                count_2.append(count)
                if counter == 0 and count > 1:
                    f2 = open('many_domains_in_one_phrase.txt', 'a')
                    f2.write(k + '\n')
                    f2.close()
                    list_.clear()
                    break
                if count == 1:
                    for d in need_domain:
                        if list(data[k]["log"][i]['metadata'][domain[d]]["semi"].values()).count('') == 0:
                            dif_domain.append(domain[d])
                            list_.append(domain[d])
                            counter+=1
                            break
                elif count_2[len(count_2) - 2] == count and count>1:
                    if len(dif_domain)!=0 and list(data[k]["log"][i]['metadata'][dif_domain[len(dif_domain) - 1]]["semi"].values()).count('') == 0:
                        dif_domain.append(dif_domain[len(dif_domain) - 1])
                        list_.append(dif_domain[len(dif_domain) - 1])
                        counter+=1
                else:
                    for d in domain:
                        if len(list(data[k]["log"][i]['metadata'][d]["semi"].values()))!=0 and list(data[k]["log"][i]['metadata'][d]["semi"].values()).count('') == 0:
                            if len(dif_domain)!=0 and dif_domain[len(dif_domain) - 1] != d:
                                dif_domain.append(d)
                                list_.append(d)
                                counter+=1
                                break
    if len(list_)!=0:
        for index in list_:
            f.write(index + '\n')
        f.write('***\n')
    f.close()
