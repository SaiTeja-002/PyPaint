'''
To-Do:
1. Save [DONE]
2. Undo
3. Shapes
'''

import pygame
import os
import os.path

clock = pygame.time.Clock
pygame.init()

#Variables
WHITE = (255, 255, 255) #
BLACK = (0, 0, 0) #
RED = (255, 0, 0) #
GREEN = (0, 255, 0) #
DARKGREEN = (0,100,0) #
SPRINGGREEN = (0,250,154) #
BLUE = (0, 0, 255) #
DARKBLUE = (0,0,139) #
VIOLET = (138,43,226) #
INDIGO = (75,0,130) #
CYAN = (0,255,255) #
TURQUOISE = (64,224,208) #
YELLOW = (255, 255, 0) #
GRAY = (128, 128, 128) #
MAROON = (128, 0, 0) #
ORANGERED = (255,69,0) #
DARKORANGE = (255,140,0) #
GOLD = (184,134,11) #
OLIVE = (128,128,0) #
PURPLE = (128,0,128) #
MAGENTA = (255,0,255) #
DEEPPINK = (255,20,147) #
PINK = (255,192,203) #
CHOCOLATE = (210,105,30) #
BROWN = (139,69,19) #

game = True
color = BLACK
defaultColor = BLACK
screenLength = 1000
screenHeight = 800
canvasLength = 1000
canvasHeight = screenHeight-150
toolBoxHeight = 40
pointsX = canvasLength-105
pointSize = 3
pointSpace = 10
colorWidth = 50
colorHeight = 50
colorTrayY = canvasHeight+toolBoxHeight
drawing = False
last_pos = None
fileName = ""

screen = pygame.display.set_mode((screenLength, screenHeight))
pygame.display.set_caption("PyPaint")
font = pygame.font.Font("High Jersey.ttf", 15)
pencil = pygame.image.load("pencil.png")
undo = pygame.image.load("undo.png")
redo = pygame.image.load("redo.png")
undoRect = undo.get_rect()
redoRect = redo.get_rect()
screen.fill(defaultColor)
canvasRect = pygame.Rect(0, toolBoxHeight, canvasLength, canvasHeight)
canvasSurface = screen.subsurface(canvasRect)

class Color:
    def __init__(self, xloc, yloc, color, name):
        self.mColor = color
        self.xpos = xloc
        self.ypos = yloc
        self.colorName = name

    def displayColor(self):     #Displays the color onto the screen
        self.rect = pygame.draw.rect(screen, self.mColor, (self.xpos, self.ypos, colorWidth, colorHeight))

    def getX(self):     #Returns the xpos of the color
        return self.xpos

    def getColorName(self):     #Returns the name of the color
        return self.colorName.lower()

    def getRect(self):      #Returns the rect of this color object to check for collisions
        return self.rect

    def getColor(self):     #Returns the color tuple
        return self.mColor

    def tipToolText(self):
        if self.mColor == WHITE:
            self.tipText = font.render("white", True, BLACK, self.mColor)
        else:
            self.tipText = font.render(self.colorName, True, WHITE, self.mColor)
        self.tipTextRect = self.tipText.get_rect()
        self.tipTextRect.center = (self.xpos+colorWidth/2, self.ypos+colorHeight/2)
        screen.blit(self.tipText, self.tipTextRect)

class PointSizes:
    def __init__(self, xloc, yloc, rad):
        self.radius = rad
        self.mColor = color
        self.xpos = xloc
        self.ypos = yloc

    def displayPoint(self):     #Displays the point size onto the screen
        self.rect = pygame.draw.circle(screen, self.mColor, (self.xpos, self.ypos), self.radius)

    def setcolor(self, c):      #Sets the color of the point
        self.mColor = c

    def getRect(self):      #Returns the rect of the point to check for collision
        return self.rect

    def getX(self):     #Returns the xposition of the centre of the circle
        return self.xpos

    def getRadius(self):    #Returns the radius of the point
        return self.radius

class Trasher:
    def __init__(self, fileName, xloc, yloc):
        self.path = fileName
        self.xpos = xloc
        self.ypos = yloc
        self.trash = pygame.image.load(self.path)
        self.trashRect = self.trash.get_rect()
        self.trashRect.center = (self.xpos+16, self.ypos+16)

    def display(self):
        screen.blit(self.trash, self.trashRect)

    def tipToolText(self):
        self.tipText = font.render("Clear", True, BLACK, RED)
        screen.blit(self.tipText, self.trashRect)

    def getRect(self):
        return self.trashRect

