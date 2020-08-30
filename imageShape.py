# Pontificia Universidad Javeriana. Departamento de Electrónica
# Author: Juan Henao, Estudiante de Ing. Electrónica.
# Procesamiento de Imagenes y visión
# 31/08/2020

# Importing library's
import numpy as np
import cv2
from random import randint
import math

# Creat class imageShape, this class generates and Identifies an image of a 45 degree rotated square
# a rectangle, an equilateral triangle, or a circle, all shapes are centered in the center
# of the Image
# User provides width and height of the image.
# # with this 2, geometric characteristics of the shapes are calculated
class imageShape:

    def __init__(self, width, height):  # Constructor
        self.width = np.uint16(width) # saves width of the image
        self.height = np.uint16(height) # saves height of the image
        self.GSflag = False # Turns True if a shape is generated
        self.shapeName = 'None' # Name of the shape generated

    def generateShape(self): # generate a shape method
        self.shape = np.zeros((self.width, self.height, 3), np.uint8) # Generate widthxheight black image
        self.GSflag = True # Turns True if a shape is generated
        random = randint(0,3) #Random int to choose one shape gen random Dom{ [0,3] }

        if random == 0: #Draw a Circle
            self.shapeName = 'Circle' # Name shape
            radio = np.int16(min(self.width, self.height) / 4) # calculates radius
            Cx = np.uint16(self.height / 2) # Calculates center point
            Cy = np.uint16(self.width / 2) # Calculates center point
            cv2.circle(self.shape, (Cx, Cy), radio, (255, 255, 0), -1) #draws circle in image

        elif random == 1: #Draw a Rectangle
            self.shapeName = 'Rectangle' # Name shape
            Cx = np.uint16(self.height / 2) # Calculates center point
            Cy = np.uint16(self.width / 2) # Calculates center point

            lado_h = np.int16(self.width / 2) # Calculates side of the rect
            lado_v = np.int16(self.height / 2) # Calculates side of the rect

            x1 = np.int16(Cx - (lado_v) / 2) # calculates top left corner points
            y1 = np.int16(Cy - (lado_h) / 2)

            x2 = np.int16(Cx + (lado_v) / 2) # calculates bottom right corner points
            y2 = np.int16(Cy + (lado_h) / 2)

            cv2.rectangle(self.shape, (x1, y1), (x2, y2), (255, 255, 0), -1) # Draw the rect

        elif random == 2: #Draw a square
            self.shapeName = 'Square'   # name shape
            Cx = np.uint16(self.height / 2) # find center points
            Cy = np.uint16(self.width / 2) #  find center points

            lado = min(self.width, self.height) / 2 # calculates side
            hip = np.int16(math.sqrt(2 * (lado * lado))) # for finding points from the center

            x1 = np.int16(Cx - hip / 2) # finds some points of the figure
            y1 = np.int16(Cy - hip / 2) # Square is centered and 45 degree rotated
            x2 = np.int16(Cx + hip / 2)

            cv2.line(self.shape, (Cx, y1), (x1, Cy), (255, 255, 0), 2) # Draws square side by side
            cv2.line(self.shape, (Cx, y1 + hip), (x1, Cy), (255, 255, 0), 2) # Draws square side by side
            cv2.line(self.shape, (Cx, y1 + hip), (x2, Cy), (255, 255, 0), 2) # Draws square side by side
            cv2.line(self.shape, (Cx, y1), (x2, Cy), (255, 255, 0), 2) # Draws square side by side

            cv2.floodFill(self.shape, None, (Cx, Cy), (255, 255, 0)) # fills with cyan

        elif random == 3: # Draw a triangle
            self.shapeName = 'Triangle' # name shape
            Cx = np.uint16(self.height / 2) # finds center point
            Cy = np.uint16(self.width / 2) #  finds center point

            lado = np.int16(min(self.width, self.height) / 2) # calculates triangle side
            a = np.int16(lado / 2) # for moving from center
            alt_h = np.int16(lado * (math.sqrt(3) / 2)) # for moving from center
            h = np.int16(alt_h / 2) # for moving from center

            cv2.line(self.shape, (Cx - a, Cy + h), (Cx + a, Cy + h), (255, 255, 0), 2) # draws triangle
            cv2.line(self.shape, (Cx - a, Cy + h), (Cx, Cy - h), (255, 255, 0), 2) # side by side
            cv2.line(self.shape, (Cx, Cy - h), (Cx + a, Cy + h), (255, 255, 0), 2)

            cv2.floodFill(self.shape, None, (Cx, Cy), (255, 255, 0)) # fills with cyan color

        else:
            print('Random Fail, check function') # if random function fails

    def showShape(self): # show generated shape method
        if self.GSflag == True: # if a shape has already been generated
            cv2.imshow('Showing Shape', self.shape) # show shape
            cv2.waitKey(5000) # wait for 5 seconds

        elif self.GSflag == False: # if shape has not been generated
            self.shape = np.zeros((self.width, self.height, 3), np.uint8)
            cv2.imshow('No shape Generated', self.shape) # show black image
            cv2.waitKey(5000) # wait 5 seconds

    def getShape(self): # get shape method
        return self.shape, self.shapeName # return shape image and name from self

    def whatShape(self, Image): # what shape method
        # Hallar contorno/ find contour of shape
        bw_Image = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY) # turn image to gray scale
        _, Image_mask = cv2.threshold(bw_Image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) # binarize using otsu
        contour, _ = cv2.findContours(Image_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) # find contour

        # Hallar minRect y minCirle que se adapten a la imagen
        # find boundin rectangle and circle for the image
        x, y, w, h = cv2.boundingRect(contour[0]) # find bounding rect
        # Hallar minCircle
        (r, t), radius = cv2.minEnclosingCircle(contour[0])# find bounding circle

        # Hallar area de contorno y de minRect & minCircle
        # claculate contour, and bounding areas
        Mcontour = cv2.moments(contour[0])
        Acountour = Mcontour['m00']
        Acircle = math.pi*radius*radius
        Arect  = w*h

        # compare the width of the bounding rect with the radius of bounding circle
        calc = (w * (math.sqrt(3)) / 3) / radius

        #Discriminar figuras
        if 0.9 < Acircle/Acountour < 1.1: # compare areas to find out what figure is
            self.IDshape = "Circle"
            return self.IDshape # return figure

        elif  0.9 < Arect/Acountour < 1.1: # compare areas to find out what figure is
            self.IDshape = "Rectangle"
            return self.IDshape # return figure

        elif 0.9 < calc < 1.1: # compare width and radius to find out the figure
            self.IDshape = 'Triangle'
            return self.IDshape # return figure

        else:
            self.IDshape = 'Square' # if no other figure was Identified it must be a square
            return self.IDshape # return figure



