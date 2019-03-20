import json
from sklearn.model_selection import train_test_split

with open("data.json") as read_file:
    data = json.load(read_file)

keys=list(data.keys()) #10438
keys_train, keys_test = train_test_split(keys, test_size=0.33, random_state=42)
print(len(keys_train)) #6993
print(len(keys_test)) #3445

#-----------------all------------------
f = open('all_dialogues.txt', 'w')

for k in range(len(data)):
    list_ = []
    for i in range(len(data[keys[k]]["log"])):
        list_.append(data[keys[k]]["log"][i]["text"])
    for index in list_:
        f.write(index + '\n')
    f.write('***\n')
f.close()
#----------------train------------------

f = open('train_dialogues.txt', 'w')

for k in keys_train:
    list_ = []
    for i in range(len(data[k]["log"])):
        list_.append(data[k]["log"][i]["text"])
    for index in list_:
        f.write(index + '\n')
    f.write('***\n')
f.close()
