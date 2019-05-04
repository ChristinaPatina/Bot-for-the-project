from copy import deepcopy
import json
from sklearn.model_selection import train_test_split
import re
import Levenshtein

with open("data.json") as read_file:
    data = json.load(read_file)

with open("dialogue_acts.json") as read_file:
    acts = json.load(read_file)

keys = list(data.keys())
keys_train, keys_test = train_test_split(keys, test_size=0.33, random_state=42)

domain = ['taxi','police','hospital','hotel','attraction','train','restaurant']
name_files = ['taxi.txt','police.txt','hospital.txt','hotel.txt','attraction.txt','train.txt','restaurant.txt','multidomen.txt']
norm_files = ['norm_taxi.txt','norm_police.txt','norm_hospital.txt','norm_hotel.txt','norm_attraction.txt','norm_train.txt','norm_restaurant.txt','norm_multidomen.txt']


def check(str1: str, word: str):

    if str1 == "I've heard about a hotel called Kirkwood House, but the only thing I know about it is the name. Can you tell me more?":
        print("===")

    str1 = re.sub("--", " -- ", str1)
    str1 = re.sub(",", ", ", str1)
    str1 = re.sub("London -- King's", "London--King's", str1)
    str1 = re.sub("TR 8991", "TR 8991 ", str1)
    word = re.sub("red Audi a", "red Audi", word)
    for w in word.split():
        if w == "St" or w == "St.":
            str1 = re.sub("Street", "St", str1)
            str1 = re.sub("Street\\.", "St.", str1)
        if w == "Co.":
            str1 = re.sub("Company", "Co.", str1)
        elif w == "Company":
            str1 = re.sub("Co\\.", "Company", str1)
    str1_list = str1.split()
    word_right = ""
    if word[0] == " ":
        word = word[1:]
    if word[len(word)-1] == " ":
        word = word[:-1]
    word_list = word.split(" ")
    flag = True
    count = 0

    if len(word_list) == 1:
        for i in str1_list:
            lev = Levenshtein.ratio(word, i)
            if lev >= 0.7:
                word_right = i
                break
    else: # more tan 1 word
        for i in str1_list:
            if count == len(word_list):
                break
            for j in word_list:
                lev = Levenshtein.ratio(j, i)
                if lev >= 0.65:
                    word_right += i
                    word_right += " "
                    count += 1
                    break
                elif count >= 1:
                    continue
                else:
                    break

    if len(word_right) != 0:
        if word_right[len(word_right)-1] == " ":
            word_right = word_right[:-1]
        if word_right[len(word_right)-1] == "?" or word_right[len(word_right)-1] == "." \
                or word_right[len(word_right)-1] == "," or word_right[len(word_right)-1] == ":"\
                or word_right[len(word_right)-1] == "!" or word_right[len(word_right)-1] == ")":
            word_right = word_right[:-1]
    word_right_list = word_right.split(" ")
    if len(word_list) != len(word_right_list):
        flag = False
    #print(str1, '\n', word, '|', word_right)#####
    assert flag
    return word_right


