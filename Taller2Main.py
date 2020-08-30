# Pontificia Universidad Javeriana. Departamento de Electrónica
# Author: Juan Henao, Estudiante de Ing. Electrónica.
# Procesamiento de Imagenes y visión
# 31/08/2020

# Importing librarys
import numpy as np
import cv2
from random import randint
import math
from imageShape import *

if __name__ == "__main__": # Execute main function in code
    while(1):
        # ask user for width anf lenght
       width = int(input('Hi user, please enter the width in pixels of the Image you want to create (Example 500) '))
       height = int(input('Now please enter a height '))

       #  Generate image, show it to user and get the classification tag and image tag to compare them
       GenImg = imageShape(height, width)
       GenImg.generateShape()
       GenImg.showShape()
       GenShape, ShapeName = GenImg.getShape()
       shapeID = GenImg.whatShape(GenShape)
        # if classification tag and image tag are
       if shapeID == ShapeName: # equal
           event = 'Success' # classification success
       else: # unequal
           event = 'Fail' # classification fail

        # show user the info
       print('Shape generated: ', ShapeName)
       print('Shape Classified: ', shapeID)
       print('Classification = ', event)
        # ask user to try again
       retry = int(input('Try again ? 1 for yes other for no '))
       if retry != 1:
            break # if not, end program


