import json
import re
with open("kvret_train_public.json") as read_file:
    data = json.load(read_file)

def replacement(domen,k,i,str):
    n=['distance','traffic_info','poi_type','address','poi']
    s=['room','agenda','time','date','party','event']
    w=['weather_attribute','date','location']
    w_a=["monday","tuesday","friday","wednesday","thursday","sunday","saturday"]
    w_d=["Monday","Tuesday","Friday","Wednesday","Thursday","Sunday","Saturday"]
    temperature=['20F', '30F', '40F', '50F', '60F', '70F', '80F', '90F', '100F']
    if (domen=='navigate'):
        l=n
    elif (domen=='schedule'):
        l=s
    else:
        l=w

    kb = []
    for l_i in l:
        slot = ''
        slots = []
        fl = 0
        if data[k]["dialogue"][i]["data"].get("requested")==None:
            return str
        else:
            if data[k]["dialogue"][i]["data"]["requested"].get(l_i)==True:
                if l_i==n[2]:
                    l_i=n[4]
                if l_i==w[1] and domen=='weather':
                    fl=1
                if l_i==w[0]:
                    fl=2

                if data[k]["scenario"]["kb"].get("items")==None:
                    return str
                else:
                    if fl==0:
                        for j in range(len(data[k]["scenario"]["kb"]["items"])):
                            if (l_i==w[2]):
                                kb.append(data[k]["scenario"]["kb"]["items"][j].get(l_i).title())
                            else:
                                kb.append(data[k]["scenario"]["kb"]["items"][j].get(l_i))

                    if (data[k]["dialogue"][i]["data"]["slots"].get(l_i) != None):
                        slot = data[k]["dialogue"][i]["data"]["slots"].get(l_i)

                    if fl==2:
                        for attr in w_a:
                            for j in range(len(data[k]["scenario"]["kb"]["items"])):
                                kb.append(data[k]["scenario"]["kb"]["items"][j].get(attr).split(','))
                                if slot!='':
                                    if slot==data[k]["scenario"]["kb"]["items"][j].get(attr).split(',')[0]:
                                        slots.append(attr.capitalize())
                    if fl==0 or (fl==2 and slot==''):
                        for kb_i in kb:
                            if kb_i==slot:
                                str = re.sub(slot, slot, str)
                            else:
                                if fl==0:
                                    z = '_' + l_i + '_'
                                    if l_i==s[2]:
                                        index=kb_i.find('pm')
                                        if index!=-1:
                                            kb_i=kb_i[:index] + ' ' + kb_i[index:]
                                        index2=kb_i.find('am')
                                        if index2!=-1:
                                            kb_i=kb_i[:index2] + ' ' + kb_i[index2:]
                                    str=re.sub(kb_i,z,str)
                                else:
                                    for w_in in w_d:
                                        z = '_' + w[1] + '_'
                                        str = re.sub(w_in, z, str)
                                    z='_' + l_i + '_'
                                    for t in temperature:
                                        str=re.sub(t, z, str)

                    if fl==2 and slot!='':
                        for s in slots:
                            z = '_' + w[1] + '_'
                            str = re.sub(s, z, str)
                        z = '_' + l_i + '_'
                        for t in temperature:
                            str = re.sub(t, z, str)
                    if fl==1:
                        str = re.sub(slot, slot, str)

                kb.clear()

    return str


def insert_relation(domen,name_file):
    f = open(name_file, 'w')
    for k in range(len(data)):
        list = []
        if (data[k]["scenario"]["task"]["intent"]==domen):
            for i in range(len(data[k]["dialogue"])):
                if len(data[k]["dialogue"])==2 and domen=='schedule':
                    list.append(data[k]["dialogue"][i]["data"]["utterance"])
                else:
                    if i>0 and data[k]["dialogue"][i]["data"].get('end_dialogue') == False:
                        string = replacement(domen,k,i,data[k]["dialogue"][i]["data"]["utterance"])
                        list.append(string)
                    else:
                        list.append(data[k]["dialogue"][i]["data"]["utterance"])
            for index in list:
                f.write(index + '\n')
            f.write('***\n')
    f.close()



insert_relation('navigate','navigate_insert_relation.txt')
insert_relation('schedule','schedule_insert_relation.txt')
insert_relation('weather','weather_insert_relation.txt')
