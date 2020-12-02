import json
grid = [0]*361
reference = ["╋ ", "○", "●"]
char_reference = [chr(x) for x in range(65, 84)]
command = [""]
history = []

def show(grid):
    global reference
    print("    A B C D E F G H I J K L M N O P Q R S")
    for y in range(19):
        print(y+1, end=" ")
        if (y+1) // 10 < 1: print(end=" ")
        for x in range(19): 
            print(reference[grid[y*19+x]], end="")
        print("")

def place(command, x, y):
    global grid

    if len(command) == 3 and command[1] in char_reference and int(command[2])<=19 and int(command[2])>=1: 
        corr = char_reference.index(command[1])+(int(command[2])-1)*19
    else: 
        input("Parameter Error: format should be {[black/white] [A-S] [1-19]}...")
        return
    
    if grid[corr] == 0:
        histroy_branch = [y, corr]
        grid[corr] = x
        if corr-19 >= 0 and grid[corr-19] != x: 
            if surround(corr-19, x): histroy_branch.append(-19)
        if corr+19 <= 360 and grid[corr+19] != x: 
            if surround(corr+19, x): histroy_branch.append(19)
        if corr%19 != 0 and grid[corr-1] != x:
            if surround(corr-1, x): histroy_branch.append(-1)
        if corr%19 != 18 and grid[corr+1] != x: 
            if surround(corr+1, x): histroy_branch.append(1)

        if surround(corr, y): input("Invalid location...")
        else: history.append(histroy_branch)

    else: input("This point has been taken up...")

def surround(index, s):
    visited = []
    def check(index):
        global grid, char_reference
        if grid[index] == 0: return False
        elif grid[index] == s: return True
        visited.append(index)
        direction = [True, True, True, True]
        if index-19 >= 0 and index-19 not in visited: direction[0] = check(index-19)
        if index+19 <= 360 and index+19 not in visited: direction[1] = check(index+19)
        if index % 19 != 0 and index-1 not in visited: direction[2] = check(index-1)
        if index % 19 != 18 and index+1 not in visited: direction[3] = check(index+1)
        return False not in direction
    if check(index):
        for corr in visited:
            grid[corr] = 0
        return True
    return False

def spread(index, i):
    global grid
    grid[index] = i
    if index-19 >= 0 and grid[index-19] == 0: spread(index-19, i)
    if index+19 <= 360 and grid[index+19] == 0: spread(index+19, i)
    if index % 19 != 0 and grid[index-1] == 0: spread(index-19, i)
    if index % 19 != 18 and grid[index+1] == 0: spread(index+1, i)

while True:

    try:
        print(history)

        show(grid)
        command = input(">> ").split(" ")
        
        if command[0] == "black":
            place(command, 1, 2)
        
        elif command[0] == "white":
            place(command, 2, 1)

        elif command[0] == "remove":
            if len(command) == 3 and command[1] in char_reference and int(command[2])<=19 and int(command[2])>=1: 
                grid[char_reference.index(command[1])+(int(command[2])-1)*19] = 0
            else: 
                input("Parameter Error: format should be {black [A-S] [1-19]}...")
                continue
        
        elif command[0] == "withdraw":
            action = history[-1]
            print(action)
            del history[-1]

            if len(action) >= 3:
                for restore in action[2:]:
                    print(restore)
                    spread(action[1]+restore, action[0])
            
            grid[action[1]] = 0

        elif command[0] == "clear":
            if input("Are you sure to clear the sle game? (type Yes to confirm): ") == "Yes": grid = [0]*441
        
        elif command[0] == "file":

            file_command = [""]
            with open("record.json", "r") as file:
                data = json.load(file)

            while True:

                file_command = input("file>> ").split(" ")

                if file_command[0] == "save":
                    if len(file_command) >= 2:
                        if data.__contains__(file_command[1]):
                            if input("This file is existed, cover it? (type Yes to confirm): ") != "Yes":
                                continue
                        data[file_command[1]] = grid
                        print("success")
                    else: input("Please give the game a name...")

                elif file_command[0] == "load":
                    if len(file_command) >= 2:
                        if data.__contains__(file_command[1]):
                            if input("Throw the current and load this file? (type Yes to confirm): ") == "Yes":
                                grid = data[file_command[1]]
                                print("success")
                        else: input("file doesn't exist...")
                    else: input("Missing the name of the file...")
                
                elif file_command[0] == "delete":
                    if len(file_command) >= 2:
                        if data.__contains__(file_command[1]):
                            if input("Sure to delete it? (type Yes to confirm): ") == "Yes":
                                del data[file_command[1]]
                                print("success")
                        else: input("file doesn't exist...")
                    else: input("Missing the name of the file...")

                elif file_command[0] == "list":
                    if data.keys() != []:
                        for name in data.keys():
                            print(name)
                    else:
                        print("**empty**")
                
                elif file_command[0] == "exit":
                    break
                
                else: print("Unknown command")
            
            with open("record.json", "w") as file:
                json.dump(data, file)
        
        elif command[0] == "exit": break
                
        else: print("Unknown command")

    except:
        print("Unknown Error (Hope you can report it at https://github.com/GT-gt-gt/cmd_Go)")