class Button:
    def __init__(self, t, xloc, yloc, tcolor, bcolor, fontSize, width, height):
        # self.text = t
        self.xpos = xloc
        self.ypos = yloc
        self.textColor = tcolor
        self.buttonColor = bcolor
        self.size = fontSize
        self.width = width
        self.height = height
        self.font = pygame.font.Font("High Jersey.ttf", self.size)
        self.text = self.font.render(t, True, self.textColor)
        self.textRect2 = pygame.Rect((self.xpos+10, self.ypos, width, height))

    def display(self):
        self.textRect = pygame.draw.rect(screen, self.buttonColor, (self.xpos, self.ypos, self.width, self.height))
        screen.blit(self.text, self.textRect2)

    def getRect(self):
        return self.textRect

class InputBox:

    def __init__(self, x, y, w, h, text=""):
        self.COLOR_INACTIVE = BLACK
        self.COLOR_ACTIVE = WHITE
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_ACTIVE
        self.text = text
        self.font = pygame.font.Font("simpletix.otf", 20)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render(self.text, True, self.color)

    def update(self):
        # Resizing the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def getText(self):
        return self.text


#Creating color objects
whiteColor = Color(0, colorTrayY, WHITE, "white")
blackColor = Color(whiteColor.getX()+colorWidth, colorTrayY, BLACK, "black")
grayColor = Color(blackColor.getX()+colorWidth, colorTrayY, GRAY, "gray")
redColor = Color(grayColor.getX()+colorWidth, colorTrayY, RED, "red")
maroonColor = Color(redColor.getX()+colorWidth, colorTrayY, MAROON, "marron")
magentaColor = Color(maroonColor.getX()+colorWidth, colorTrayY, MAGENTA, "magenta")
oliveColor = Color(magentaColor.getX()+colorWidth, colorTrayY, OLIVE, "olive")
greenColor = Color(oliveColor.getX()+colorWidth, colorTrayY, GREEN, "green")
darkGreenColor = Color(greenColor.getX()+colorWidth, colorTrayY, DARKGREEN, "dark green")
springGreenColor = Color(darkGreenColor.getX()+colorWidth, colorTrayY, SPRINGGREEN, "spring green")
blueColor = Color(springGreenColor.getX()+colorWidth, colorTrayY, BLUE, "blue")
darkBlueColor = Color(blueColor.getX()+colorWidth, colorTrayY, DARKBLUE, "dark blue")
cyanColor = Color(darkBlueColor.getX()+colorWidth, colorTrayY, CYAN, "cyan")
turquoiseColor = Color(cyanColor.getX()+colorWidth, colorTrayY, TURQUOISE, "turquoise")
violetColor = Color(turquoiseColor.getX()+colorWidth, colorTrayY, VIOLET, "violet")
indigoColor = Color(violetColor.getX()+colorWidth, colorTrayY, INDIGO, "indigo")
yellowColor = Color(indigoColor.getX()+colorWidth, colorTrayY, YELLOW, "yellow")
orangeRedColor = Color(yellowColor.getX()+colorWidth, colorTrayY, ORANGERED, "orange red")
darkOrangeColor = Color(orangeRedColor.getX()+colorWidth, colorTrayY, DARKORANGE, "dark orange")
goldColor = Color(darkOrangeColor.getX()+colorWidth, colorTrayY, GOLD, "gold")
chocolateColor = Color(0, colorTrayY+50, CHOCOLATE, "chocolate")
brownColor = Color(chocolateColor.getX()+colorWidth, colorTrayY+50, BROWN, "brown")
pinkColor = Color(brownColor.getX()+colorWidth, colorTrayY+50, PINK, "pink")
deepPinkColor = Color(pinkColor.getX()+colorWidth, colorTrayY+50, DEEPPINK, "deep pink")
purpleColor = Color(deepPinkColor.getX()+colorWidth, colorTrayY+50, PURPLE, "purple")


listOfColors = [whiteColor, blackColor, redColor, greenColor, blueColor, yellowColor, maroonColor, magentaColor,
                darkGreenColor, springGreenColor, darkBlueColor, cyanColor, violetColor, indigoColor, turquoiseColor,
                grayColor, oliveColor, orangeRedColor, darkOrangeColor, goldColor, chocolateColor, brownColor,
                pinkColor, deepPinkColor, purpleColor]

#Creating pointsize objects
pt3 = PointSizes(canvasLength-100, 20, 3)
pt5 = PointSizes(pt3.getX()+pt3.getRadius()+pointSpace+5, 20, 5)
pt7 = PointSizes(pt5.getX()+pt5.getRadius()+pointSpace+7, 20, 7)
pt9 = PointSizes(pt7.getX()+pt7.getRadius()+pointSpace+9, 20, 9)

