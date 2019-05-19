import json
from sklearn.model_selection import train_test_split
import re

with open("data.json") as read_file:
    data = json.load(read_file)

with open("dialogue_acts.json") as read_file:
    acts = json.load(read_file)

keys = list(data.keys())
keys_train, keys_test = train_test_split(keys, test_size=0.33, random_state=42)
"""
'1st realisation (all)'
def goal(data, acts, keys):
    f = open('goals.txt', 'w')
    for k in keys:
        if k == 'PMUL3872.json' or k == 'PMUL4707.json' or k == 'PMUL4776.json':
            continue
        count = 0 # number of move in the dialogue
        key = k[0:-5]  # the name of the element in the file without .json
        for i in range(len(data[k]["log"])):
            goal = []
            if i % 2 == 0:
                string = re.sub("\n", " ", data[k]["log"][i]["text"])
                if string[len(string) - 1] == " ":
                    string = string[:-1]
                f.write(string + '\n')
                count += 1
                if acts[key][str(count)] != "No Annotation":
                    name_goal = list(acts[key][str(count)].keys())
                    for n in name_goal:
                        if n[len(n)-7::] == "Request":
                            right_goal = ""
                            for k_k in range(len(acts[key][str(count)][n])):
                                if acts[key][str(count)][n][k_k][1] == "?":
                                    slot = acts[key][str(count)][n][k_k][0]
                                    if slot == 'Post':
                                        slot = 'postcode'
                                    if slot == 'Ref':
                                        slot = 'reference'
                                    if slot == 'Dest':
                                        slot = 'destination'
                                    if slot == 'Price':
                                        slot = 'pricerange'
                                    if slot == 'Addr':
                                        slot = 'address'
                                    if slot == 'Depart':
                                        slot = 'departure'
                                    if slot == 'Id':
                                        slot = 'trainID'
                                    if slot == 'Arrive':
                                        slot = 'arriveBy'
                                    if slot == 'Leave':
                                        slot = 'leaveAt'
                                    right_goal += "-" + slot.lower()
                            n = n + right_goal
                        goal.append(n)
                else:
                    goal.append('NoAnnotation')

                for g in goal:
                    f.write(g + ' ')
                f.write('\n')
    f.close()
"""
def goal(data, acts, keys):
    f = open('goals.txt', 'w')
    for k in keys:
        if k == 'PMUL3872.json' or k == 'PMUL4707.json' or k == 'PMUL4776.json':
            continue
        count = 0 # number of move in dialogue
        key = k[0:-5]  # the name of the element in the file without .json
        for i in range(len(data[k]["log"])):
            goal = []
            if i % 2 == 0:
                string = re.sub("\n", " ", data[k]["log"][i]["text"])
                if string[len(string) - 1] == " ":
                    string = string[:-1]
                count += 1
                if acts[key][str(count)] != "No Annotation":
                    name_goal = list(acts[key][str(count)].keys())
                    for c_i in range(len(name_goal)):
                        if name_goal[c_i][len(name_goal[c_i])-11::] == "OfferBooked":
                            name_goal[c_i] = name_goal[c_i][:-2]
                    copy_name = deepcopy(name_goal)
                    for item in copy_name:
                        if item[len(item)-7::] == "reqmore":
                            name_goal.remove(item)
                        if item[len(item)-7::] == "NoOffer":
                            name_goal.remove(item)
                        if item[len(item) - 6::] == "NoBook":
                            name_goal.remove(item)

                    counter_domain = 1
                    if len(name_goal) > 1:
                        for n_ii in range(len(name_goal)-1):
                            index_i = name_goal[n_ii].find("-")
                            for n_jj in range(n_ii+1, len(name_goal)):
                                index_j = name_goal[n_jj].find("-")
                                if name_goal[n_ii][0:index_i] != name_goal[n_jj][0:index_j]:
                                    counter_domain += 1

                    copy_name_ = deepcopy(name_goal)
                    if len(name_goal) > 1 and counter_domain > 1:
                        for item_ in copy_name_:
                            if item_[0:7] == "Booking":
                                name_goal.remove(item_)
                    # Если несколько доменов в строке, то её удаляем
                    fl = 0
                    if len(name_goal) != 0:
                        for n_i in range(len(name_goal)-1):
                            if fl == 1:
                                break
                            ind_i = name_goal[n_i].find("-")
                            for n_j in range(n_i+1, len(name_goal)):
                                ind_j = name_goal[n_j].find("-")
                                if name_goal[n_i][0:ind_i] != name_goal[n_j][0:ind_j]:
                                    name_goal.clear()
                                    fl = 1
                                    break

                    count_request = -1
                    for n_ind, n in enumerate(name_goal):
                        if n[len(n) - 7::] == "Request":
                            count_request = n_ind

                    if count_request != -1:
                        right_goal = ""
                        for k_k in range(len(acts[key][str(count)][name_goal[count_request]])):
                            if acts[key][str(count)][name_goal[count_request]][k_k][1] == "?":
                                slot = acts[key][str(count)][name_goal[count_request]][k_k][0]
                                if slot == 'Post':
                                    slot = 'postcode'
                                if slot == 'Ref':
                                    slot = 'reference'
                                if slot == 'Dest':
                                    slot = 'destination'
                                if slot == 'Price':
                                    slot = 'pricerange'
                                if slot == 'Addr':
                                    slot = 'address'
                                if slot == 'Depart':
                                    slot = 'departure'
                                if slot == 'Id':
                                    slot = 'trainID'
                                if slot == 'Arrive':
                                    slot = 'arriveBy'
                                if slot == 'Leave':
                                    slot = 'leaveAt'
                                right_goal += "-" + slot.lower()
                        n = name_goal[count_request] + right_goal
                        n = n[(n.find("-")+1)::] # удаляем домен из цели
                        # если есть цель Request оставляем только её
                        goal.clear()
                        goal.append(n)
                    else:
                        if len(name_goal) == 1:
                            z = name_goal[0][(name_goal[0].find("-")+1)::]
                            goal.append(z)
                        elif len(name_goal) > 1:
                            # оставляю вторую цель в списке
                            z = name_goal[1][(name_goal[1].find("-") + 1)::]
                            goal.append(z)
                if len(goal) != 0:
                    f.write(string + '\n')
                    for g in goal:
                        f.write(g + ' ')
                    f.write('\n')
    f.close()


goal(data, acts, keys_train)
