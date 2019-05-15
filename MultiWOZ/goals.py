import json
from sklearn.model_selection import train_test_split
import re

with open("data.json") as read_file:
    data = json.load(read_file)

with open("dialogue_acts.json") as read_file:
    acts = json.load(read_file)

keys = list(data.keys())
keys_train, keys_test = train_test_split(keys, test_size=0.33, random_state=42)

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


goal(data, acts, keys_train)
