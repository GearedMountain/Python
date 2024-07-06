def FindConnected(inptph):
    input = open(inptph, "r", encoding='UTF-8') 
    data = input.read() 
    answer = ""
    cordmap = data.split("\n") 
    input.close()  
    # printing the data 
    rows = 1
    columns = 1
    pipemap = {}
    
    #Find the asterik and row / column size 
    startcoord = ""
    for i in cordmap:
        coord = i.split(" ")
        pipemap[coord[1] + "," + coord[2]] = coord[0]
        if coord[0] == "*":
            startcoord = coord[1] + "," + coord[2]
        if int(coord[1]) > columns:
            columns = int(coord[1])
        if int(coord[2]) > rows:
            rows = int(coord[2])
    fillmap = {} 
    fillmap[startcoord] = "*"
    currentcoord = startcoord
    
    # stack used for checking values, 
    fillstack = []
    fillstack.append(currentcoord)
    
    # While loop that continues interating until every currently connected pipe has been checked
    while len(fillstack) > 0:
        currentcoord = fillstack[0]
    
        x = currentcoord.split(",")[0]
        y = currentcoord.split(",")[1]
        if pipemap[currentcoord].isalpha():
            answer += pipemap[currentcoord]
            
        # First ensure pipe can go in that direction, then tested in try except incase entry doesnt exist
        if pipemap[currentcoord] not in ["╝","╣","╗","║"," "]:
            try:
                if pipemap[str(int(x)+1) + "," + str(y)] not in ["╚","╔","║","╠"," "] and str(int(x)+1) + "," + str(y) not in fillmap:
                    fillmap[str(int(x)+1) + "," + str(y)] = pipemap[str(int(x)+1) + "," + str(y)]
                    fillstack.append(str(int(x)+1) + "," + str(y))
            except Exception as error:
                print("")
        
        if pipemap[currentcoord] not in ["╚","═","╩","╝"," "]:
            try:
                if pipemap[str(str(x)) + "," + str(int(y)-1)] not in ["╦","╔","╗","═"," "] and str(str(x)) + "," + str(int(y)-1) not in fillmap:
                    fillmap[str(str(x)) + "," + str(int(y)-1)] = pipemap[str(x) + "," + str(int(y)-1)]
                    fillstack.append(str(str(x)) + "," + str(int(y)-1))
            except Exception as error:
                print("")
        
        if pipemap[currentcoord] not in ["╚","╔","║","╠"," "]:
            try:
                if pipemap[str(int(x)-1) + "," + str(y)] not in ["╝","╣","╗","║"," "] and str(int(x)-1) + "," + str(y) not in fillmap:
                    fillmap[str(int(x)-1) + "," + str(y)] = pipemap[str(int(x)-1) + "," + str(y)]
                    fillstack.append(str(int(x)-1) + "," + str(y))
            except Exception as error:
                print("")
    
        if pipemap[currentcoord] not in ["╦","╔","╗","═"," "]:
            try:
                if pipemap[str(x) + "," + str(int(y)+1)] not in ["╚","═","╩","╝"," "] and str(x) + "," + str(int(y)+1) not in fillmap:
                    fillmap[str(x) + "," + str(int(y)+1)] = pipemap[str(x) + "," + str(int(y)+1)]
                    fillstack.append(str(x) + "," + str(int(y)+1))
            except Exception as error:
                print("")
        
        fillstack.remove(currentcoord)
    for i in range(rows+1):
        i = rows - i
        rowout = ""
        for j in range(columns+1):
            try: 
                rowout += pipemap[str(j) + "," + str(i)]
            except: 
                rowout += " "
        print(rowout)
        
    print(" ")
    print(" ")
    print(" ")
    
    for i in range(rows+1):
        i = rows - i
        rowout = ""
        for j in range(columns+1):
            try: 
                rowout += fillmap[str(j) + "," + str(i)]
            except: 
                rowout += " "
        print(rowout)
    
    # Ensure the answer string is alphabetical order
    
    return "".join(sorted(answer))
print(FindConnected("coding_qual_input.txt"))
