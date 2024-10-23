import os

def clear_terminal():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Unix/Linux/Mac
    else:
        os.system('clear')



state_tasks = { "unlock the door": False, "look in the garderobe": False, "eat a dish": False,
"lay the table": False, "bake a cake": False, "open the fridge": False, "watch TV": False, "take remote": False,
"look behind the TV": False, "unlock bedroom 3": False, "unlock office": False, "look into the chest": False,
"unlock closet": False, "look under the bed": False, "go on computer": False, "take a shower": False, "take repairkit":False,
"unlock safe": False, "look in the mirror": False, "search the documents": False, "read a book": False, "sleep": False}

floor1_rooms = ["entrance", "dinning_room", "kitchen", "living_room"]
floor2_rooms = ["corridor", "bedroom1", "bedroom2", "bedroom3", "office", "bathroom", "toilet"]
all_rooms = ["entrance", "dinning_room", "kitchen", "living_room", "corridor", "bedroom1", "bedroom2", "bedroom3", "office", "bathroom", "toilet"]

player_venue = {"p0": "  ", "p1": "  ", "p2": "  ", "p3": "  ", "p4": "  ", "p5": "  ", "p6": "  ", "p7": "  ", "p8": "  ", "p9": "  ", "p10": "  "}

def player():
    global avatar
    global current_room
    global all_rooms
    for i in range(len(all_rooms)):
        if stringify(current_room) == all_rooms[i]:
            player_venue[f"p{i}"] = avatar
        else:
            player_venue[f"p{i}"] = "  "

#🧍
avatar = "🧑"
floor1 = lambda: f"""
                                           kitchen
 living room                          |––––––––––––––-|
|–––––––––––|   entrance __           |            (x)|
|(x)        |   |––-––––|//|stairs    |      {player_venue["p2"]}    (x)|
|           |___|        /_|          |  |––––––––––––|
|    {player_venue["p3"]}      ___          |   |–––––––|  |––––|
|           |   |         |___|               |
|    (x)    |   |(x) {player_venue["p0"]}    ___     (x)  {player_venue["p1"]} (x)|
|–––––––––––|   |         |   |––-––––––––––––|
                |––|(§)|––|      dinnig room
"""

floor2 = lambda: f"""
         bedroom1                                     
        |–––––––––––|   corridor __                  
        |(x)     (x)|___|––-––––|//|stairs                 
        |   {player_venue["p5"]}       ___         /_| |---------------|
        |___________|   |        |___|(x)    {player_venue["p8"]}   (x)|office
bedroom2|(x)     (x)|___|         _§_                |
        |(x) {player_venue["p6"]}      ___   {player_venue["p4"]}    |___|---------------|
        |–––––––––––|___|         ___                | 
bedroom3|(x)         _§_         |   |(x)    {player_venue["p9"]}   (x)|bathroom
        |(x)  {player_venue["p7"]}    |   |––| |––-|   |––-––––––––––––|
        |___________|   |  {player_venue["p10"]} (x)|
                        |--------|
                         toilet      
"""


def statment(state_task):
   if not (state_tasks[state_task]):
       state_tasks[state_task] = True
   return ""
   
achivement_variables = {"eat a dish": 0, "sleep": 0, "unlock bedroom 3": 0, "go on computer": 0, "unlock safe": 0}

def true_maker_achivement(achivement, max_value = 2):
    if achivement_variables[achivement] == max_value:
        state_tasks[achivement] = True

def achivements(achivement):
    achivement_variables[achivement] += 1
    return achivement_variables[achivement]

executer_tasks_recieved = []

def automatic_achivement(achivement, executer_task, max_value = 2):
    if executer_task in executer_tasks_recieved:
        progress = achivement_variables[achivement]
    else:
        progress = achivements(achivement)
    executer_tasks_recieved.append(executer_task)
    true_maker_achivement(achivement, max_value)
    return f"[achivement: {progress}/{max_value} of '{achivement}' enabled]"

