################################################################################
# File Name: svgToTkinter.py

# File Description: Parses SVG code in python, converts it into lists of (x,y) 
# polygon coordinates, and draws it on a Tkinter canvas

# File Author: Amal Nanavati
################################################################################

from Tkinter import *

class SVG(object):
    """An object that parses an SVG file, allowing the data to be searched and \
    rendered in Python/Tkinter"""

    def __init__(self, filePath):
        """Initialize the SVG object"""
        self.filePath = filePath
        self.svgPaths = {} # Dictionary to store the SVG paths in
        self.parseSVGFile()
        # The map we are using separates the two parts of MI, hence
        # combine them into one state
        MI1 = self.svgPaths.pop("MI-")
        MI2 = self.svgPaths.pop("SP-")
        self.svgPaths["MI"] = MI1+MI2

        
    def __str__(self):
        """Print the file path of the SVG object"""
        return self.filePath

    def parseSVGFile(self):
        """Parse the SVG object"""
        try:
            data = open(self.filePath, 'r').read()
        except:
            raise Exception('Could not load %s : File does not exist', 
                            self.filePath)
        tags = data.split('>') # Get a list of each set of tags
        # Iterate over tags
        for svgTag in tags:
            if "<svg" in svgTag:
                self.getWidthHeight(svgTag)
            elif "<path" in svgTag:
                self.getSVGPath(svgTag)

    def getWidthHeight(self, svgTag):
        """Gets the width and height of the SVG image from the tag containing
        "<svg".  """
        if "width" in svgTag:
            beginI = svgTag.find("width=")+len('width="')
            endI = svgTag.find("\"", beginI)
            self.width = float(svgTag[beginI:endI])
        if "height" in svgTag:
            beginI = svgTag.find("height=")+len('height="')
            endI = svgTag.find("\"", beginI)
            self.height = float(svgTag[beginI:endI])

    def getSVGPath(self, svgTag):
        """Given a SVG path, adds it to the dictionary of IDs and polygon paths"""
        print repr(svgTag)
        # Get the Path ID
        beginI = svgTag.find(" id=")+len(' id="')
        endI = svgTag.find("\"", beginI)
        ID = svgTag[beginI:endI]
        print ID
        # Get the path code
        beginI = svgTag.find(" d=")+len(' d="')
        endI = svgTag.find("\"", beginI)
        pathCode = svgTag[beginI:endI]
        print pathCode
        self.svgPaths[ID] = self.convertSVGPathToXYCoordinates(pathCode)

    def convertSVGPathToXYCoordinates(self, pathCode):
        """Converts the instructions in the SVG file to a list of (x,y)
        coordinates that can be used to draw the path"""
        xyPoints = [] #2D list of (x,y) tuples
        directions = pathCode.split(" ") # splits pathCode into its directions and
                                         # arguments
        command = ""
        while (len(directions) > 0):
            if directions[0] == '': 
                directions.pop(0)
                break
            if directions[0].isalpha():
                command = directions.pop(0)
                if (command == "M" or command == "m"):
                    xyPoints.append([])
            # if len(directions) == 0: 
            #     raise Exception("Invalid number of arguments for %s", command)

            # Move commands (absolute and relative)

            if (command == "M"):
                while "," not in directions[0]:
                    directions[0] += directions.pop(1)
                arguments = directions.pop(0).split(",")
                x = float(arguments[0].strip())
                y = float(arguments[1].strip())
                xyPoints[-1].append((x,y))
            elif (command == "m"):
                while "," not in directions[0]:
                    directions[0] += directions.pop(1)
                arguments = directions.pop(0).split(",")
                print arguments
                dx = float(arguments[0].strip())
                dy = float(arguments[1].strip())
                if len(xyPoints) == 1 and len(xyPoints[0]) == 0:
                    (x0,y0) = (0,0)
                elif (len(xyPoints[-1]) == 0):
                    (x0,y0) = xyPoints[-2][-1]
                else:
                    (x0,y0) = xyPoints[-1][-1]
                (x,y) = (x0+dx,y0+dy)
                xyPoints[-1].append((x,y))

            # Line commands (absolute and relative)

            if (command == "L"):
                while "," not in directions[0]:
                    directions[0] += directions.pop(1)
                arguments = directions.pop(0).split(",")
                x = float(arguments[0].strip())
                y = float(arguments[1].strip())
                xyPoints[-1].append((x,y))
            elif (command == "l"):
                while "," not in directions[0]:
                    directions[0] += directions.pop(1)
                arguments = directions.pop(0).split(",")
                dx = float(arguments[0].strip())
                dy = float(arguments[1].strip())
                (x0,y0) = xyPoints[-1][-1]
                (x,y) = (x0+dx,y0+dy)
                xyPoints[-1].append((x,y))

            # Horizontal Line (absolute and relative)

            if (command == "H"):
                argument = directions.pop(0)
                x = float(argument.strip())
                y0 = xyPoints[-1][-1][1]
                xyPoints[-1].append((x,y0))
            elif (command == "h"):
                argument = directions.pop(0)
                dx = float(argument.strip())
                (x0,y0) = xyPoints[-1][-1]
                (x,y) = (x0+dx,y0)
                xyPoints[-1].append((x,y))

            # Vertical Line (absolute and relative)

            if (command == "V"):
                argument = directions.pop(0)
                y = float(argument.strip())
                x0 = xyPoints[-1][-1][0]
                xyPoints[-1].append((x0,y))
            elif (command == "v"):
                argument = directions.pop(0)
                dy = float(argument.strip())
                (x0,y0) = xyPoints[-1][-1]
                (x,y) = (x0,y0+dy)
                xyPoints[-1].append((x,y))

            # Close Path

            if (command == "Z" or command == "z"):
                pass

            # Curve Command (not yet implemented)

            if (command == "C"):
                lastArguments = ("","")
                while (len (directions) != 0 and not directions[0].isalpha()): 
                    while "," not in directions[0]:
                        directions[0] += directions.pop(1)
                    lastArguments = directions.pop(0).split(",")
                x = float(lastArguments[0].strip())
                y = float(lastArguments[1].strip())
                xyPoints[-1].append((x,y))

            if (command == "c"):
                (dx, dy) = (0.0, 0.0)
                while (not directions[0].isalpha()): 
                    while "," not in directions[0]:
                        directions[0] += directions.pop(1)
                    arguments = directions.pop(0).split(",")
                    dx += float(arguments[0].strip())
                    dy += float(arguments[1].strip())
                (x0,y0) = xyPoints[-1][-1]
                (x,y) = (x0+dx/2,y0+dy/2) # I am not sure why the 2 is necessary, but it makes it display properly :P
                xyPoints[-1].append((x,y))

        return xyPoints

    def draw(self, canvas, colorDict = {}):
        for ID in self.svgPaths:
            if ID not in colorDict.keys(): color = "white"
            else: color = colorDict[ID]
            for points in self.svgPaths[ID]:
                if (len(ID) <= 3):
                    canvas.create_polygon(*points, fill=color, outline="black", width=2)
                else: # NOT a state ID
                    color = "black"
                    canvas.create_line(*points, fill=color, width=2)


# import random
# svg = SVG('USA_Counties_with_FIPS_and_names.svg')
# root = Tk()
# # states = ['WA', 'DE', 'DC', 'WI', 'WV', 'HI', 'FL', 'WY', 'NH', 'NJ', 'NM', 'TX', 'LA', 'NC', 'ND', 'NE', 'TN', 'NY', 'PA', 'MT', 'RI', 'NV', 'VA', 'CO', 'AK', 'AL', 'AR', 'VT', 'GA', 'IN', 'IA', 'MA', 'AZ', 'CA', 'ID', 'CT', 'ME', 'MD', 'OH', 'UT', 'MO', 'MN', 'MI', 'KS', 'OK', 'MS', 'SC', 'KY', 'SD', 'OR', 'IL']
# # colorDict = {key:random.choice(["red","orange","yellow","green","blue","purple"]) for key in states}
# canvas = Canvas(root, width=svg.width, height=svg.height)
# canvas.pack()
# svg.draw(canvas)#, colorDict=colorDict)
# canvas.mainloop()

        