listOfPoints = [pt3, pt5, pt7, pt9]

trash = Trasher("trash.png", pointsX-50, 5)

def launch():
    global canvasLength, defaultColor

    try:
        os.mkdir("Gallery")
    except OSError:
        pass
        # print("Creation of the directory failed")
    else:
        pass
        # print("Successfully created the directory")

    val = 1
    font = pygame.font.Font("High Jersey.ttf", 60)

    text1 = font.render("Select the ", True, BLACK)
    text2 = font.render("Canvas Color", True, WHITE)

    text1Rect = text1.get_rect()
    text2Rect = text2.get_rect()

    text1Rect.center = (400, 100)
    text2Rect.center = (635, 100)

    while val:
        lightMode = pygame.draw.rect(screen, WHITE, (0, 0, 500, 800))
        darkMode = pygame.draw.rect(screen, BLACK, (500, 0, 500, 800))

        screen.blit(text1, text1Rect)
        screen.blit(text2, text2Rect)
        cursor = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if lightMode.collidepoint(cursor):
                    val = 0
                    defaultColor = WHITE
                elif darkMode.collidepoint(cursor):
                    val = 0
                    defaultColor = BLACK

        pygame.display.update()

    screen.fill(defaultColor)
    pygame.image.save(screen, "clearScreen.png")
    pygame.image.save(screen, "prevImage.png")
    pygame.image.save(screen, "curImage.png")
    main()


def fileSave():
    global fileName

    val = 1
    dialogRect = pygame.Rect(int(screenLength/2-200), int(screenHeight/2-150), 400, 200)
    font = pygame.font.Font("simpletix.otf", 20)
    text = font.render("choose a name to save your master-piece", True, WHITE)
    textRect = text.get_rect()
    textRect.x = dialogRect.x+10
    textRect.y = dialogRect.y+50
    saveButton = Button("save", dialogRect.x+dialogRect.w/2-180, dialogRect.y+dialogRect.h-40, WHITE, GREEN, 25, 50, 30)
    cancelButton = Button("cancel", dialogRect.x+dialogRect.w/2+80, dialogRect.y+dialogRect.h-40, WHITE, GRAY, 25, 60, 30)
    textBox = InputBox(dialogRect.x+10, dialogRect.y+dialogRect.h/2-10, dialogRect.w-10, 20)

    while val:
        dialogBox = pygame.draw.rect(screen, GRAY, dialogRect)
        saveButton.display()
        cancelButton.display()
        screen.blit(text, textRect)

        cursor = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove("Gallery/deleteFile.png")
                os.remove("clearScreen.png")
                os.remove("prevImage.png")
                os.remove("curImage.png")
                os.remove("redoImage.png")
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if saveButton.getRect().collidepoint(cursor):
                    fileName = textBox.getText()
                    path = "Gallery/"+fileName
                    os.renames("Gallery/deleteFile.png", path)
                    val = 0
                    fileName = ""

                elif cancelButton.getRect().collidepoint(cursor):
                    fun("redo")
                    fileName = ""
                    os.remove("Gallery/deleteFile.png")
                    val = 0

            textBox.handle_event(event)

        textBox.update()
        textBox.draw(screen)
        pygame.display.update()

    screen.fill(defaultColor)
    main()


def draw(event):
    global drawing, last_pos
    cursor = pygame.mouse.get_pos()

    if event.type == pygame.MOUSEMOTION:
        if drawing and cursor[0] in range(screenLength) and cursor[1] in range(toolBoxHeight+1, colorTrayY-2):
            cursor = pygame.mouse.get_pos()
            if last_pos is not None:
                pygame.draw.line(screen, color, last_pos, cursor, pointSize)
            last_pos = cursor
    elif event.type == pygame.MOUSEBUTTONUP:
        cursor = (0, 0)
        drawing = False
        last_pos = None
    elif event.type == pygame.MOUSEBUTTONDOWN:
        drawing = True


def fun(type):
    if type == "clear":
        clearScreen = pygame.image.load("clearScreen.png")
        screen.blit(clearScreen, (0, 0, screenLength, screenHeight))

    elif type == "undo":
        prevImage = pygame.image.load("prevImage.png")
        screen.blit(prevImage, (0, 0, screenLength, screenHeight))

    elif type == "redo":
        print("redoing")
        redoImage = pygame.image.load("redoImage.png")
        screen.blit(redoImage, (0, 0, screenLength, screenHeight))