class Room:
   def __init__(self, name, room_neighbors, task_array, state_lambdas):
       self.name = name
       self.neighbors = room_neighbors
       self.tasks = []
       self.tasks.extend(task_array)
       self.state_lambdas = state_lambdas

   def look_state_task(self, task):
       i = self.tasks.index(task)
       index = i*2
       true_state_lambdas = self.state_lambdas[index]
       false_state_lambdas = self.state_lambdas[(index+1)]
       if state_tasks[task]:
           print("\033[93m" + true_state_lambdas() + "\033[0m") #because it is a lambda we do ()
       else:
           print("\033[93m" + false_state_lambdas() + "\033[0m")

def objectify(roomname):
    global current_room
    current_room = eval(roomname)
    return " "

entrance = Room("entrance", ["living_room", "dinning_room", "stairs"], 
["unlock the door", "look in the garderobe"], [
    lambda: f"Congratulations! You escaped!{quit()}",  #we use lambda so the code inside the string will be not executed
    lambda: "You need the door keys to unlock it",
    lambda: f"You have found the closet-keys {statment('unlock closet')}",
    lambda: "The garderobe is broken, you need the repairkit to open it"
    ])

dinning_room = Room("dinning_room", ["entrance", "kitchen"],
["eat a dish", "lay the table"], [
    lambda: f"You have eaten well and feel now tired! {automatic_achivement('sleep', 'eat a dish')}", 
    lambda: f"You need to some things before eating a dish [{achivement_variables['eat a dish']}/2 things done]", 
    lambda: "You have already layed the table",
    lambda: f"You have sucessfully layed the table {automatic_achivement('eat a dish', 'lay the table')}{statment('lay the table')}"
    ])

kitchen = Room("kitchen", ["dinning_room"],
["bake a cake", "open the fridge"], [
    lambda: f"Nice you have now baked a cake {automatic_achivement('eat a dish', 'bake a cake')}", 
    lambda: "Sorry, you need to gather ingreadiants for making a cake", 
    lambda: "There is nothing in the fridge", 
    lambda: f"You have now gathered ingreadiants to make a cake {statment('bake a cake')}{statment('open the fridge')}"
    ])

living_room = Room("living_room", ["entrance"],
["watch TV", "look behind the TV"], [
    lambda: f"You know have the knowledge to start a computer {automatic_achivement('go on computer', 'watch TV')}",
    lambda: "You need the remote to activate the TV",
    lambda: f"You have now writtend down the wifi password {automatic_achivement('go on computer', 'look behind the TV')}",
    lambda: "You see the wifi password, you need to have a pen to write the wifi password down"
    ])

stairs = Room("stairs", ["entrance", "corridor"], [], [])

corridor = Room("corridor", ["bedroom1", "bedroom2", "toilet", "bathroom", "stairs"],
["unlock office","unlock bedroom 3"], [
    lambda: f"You have now entered the office {objectify('office')}", #through this task the player is teleported immediately in the office and there will be no "office" choice in the room menu
    lambda: "You need the office-keys to enter the office",
    lambda: f"You have now entered the bedroom 3 {objectify('bedroom3')}",
    lambda: f"You need the bedroom-3-keys to enter the bedroom 3 [make a the bedroom-3-keys {achivement_variables['unlock bedroom 3']}/3 completed]"
])

bedroom1 = Room("bedroom1", ["corridor"],
["look under the bed", "unlock closet"], [
    lambda: f"You have found a keymaker under your bed {automatic_achivement('unlock bedroom 3', 'look under the bed', 3)}",
    lambda: "There is a monster under your bed, you need to sleep to make it go away",
    lambda: f"You have found the office-keys {statment('unlock office')}",
    lambda: "You need the closet-keys to open the closet"
])

bedroom2 = Room("bedroom2", ["corridor"],
["take remote", "sleep", "look into the chest"], [
    lambda: "You have already taken the remote",
    lambda: f"You have now taken the remote {statment('watch TV')}{statment('take remote')}",
    lambda: f"Cool it is already morning, there are no monsters at day-time and you can now read books{statment('look under the bed')}{statment('read a book')}",
    lambda: f"You need to some things before going to bed [{achivement_variables['sleep']}/2 things done]",
    lambda: "There is nothing in the chest",
    lambda: f"You have found a blueprint of the bedroom-3-keys under your bed {automatic_achivement('unlock bedroom 3', 'look into the chest', 3)}{statment('look into the chest')}"
])

