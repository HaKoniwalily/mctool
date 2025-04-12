import json
from collections import OrderedDict
json_file ="./nbs/名称.json"
name = "名称"
username ='hakoniwalily'

def process_keys(key,layer_inst):
    new_key = ''
    fix_inst = ''

    if layer_inst == 0:
    # 竖琴
        if key>=33 and key<=57:
            #使用钢琴
            new_key =key-33
            fix_inst = "f"
            
        elif key<33 and key>=21:
            #低一度用吉他
            new_key = key+12-33
            fix_inst = "7"
        elif key<21 and key>=10:
            #低2度用BASS
            new_key = key+24-33
            fix_inst = "0"
        elif key>57 and key<=81:
            #高1-2度用bell
            new_key = key-24-33
            fix_inst = "4"
        else:
            new_key=''
            fix_inst ='#'
    #别的乐器后面再说
    elif layer_inst == 5:
        #吉他,key判定Pass
        new_key =key-33
        fix_inst = "7"
    elif layer_inst == 7:
    #铃铛,key判定Pass
        new_key =key-33
        fix_inst = "4"   
    elif layer_inst == 1:
    #bass,key判定Pass
        new_key =key-33
        fix_inst = "0"               
    elif layer_inst == 6:
    #长笛,key判定Pass
        new_key =key-33
        fix_inst = "5"
    elif layer_inst == 3:
        new_key =key-33
        fix_inst = "x"  
    elif layer_inst == 2:
        new_key =key-33
        fix_inst = "j"   
    elif layer_inst == 4:  
        new_key =key-33
        fix_inst = "2"  
    elif layer_inst == 11:  
        new_key =key-33
        fix_inst = "a"  
    elif layer_inst == 13:  
        new_key =key-33
        fix_inst = "c"          
                                  
    return new_key,fix_inst


with open(json_file) as f:
    data = json.load(f)
notes =data["notes"]
jiange = 2
#器材表，转换成插件器材
inst ={
    0:'f', #竖琴
    5:'7', #吉他
    7:'4', #铃铛
    1:'0', #bass
    6:'5', #长笛
    3:'x', #snare drum
    2:'j', #bass drum
    4:"2", #click
    11:'a', #cow bell
    13:'c' #bit
    
}
#音符转化表
notes_key ={
    '0':"0",
    '1':"1",
    '2':"2",
    '3':"3",
    '4':"4",
    '5':"5",
    '6':"6",
    '7':"7",
    '8':"8",
    '9':"9",
    '10':"a",
    '11':"b",
    '12':"c",
    '13':"d",
    '14':"e",
    '15':"f",
    '16':"g",
    '17':"h",
    '18' :"i",
    '19' :"j",
    '20' :"k",
    '21' :"l",
    '22' :"m",
    '23' :"n",
    '24' :"o",

}
print(notes[16])
layer_lists = {}
layer_last_tick ={}
result={}

for note in notes:
    layer_value = note['layer']
    if layer_value not in layer_lists:
        layer_lists[layer_value] = {}
        layer_last_tick[layer_value] = 0
        result[layer_value] =""

for note in notes:
    layer_value = note['layer']
    key =note['key']
    #key要-33
    layer_inst =note['inst']
    
    
    #根据不同乐器来执行不同的算法
    new_key,fix_inst =process_keys(key,layer_inst)  
        
    tick =note['tick']
    
    layer_lists[layer_value][tick] = [fix_inst,str(new_key)]
    if tick !=0:
        if layer_last_tick[layer_value]+1 !=tick:
            for i in range(layer_last_tick[layer_value]+1, tick):
                layer_lists[layer_value][i] = ["#",'']
          
    layer_last_tick[layer_value] = tick
    
#生成指令
for layer in layer_lists:
    sorted_dict = OrderedDict(sorted(layer_lists[layer].items()))
    # print(sorted_dict)
    for key,value in sorted_dict.items():
        if value[1]!= '':
            #这里器材判断以后写，暂时竖琴
            # print(value)
            # add_key = notes_key[int(value)]
            add_key = notes_key[value[1]]
            
            # print(add_key)
            
            # result[layer] =str(result[layer]+"f"+add_key)
            result[layer] =str(result[layer]+value[0]+add_key)
            
            # print(value)
            pass
        else:
            result[layer] =str(result[layer]+'#')
play_command =f'/music {jiange} '
def split_and_print(text, chunk_size):
    for i in range(0, len(text), chunk_size):
        global play_command
        
        if i==0:
            print(f"/music compose create {name}{total_layer} {jiange} " +text[i:i + chunk_size])
            play_command=play_command+'@'+username+':'+ name+str(total_layer)+'@'+' '
        else:
            print(f"/music compose append {name}{total_layer} " +text[i:i + chunk_size])
# for res in result:
# print(result)
total_layer = 0
for res in result:
    split_and_print(result[res], 200)
    total_layer=total_layer+1

print(f"/music pack create {name} {jiange}")
def split_print(text, chunk_size):
    for i in range(0, len(text), chunk_size):    
        if i==0:
            print(f"/music pack append {name}"+' '+'@'+username+':'+ name+str(total_layer)+'@'+' ')
total_layer = 0
for res in result:
    split_print(result[res], 200)
    total_layer=total_layer+1

print(play_command)
print(f"/music compose delete {name}0")
print(f"/music pack delete {name}")
    # print(sorted_dict)
# print(layer_lists[0])
# print(layer_last_tick)