def tagging(string: str, my_dict: dict):
    f = open('tags.txt', 'a')

    str_list = string.split()
    str_list_copy = deepcopy(str_list)
    tags = []
    right = True
    keys = list(my_dict.keys())
    keys_copy = deepcopy(keys)

    if string == "The Jesus Green Outdoor Pool is between Victoria Road and the river. The Kings Hedges Learner pool is on Jedburgh Court, Kings Hedges. Would you like their phone numbers?":
        print("===")

    for i in str_list_copy:

        if len(keys_copy) == 0:
           tags.append("O")
           continue

        for key in keys_copy:
            key_words = key.split()
            len_key_words = len(key_words)
            slot = my_dict[key][1:-1]
            if len_key_words == 1:
                if key_words[0] != i:
                    tags.append("O")
                    break
                if key_words[0] == i:
                    tags.append("B-" + slot)
                    keys_copy.remove(key)
                    break
            else: # переписать что в else
                len_words = len_key_words
                for j in key_words:
                    if i != j:
                        #tags.append("O")#####
                        break
                    if i == j and len_words == len_key_words:
                        tags.append("B-" + slot)
                        len_words -= 1
                        continue # нужен break, но тогда переписать
                    if i == j and len_words < len_key_words:
                        tags.append("I-" + slot)
                        len_words -= 1
                        break # нужен break, но тогда переписать
                    if len_words == 0:
                        keys_copy.remove(key)

    print(len(str_list), len(tags), '\n', tags)
    if len(str_list) != len(tags):
        right = False
    #assert right

    f.write(string + '\n')
    for tag in tags:
        f.write(tag + ' ')
    f.write('\n')
    # для проверки, потом удалить
    if right == True:
        f.write('True' + '\n')
    else:
        f.write('False' + '\n')
    #
    f.close()


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
    slots2 = []
    sl = ""

    str_buf = [str]
    my_dict = dict()

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
            #return str
            i = i+1
        #else:
        if data[k]["log"][i]['metadata'][d]["semi"].get(s) != None:
            kb.append(data[k]["log"][i]['metadata'][d]["semi"].get(s))
        if data[k]["log"][i]['metadata'][d]["book"].get(s) != None:
            if data[k]["log"][i]['metadata'][d]["book"].get(s) != "":
                kb.append(data[k]["log"][i]['metadata'][d]["book"].get(s))
            if len(data[k]["log"][i]['metadata'][d]["book"]["booked"]) != 0:
                #print(k,i,d)
                for s2 in slots:
                    if data[k]["log"][i]['metadata'][d]["book"]["booked"][0].get(s2) != None:
                        kb2.append(data[k]["log"][i]['metadata'][d]["book"]["booked"][0].get(s2))
                        sl = s2

        for kb_i in kb:
            if kb_i != '':
                z = ' _' + s + '_ '
                str = re.sub(" " + kb_i, z, str)
                str_buf.append(str)
                if str_buf[len(str_buf)-2] != str:
                    print(k,i)#####
                    kb_i_ = check(str_buf[len(str_buf)-2], kb_i)
                    str = re.sub(kb_i_, z, str_buf[len(str_buf)-2])
                    str_buf[len(str_buf)-1] = str
                    my_dict[kb_i_] = z[1:-1]

        if len(kb2) != 0:
            for kb2_i in kb2:
                z = ' _' + sl + '_ '
                str = re.sub(" " + kb2_i, z, str)
                str_buf.append(str)
                if str_buf[len(str_buf) - 2] != str:
                    kb2_i_ = check(str_buf[len(str_buf)-2], kb2_i)
                    str = re.sub(kb2_i_, z, str_buf[len(str_buf)-2])
                    str_buf[len(str_buf) - 1] = str
                    my_dict[kb2_i_] = z[1:-1]

        kb.clear()
        kb2.clear()

    slots.clear()

    key = k[0:-5] # the name of the element in the file without .json
    keys = list(acts[key].keys())
    for keys_i in keys:
        if acts[key][keys_i] != "No Annotation":
            keys_in_keys = list(acts[key][keys_i].keys())
            for kk_i in keys_in_keys:
                for ii in range(len(acts[key][keys_i][kk_i])):
                    if acts[key][keys_i][kk_i][ii][0] != "none":
                        if acts[key][keys_i][kk_i][ii][1] != "?":
                            slots2.append(acts[key][keys_i][kk_i][ii][0])
                            kb.append(acts[key][keys_i][kk_i][ii][1])
                            for s2 in slots2:
                                for kb_i in kb:
                                    if kb_i == '+44 1223 568988':
                                        continue
                                    z = ' _' + s2 + '_ '
                                    str = re.sub(" " + kb_i, z, str_buf[len(str_buf) - 1])
                                    str_buf.append(str)
                                    if str_buf[len(str_buf) - 2] != str:
                                        kb_i_ = check(str_buf[len(str_buf)-2], kb_i)
                                        str = re.sub(kb_i_, z, str_buf[len(str_buf)-2])
                                        str_buf[len(str_buf) - 1] = str
                                        my_dict[kb_i_] = z[1:-1]
                        slots2.clear()
                        kb.clear()

            keys_in_keys.clear()
    if d == 'police':
        with open("police_db.json") as read_file:
            pol_db = json.load(read_file)
        slot_keys = list(pol_db[0].keys())
        for k in slot_keys:
            z = ' _' + k + '_ '
            if k == 'id':
                continue
            else:
                str = re.sub(pol_db[0].get(k), z, str)

    if d == 'hospital':
        with open("hospital_db.json") as read_file:
            hosp_db = json.load(read_file)
        slots_k_hosp = ['department','phone']
        for id in slots_k_hosp:
            for i in range(len(hosp_db)):
                kb.append(hosp_db[i].get(id))
            for kb_i in kb:
                z = ' _' + id + '_ '
                str = re.sub(kb_i, z, str)
            kb.clear()

    print(str_buf[len(str_buf)-1], '\n', k, i) #####
    #tagging(str_buf[0], my_dict)

    return str_buf[len(str_buf)-1]
    
    def normalization(one_domain, name_file):

    f = open(name_file, 'w')
    for k in keys_train:
        list_ = []
        count_domain = 0  # how many domains does the dialogue include
        need_domain = []  # indexes of domains
        domen = []  # domain names
        for j in range(len(domain)):
            if len(list(data[k]["goal"][domain[j]].values())) != 0:
                count_domain += 1
                need_domain.append(j)
        if count_domain == 1 and one_domain == domain[need_domain[0]]:
            domen.append(one_domain)
        elif count_domain > 1 and one_domain == 'multi':
            for n_d in need_domain:
                domen.append(domain[n_d])
        if one_domain != 'multi' and k.find("MUL") == -1:
            if len(list(data[k]["goal"][one_domain].values())) != 0:
                for i in range(len(data[k]["log"])):
                    if i < len(data[k]["log"]) - 2:
                        string = replacement(one_domain, k, i, data[k]["log"][i]["text"])
                        list_.append(string)
                    else:
                        list_.append(data[k]["log"][i]["text"])
                        tagging(data[k]["log"][i]["text"], dict())
                for index in list_:
                    f.write(index + '\n')
                f.write('***\n')

        elif one_domain == 'multi': #else
            if k.find("MUL") != -1:
                count = 0
                for d in domen:
                    if len(list(data[k]["goal"][d].values())) != 0:
                        for i in range(len(data[k]["log"])):
                            if count == 0:
                                if i < len(data[k]["log"])-2:
                                    string = replacement(d, k, i, data[k]["log"][i]["text"])
                                    list_.append(string)
                                else:
                                    list_.append(data[k]["log"][i]["text"])
                            else:
                                if i < len(data[k]["log"])-2:
                                    string = replacement(d, k, i, list_[i])
                                    list_[i] = string
                    count += 1
                for index in list_:
                    f.write(index + '\n')
                f.write('***\n')
            else:
                continue
    f.close()
    
    
    
#normalization('taxi', norm_files[0])
#normalization('police', norm_files[1])
#normalization('hospital', norm_files[2])
#normalization('hotel', norm_files[3])
normalization('attraction', norm_files[4])
#normalization('train', norm_files[5])
#normalization('restaurant', norm_files[6])
#normalization('multi', norm_files[7])