def main():

    global game, pointSize, color, fileName
    redoRect.center = (pointsX-50-trash.getRect().w-10, 26)
    undoRect.center = (redoRect.x-50, 26)
    val = 1

    while game:
        # if os.path.isfile("Image.png"):
        #     print("hello")
        # pygame.image.save(screen, "curImage.png")
        # screen.fill(defaultColor)
        # pygame.mouse.set_visible(False)
        # curImage = pygame.image.load("curImage.png")
        # screen.blit(curImage, (0, 0, screenLength, screenHeight))

        cursor = pygame.mouse.get_pos()
        x = cursor[0]
        y = cursor[1]

        pygame.draw.rect(screen, GRAY, (0, 0, screenLength, toolBoxHeight))
        # screen.blit(redo, redoRect)
        # screen.blit(undo, undoRect)
        pygame.draw.rect(screen, (240, 221, 215), (pointsX, 0, 200, toolBoxHeight))
        trash.display()

        if trash.getRect().collidepoint(cursor):
            trash.tipToolText()

        # if y < toolBoxHeight + 1:
        #     print("hello")
        #     y = toolBoxHeight + 1
        if x > canvasLength:
            x = canvasLength
        if x < 0:
            x = 0
        if y > canvasHeight:
            y = canvasHeight

        #Displaying the color tray
        for iColor in listOfColors:
            iColor.displayColor()

        for iColor in listOfColors:
            if iColor.getRect().collidepoint(cursor):
                iColor.tipToolText()

        #Displaying the point size tray
        for iPoint in listOfPoints:
            iPoint.displayPoint()

        #Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove("clearScreen.png")
                os.remove("prevImage.png")
                os.remove("curImage.png")
                os.remove("redoImage.png")
                game = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    fun("clear")

                if event.key == pygame.K_u:
                    fun("undo")

                if event.key == pygame.K_r:
                    fun("redo")

                if event.key == pygame.K_s:
                    pygame.image.save(canvasSurface, "Gallery/deleteFile.png")
                    fileSave()
                    # if fileName:
                    #     print("deleting the file")
                    #     os.remove("deleteFile.png")
                    # else:
                    #     print("Renaming the file")
                    #     os.renames("deleteFile.png", fileName)
                    fileName = ""

            if event.type == pygame.MOUSEBUTTONDOWN:
                if val == 1 and cursor[1] in range(toolBoxHeight+1, colorTrayY-2):
                    pygame.image.save(screen, "prevImage.png")

                val = 0
                # Checking for collision with clear button
                if trash.getRect().collidepoint(cursor):
                    fun("clear")

                # if undoRect.collidepoint(cursor):
                #     print("Undo rect")
                #     fun("undo")
                #
                # if redoRect.collidepoint(cursor):
                #     print("Redo rect")
                #     fun("redo")

                # Checking for collision with the point size tray
                for iPoint in listOfPoints:
                    if iPoint.getRect().collidepoint(cursor):
                        pointSize = iPoint.getRadius()

                # cursor = pygame.mouse.get_pos()
                # x = cursor[0]
                # y = cursor[1]
                for x in range(cursor[0] - pointSize, cursor[0] + pointSize):
                    for y in range(cursor[1] - pointSize, cursor[1] + pointSize):
                        # print(x, y)

                        # if y < toolBoxHeight + 1:
                        #     # print("hello")
                        #     y = toolBoxHeight + 1
                        if x > canvasLength:
                            x = canvasLength
                        if x < 0:
                            x = 0
                        if y > canvasHeight:
                            y = canvasHeight

                # Checking for collision with the color tray
                for mColor in listOfColors:
                    if (mColor.getRect().collidepoint(cursor)):
                        color = mColor.getColor()

                # Setting the color to be drawn
                for iPoint in listOfPoints:
                    iPoint.setcolor(color)

            if cursor[0] in range(screenLength) and cursor[1] in range(toolBoxHeight+1, colorTrayY-2):
                draw(event)

            if event.type == pygame.MOUSEBUTTONUP:
                val = 1
                pygame.image.save(screen, "redoImage.png")

        # pix = pygame.PixelArray(screen)

                    #Drawing the appropriate color
                    # pix = pygame.PixelArray(screen)
                    # if x in range(canvasLength) and y in range(canvasHeight):
                    #     pix = pygame.PixelArray(screen)
                    #     pix[x][y] = color
                    #     del pix

        # del pix
        pygame.display.update()

launch()
pygame.quit()
exit()