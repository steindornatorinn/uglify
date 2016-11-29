import re

def uglify(filename):
    '''Takes a short python script and removes any syntactic sugar such as
    comments, descriptive variable name and booleans and shortens them.
    This function takes a filename as input and outputs the result into a file called
    original_ugly.py'''
    #Open a file and read from it
    inFile = open(filename, 'r')
    workString = inFile.read()

    #Create a list to host our symbols for now
    symbolList = []

    #replace tabs with 4 spaces
    p = re.compile('\t')
    match = p.search(workString)
    while(match):
        workString = workString[:match.start()] + "    " + workString[match.end():]
        match = p.search(workString)

    #replace True with 1 and False with 0
    p = re.compile('True')
    match = p.search(workString)
    while(match):
        workString = workString[:match.start()] + "1" + workString[match.end():]
        match = p.search(workString)

    p = re.compile('False')
    match = p.search(workString)
    while(match):
        workString = workString[:match.start()] + "0" + workString[match.end():]
        match = p.search(workString)


        
    #Remove the comments
    p = re.compile('[ |\t]*#[^\n]*\n')
    match = p.search(workString)
    while(match):
        workString = workString[:match.start()] + workString[match.end():]
        match = p.search(workString)
        
    p = re.compile('[ |\t]*\'\'\'[^\']*\'\'\'[^\n]*\n')
    match = p.search(workString)
    while(match):
        workString = workString[:match.start()] + workString[match.end():]
        match = p.search(workString)
    
    #Find all instances of variable assignment and insert into our symbol table
    p = re.compile('\w+ ?=')
    matches = p.findall(workString)
    for match in matches:
        if(match[-2] == ' '):
            match = match[0:-2]
        symbolList.append(match)

    #Find all instances of our own functions and insert into our symbol table
    p = re.compile('def \w+\s?\(\s?\w+')
    p2 = re.compile('\(\s?\w+')
    p3 = re.compile('\w+')
    matches = p.findall(workString)
    for match in matches:
        temp = p2.findall(match)
        temp = p3.findall(temp[0])
        symbolList.append(temp[0])

    #Same stuff but for argument 2
    p = re.compile('def \w+\s?\(\s?\w+\s?,\s?\w+')
    p2 = re.compile(',\s?\w+')
    p3 = re.compile('\w+')
    matches = p.findall(workString)
    for match in matches:
        temp = p2.findall(match)
        temp = p3.findall(temp[0])
        symbolList.append(temp[0])

    #Same stuff but for argument 3
    p = re.compile('def \w+\s?\(\s?\w+\s?,\s?\w+,\s?\w+')
    p2 = re.compile(',\s?\w+,s?\w+')
    p3 = re.compile('\w+')
    matches = p.findall(workString)
    for match in matches:
        temp = p2.findall(match)
        temp = p3.findall(temp[0])
        symbolList.append(temp[1])

    #Same stuff but for for loops
    p = re.compile('for \w+ in')
    p2 = re.compile(' \w+ ')
    p3 = re.compile('\w+')
    matches = p.findall(workString)
    for match in matches:
        temp = p2.findall(match)
        temp = p3.findall(temp[0])
        symbolList.append(temp[0])

        
    #remove duplicates and symbols that are too short to simplify
    symbolList[:] = [string for string in symbolList if len(string) >= 3]
    symbolList =  list(set(symbolList))


    #create a dictionary for them
    symDict = {}
    character = 'A'
    for item in symbolList:
        if(ord(character) > ord('Z')):
            character = 'A'
        symDict[item] = character
        character = chr(ord(character)+1)
    print(symDict)

    #replace all instances of these identifiers in our file
    for item in symbolList:
        p = re.compile('[^\w]' + item + '[^\w]')
        match = p.search(workString)
        while(match):
            workString = workString[:match.start()+1] + symDict[item]+ workString[match.end()-1:]
            match = p.search(workString)
        

    #write it out
    outfile = open(filename[:-3] + '_ugly.py', 'w')
    outfile.write(workString)
