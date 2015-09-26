from Tkinter import *
import math, random, copy

def convertSVGPathToXYPointsCounties(path):
    #print path
    points = [[]] #2D list, each with points for a create_polygon function
    directions = path.split(" ")
    currentPhase = ""
    index = 0
    while (len(directions) > 0):
        if directions[0] == '': break
        if (directions[0].isalpha()): 
            if (directions[0] == "M" and len(points[0]) >= 1):
                #print "yay!"
                index += 1
                points.append([])
            currentPhase = directions[0]
            directions.pop(0)
        elif (currentPhase == "M" or currentPhase == "L"): # Move Path
            endI = directions[0].find(",")
            points[index].append(1.689*float(directions[0][0:endI])-10.69926)
            points[index].append(1.679*float(directions[0][endI+1:])+7.1097734)
            directions.pop(0)
    return points

def drawSVGPathsCounties(fileName):
    (paths, width, height) = convertSVGFileToDictOfPathsCounties(fileName)
    # (michigan1, michigan2) = (paths["MI-"], paths["SP-"])
    # paths["MI"] = [michigan1, michigan2]
    # paths.pop("MI-")
    # paths.pop("SP-")
    print paths.keys()
    # statesData = sampleStatesData()
    # (colorData, colors) = colorStatesData(statesData)
    for ID in paths:
        # print ID, paths[ID]
        # if (ID == "MI"):
        #     points = convertSVGPathToXYPoints(paths[ID][0])
        #     points += convertSVGPathToXYPoints(paths[ID][1])
        # else:
        points = convertSVGPathToXYPointsCounties(paths[ID])
        #print ID, points
        for point in points:
            if (len(ID) == 5):
            #     #print ID, point
            #     rgbColor = colorData[ID]
            #     color = eval(rgbColor)
                color = rgb(int(ID)%256, int(ID)%128, int(ID)%64)
                canvas.create_polygon(*point, fill=color, outline="black")
            else:
            #     rgbColor = colors[-1]
            #     color = eval(rgbColor)
                canvas.create_line(*point, fill="black", width=2)
    # print paths["13273"]
    # points = convertSVGPathToXYPoints(paths["13273"])
    # print points
    # for point in points:
    #     print "yay"
    #     canvas.create_polygon(*point, fill="red", outline="black")
    # button1 = Button(text = "Quit", anchor = W)
    # button1.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
    # sv = StringVar()
    # e = Entry(textvariable=sv)
    # sv.set("Search")
    # sv.trace("w", lambda name, index, mode, sv=sv, e=e: hello(sv, e))
    # e_window = canvas.create_window(10, 10, anchor=NW, window=e)
    # root.bind("<Button-1>", mouseClick)

def convertSVGFileToDictOfPathsCounties(name):
    svg = open(name, 'r').read()
    (width, height) = (0,0)
    paths = dict()
    svgCode = svg.split("\n")
    for svgCodeI in xrange(len(svgCode)):
        code = svgCode[svgCodeI]
        if ('d="M' in code):
            beginI = svgCode[svgCodeI+1].find("id=")+4
            endI = svgCode[svgCodeI+1].find("\"", beginI)
            ID = svgCode[svgCodeI+1][beginI:endI]
            beginI = code.find("\"")+1
            endI = code.find("\"", beginI)
            drawInstructions = code[beginI:endI]
            paths[ID] = drawInstructions
        elif ("width=" in code ):
            beginI = code.find("width=")+7
            endI = code.find("\"", beginI)
            width = float(code[beginI:endI])
        if ("height=" in code):
            beginI = code.find("height=")+8
            endI = code.find("\"", beginI)
            height = float(code[beginI:endI])
    #print paths, width, height
    return (paths, width, height)

def convertSVGPathToXYPoints(path):
    #print path
    points = [[]] #2D list, each with points for a create_polygon function
    directions = path.split(" ")
    currentPhase = ""
    index = 0
    while (len(directions) > 0):
        (xOffset, yOffset) = (0.0,0.0)
        if (directions[0].isalpha()): 
            if (directions[0] == "c"): #I have not implemented curves yet.  However, they only have a tiny change, so I will remove them.  However, I have to account for their offset
                while (not directions[1].isalpha()):
                    endI = directions[1].find(",")
                    xOffset += float(directions[1][0:endI])
                    yOffset += float(directions[1][endI+1:])
                    directions.pop(1)
                if (len(directions) == 2): break
                else: directions.pop(1)
            if (directions[0].lower() == "m" and len(points[0]) >= 1):
                #print "yay!"
                index += 1
                points.append([])
            currentPhase = directions[0]
            directions.pop(0)
        if (currentPhase == "m" or currentPhase == "c" or currentPhase == "l"): # Move Path
            endI = directions[0].find(",")
            if (len(points[index]) == 0): # Initial Point
                if (len(points) == 1):
                    points[index].append(float(directions[0][0:endI]))
                    points[index].append(float(directions[0][endI+1:]))
                else:
                    points[index].append(points[index-1][-2] + xOffset/2 + float(directions[0][0:endI]))
                    points[index].append(points[index-1][-1] + yOffset/2 + float(directions[0][endI+1:]))
            else:
                points[index].append(points[index][-2] + xOffset/2 + float(directions[0][0:endI]))
                points[index].append(points[index][-2] + yOffset/2 + float(directions[0][endI+1:]))
            directions.pop(0)
        elif (currentPhase == "M"): #Absolute Move Path
            endI = directions[0].find(",")
            points[index].append(float(directions[0][0:endI]))
            points[index].append(float(directions[0][endI+1:]))
            directions.pop(0)
        elif (currentPhase == "v"): #Vertical Line
            points[index].append(points[index][-2])
            points[index].append(points[index][-2] + float(directions[0]))
            directions.pop(0)
        elif (currentPhase == "h"): #Horizontal Line
            points[index].append(points[index][-2] + float(directions[0]))
            points[index].append(points[index][-2])
            directions.pop(0)
    return points