bedroom3 = Room("bedroom3", ["corridor"],
["go on computer", "unlock safe"], [
    lambda: f"You know know the first part of the pin of the safe {automatic_achivement('unlock safe', 'go on computer')}",
    lambda: f"You need to some things before going on the computer [{achivement_variables['go on computer']}/2 things done]",
    lambda: f"You have now found the keys of the exit door {statment('unlock the door')}",
    lambda: f"You need to know the 2 parts of the pin code to open the safe [{achivement_variables['unlock safe']}/2 parts found]"
])

bathroom = Room("bathroom", ["corridor"],
["look in the mirror","take a shower"], [
    lambda: "You look as always",
    lambda: f"You look beautiful, oh silly you, you have found a pen in your hair {statment('look behind the TV')}{statment('look in the mirror')}",
    lambda: "You are now clean",
    lambda: f"You look beautiful, oh silly you, you have found a pen in your hair {automatic_achivement('sleep', 'take a shower')}{statment('take a shower')}"

])

office = Room("office", ["corridor"],
["search the documents", "read a book"], [
    lambda: "You have found nothing",
    lambda: f"You know know the second part of the pin of the safe {automatic_achivement('unlock safe', 'search the documents')}",
    lambda: f"You now know how to make a key {automatic_achivement('unlock bedroom 3', 'read a book', 3)}",
    lambda: "You are too tired to read a book, you need to sleep first"
])

toilet = Room("toilet", ["corridor"],
["take repairkit"], [
    lambda: "You already have the repairkit with you", 
    lambda: f"You now have a repair kit with you {statment('look in the garderobe')}{statment('take repairkit')}"
    ])

#set all to initial status
def reset():
    for task in state_tasks:
        state_tasks[task] = False

    for achivement in achivement_variables:
        achivement_variables[achivement] = 0

#reset()

#testing
"""
dinning_room.look_state_task("eat a dish")
dinning_room.look_state_task("lay the table")
dinning_room.look_state_task("lay the table")
kitchen.look_state_task("bake a cake")
kitchen.look_state_task("open the fridge")
kitchen.look_state_task("open the fridge")
kitchen.look_state_task("bake a cake")
kitchen.look_state_task("bake a cake")
dinning_room.look_state_task("eat a dish")
dinning_room.look_state_task("eat a dish")
"""
#solve the problem that you can only go to the office when you have unlocked the office, the same goes with the bedroom 3


print("""\033[45m
///////////////Escape Room///////////////

You are locked in a house, 
complete tasks to find the keys to unlock the entrance door

Press a letter to go to a different room
Press a number to do a task
    
Have fun!
Creator: Vladislav Feyereisen
\033[0m""")

current_room = entrance
validator_array = {}

def stringify(room):
    return room.name

while True:
    player()

    if stringify(current_room) in floor1_rooms:
        print(floor1())
    else:
        print(floor2())

    print("Current Room: " + "\033[92m" + stringify(current_room) + "\033[0m")
    print("")
    print("Neighboring rooms:")
    for index in range(len(current_room.neighbors)):
        neigboring_room = current_room.neighbors[index]
        letter = chr(97+index)
        validator_array[letter] = neigboring_room
        print("\033[96m" + f"({letter}) {neigboring_room} " + "\033[0m", end="| ")
    print()
    print("")
    print("tasks available in this room:")
    for index in range(len(current_room.tasks)):
        task = current_room.tasks[index]
        number = str(index + 1)
        validator_array[number] = task
        print("\033[96m" + f"({number}) {task} " + "\033[0m", end="| ")
    
    print()
    print("")
    
    try:
        action_chosen = input("Please choose your action: ")
        clear_terminal()
        if action_chosen in validator_array:
            action = validator_array[action_chosen.lower()]
            try:
                pure_task = int(action_chosen)
                print("//////////////////////////////")
                current_room.look_state_task(action)
                validator_array.clear()
            except ValueError:
                if action == "stairs":
                    if current_room == entrance:
                        current_room = eval("corridor")
                    else:
                        current_room = eval("entrance")
                else:
                    current_room = eval(action)
                validator_array.clear()
        else:
            print(f"\033[91m" + "/////// Invalid Action  /////// " + "\033[0m")
    except ValueError:
        print("Error 404")
    print("//////////////////////////////")
    

