'''
To-Do:
1. Save [DONE]
2. Undo
3. Shapes
'''

import pygame

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
canvasHeight = 650
toolBoxHeight = 40
pointsX = canvasLength-105
pointSize = 3
pointSpace = 10
colorWidth = 50
colorHeight = 50
colorTrayY = canvasHeight+toolBoxHeight
drawing = False
last_pos = None
w = 10

screen = pygame.display.set_mode((screenLength, screenHeight))
pygame.display.set_caption("PyPaint")
font = pygame.font.Font("High Jersey.ttf", 15)
pencil = pygame.image.load("pencil.png")
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
    main()

def fileSave():
    val = 1
    font = pygame.font.Font("High Jersey.ttf", 20)
    dialogRect = pygame.Rect(int(screenLength/2-200), int(screenHeight/2-150), 400, 200)
    saveRect = pygame.Rect(dialogRect.x+dialogRect.w-50, dialogRect.y+dialogRect.h-40, 40, 25)
    saveText = font.render("save", True, WHITE)

    while val:
        dialogBox = pygame.draw.rect(screen, GRAY, dialogRect)

        cursor = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if dialogBox.collidepoint(cursor):
            val = 0

        pygame.display.update()

    screen.fill(defaultColor)
    main()


def draw(event):
    global drawing, last_pos

    if event.type == pygame.MOUSEMOTION:
        if (drawing):
            mouse_position = pygame.mouse.get_pos()
            if last_pos is not None:
                pygame.draw.line(screen, color, last_pos, mouse_position, pointSize)
            last_pos = mouse_position
    elif event.type == pygame.MOUSEBUTTONUP:
        mouse_position = (0, 0)
        drawing = False
        last_pos = None
    elif event.type == pygame.MOUSEBUTTONDOWN:
        drawing = True

def main():
    global game, pointSize, color

    while game:
        cursor = pygame.mouse.get_pos()
        pygame.draw.rect(screen, (240, 221, 215), (pointsX, 0, 200, toolBoxHeight))
        trash.display()
        if trash.getRect().collidepoint(cursor):
            trash.tipToolText()

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
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    screen.fill(defaultColor)
                elif event.key == pygame.K_s:
                    # fileSave()
                    fileName = input("Please enter the file name(along with the type): ")
                    pygame.image.save(canvasSurface, fileName)
                    print("Image successfully saved")
            draw(event)

        # pix = pygame.PixelArray(screen)
        if pygame.mouse.get_pressed()[0]:

            #Checking for collision with clear button
            if trash.getRect().collidepoint(cursor):
                screen.fill(defaultColor)

            #Checking for collision with the point size tray
            for iPoint in listOfPoints:
                if iPoint.getRect().collidepoint(cursor):
                    pointSize = iPoint.getRadius()

            for x in range(cursor[0]-pointSize, cursor[0]+pointSize):
                for y in range(cursor[1]-pointSize, cursor[1]+pointSize):
                    if y < toolBoxHeight+1:
                        y = toolBoxHeight+1
                    if x > canvasLength:
                        x = canvasLength
                    if x < 0:
                        x = 0
                    if y > canvasHeight:
                        y = canvasHeight

                    #Checking for collision with the color tray
                    for mColor in listOfColors:
                        if(mColor.getRect().collidepoint(cursor)):
                            color = mColor.getColor()

                    #Setting the color to be drawn
                    for iPoint in listOfPoints:
                        iPoint.setcolor(color)

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