def drawSVGPaths(fileName):
    (paths, width, height) = convertSVGFileToDictOfPaths(fileName)
    # root = Tk()
    # canvas = Canvas(root, width=width, height=height)
    # canvas.pack()
    # (michigan1, michigan2) = (paths["MI-"], paths["SP-"])
    # paths["MI"] = [michigan1, michigan2]
    # paths.pop("MI-")
    # paths.pop("SP-")
    print paths.keys()
    statesData = sampleStatesData()
    (colorData, colors) = colorStatesData(statesData)
    for ID in paths:
        if (ID == "MI"):
            points = convertSVGPathToXYPoints(paths[ID][0])
            points += convertSVGPathToXYPoints(paths[ID][1])
        else:
            points = convertSVGPathToXYPoints(paths[ID])
        #print ID, points
        for point in points:
            if (len(ID) <= 3 and ID != "AK" and ID != "HI" and ID != "FL" and ID != "MI" and ID != "ME"):
                #print ID, point
                rgbColor = colorData[ID]
                color = eval(rgbColor)
                #color = rgbString(ord(ID[0])+ord(ID[1]), ord(ID[1])%ord(ID[0]), 255)
                canvas.create_line(*point, width=4, fill="white")
            # else:
            #     rgbColor = colors[-1]
            #     color = eval(rgbColor)
            #     canvas.create_line(*point, width=3, fill="black")
    # points = convertSVGPathToXYPoints(paths["ID"])
    # print points
    # for point in points:
    #     print "yay"
    #     canvas.create_polygon(*point, fill="red", outline="black")
    button1 = Button(text = "Quit", anchor = W, command=testButton)
    button1.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
    # sv = StringVar()
    # e = Entry(textvariable=sv)
    # sv.set("Search")
    # sv.trace("w", lambda name, index, mode, sv=sv, e=e: hello(sv, e))
    button1Window = canvas.create_window(100, 100, anchor=NW, window=button1)
    # root.bind("<Button-1>", mouseClick)
    canvas.mainloop()

def testButton():
    print "hello"

def hello(var, entry):
    print var.get(), entry.cget("state")

def mouseClick(*args):
    print "mouseClick"

def rgb(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

def sampleStatesData():
    states = ['WA', 'DE', 'DC', 'WI', 'WV', 'HI', 'FL', 'WY', 'NH', 'NJ', 'NM', 'TX', 'LA', 'NC', 'ND', 'NE', 'TN', 'NY', 'PA', 'MT', 'RI', 'NV', 'VA', 'CO', 'AK', 'AL', 'AR', 'VT', 'GA', 'IN', 'IA', 'MA', 'AZ', 'CA', 'ID', 'CT', 'ME', 'MD', 'OH', 'UT', 'MO', 'MN', 'MI', 'KS', 'OK', 'MS', 'SC', 'KY', 'SD', 'OR', 'IL']
    states.sort()
    statesData = dict()
    i = 0
    for state in states:
        statesData[state] = i
        i += 1
    return statesData

def maxStateData(statesData):
    maximum = statesData[statesData.keys()[0]]
    for state in statesData:
        if (statesData[state] > maximum):
            maximum = statesData[state]
    return maximum

def normalizeStatesData(statesData, maximum):
    normalizedData = dict()
    for state in statesData:
        normalizedData[state] = statesData[state]/float(maximum)
    return normalizedData

    
def colorStatesData(statesData, numberOfColors=5):
    colorData = open("colorbrewer.json").read()
    print colorData.find("\n")
    colorSchemes = eval(colorData)
    colorScheme = random.choice(colorSchemes.keys())
    colors = colorSchemes[colorScheme][str(numberOfColors)]
    maximum = maxStateData(statesData)
    normalizedData = normalizeStatesData(statesData, maximum)
    colorData = dict()
    for state in normalizedData:
        colorIndex = int(normalizedData[state]*len(colors))
        if (colorIndex == numberOfColors): colorIndex -= 1
        colorData[state] = colors[colorIndex]
    return (colorData, colors)

def convertSVGFileToDictOfPaths(name):
    svg = open(name, 'r').read()
    (width, height) = (0,0)
    paths = dict()
    svgCode = svg.split("\n")
    for svgCodeI in xrange(len(svgCode)):
        code = svgCode[svgCodeI]
        if ("<path" in code):
            beginI = code.find("id=")+4
            endI = code.find("\"", beginI)
            ID = code[beginI:endI]
            beginI = code.find("\"")+1
            endI = code.find("\"", beginI)
            drawInstructions = code[beginI:endI]
            paths[ID] = drawInstructions
        elif ("width=" in code ):
            beginI = code.find("width=")+7
            endI = code.find("\"", beginI)
            width = float(code[beginI:endI])
        if ("height=" in code):
            beginI = code.find("height=")+8
            endI = code.find("\"", beginI)
            height = float(code[beginI:endI])
    #print paths, width, height
    return (paths, width, height)

if (__name__ == "__main__"):
    (paths, width, height) = convertSVGFileToDictOfPathsCounties('USA_Counties_with_FIPS_and_names.svg')
    root = Tk()
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    drawSVGPathsCounties('USA_Counties_with_FIPS_and_names.svg')
    drawSVGPaths('BlankMap-World6.svg')
    canvas.mainloop()