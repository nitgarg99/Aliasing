from PIL import Image, ImageDraw, ImageTk
from math import tan, radians
import tkinter as tk
import time
import sys

def drawLine(im, x, y):
    draw = ImageDraw.Draw(im)
    draw.line ([(im.size[0]/2, im.size[1]/2), (x, y)], 0, 1)
    del draw

def drawLinePattern(im, n, offset=0):
    sep_degrees = 360/n
    for i in range (n):
        degree = i*sep_degrees
        degree = (degree + offset) 
        #Translate degree into 0 - 360 domain
        multiplier = int(degree) // 360
        degree = degree - multiplier * 360 
        if degree < 45:
            slope = tan(radians(degree))
            y = slope * -im.size[0]/2
            y = y + im.size[1]/2
            y = round(y)
            #DEBUG: print('Drawing line to (', im.size[0], y, ')')
            drawLine(im, im.size[0], y)
        elif degree <= 135:
            slope = tan(radians(degree))
            x = (im.size[1]/2)/slope
            x = x + im.size[0]/2
            x = round(x)
            #DEBUG: print('Drawing line to (', x, 0, ')')
            drawLine(im, x, 0)
        elif degree < 225:
            slope = tan(radians(degree))
            y = slope * im.size[0]/2
            y = y + im.size[1]/2
            y = round(y)
            #DEBUG: print('Drawing line to (', 0, y, ')')
            drawLine(im, 0, y)
        elif degree <= 315:
            slope = tan(radians(degree))
            x = -(im.size[1]/2)/slope
            x = x + im.size[0]/2
            x = round(x)
            #DEBUG: print('Drawing line to (', x, im.size[1], ')')
            drawLine(im, x, im.size[1])
        elif degree < 360:
            slope = tan(radians(degree))
            y = slope * -im.size[0]/2
            y = y + im.size[1]/2
            y = round(y)
            #DEBUG: print('Drawing line to (', im.size[0], y, ')')
            drawLine(im, im.size[0], y)

#We will assume square sizes and that im size is 512
def resize (im, scale): 
    data = list(im.getdata())
    newLength = int(round(512 / scale))
    newDataSize = newLength ** 2
    newData = []
    for row in range (0, newLength):
        rowAdder = newLength * row
        for column in range (0, newLength):
            pixIndex = column + rowAdder
            sampleColumn = int(round(column*scale))
            sampleRow = int(round(row*scale))
            if sampleColumn > 511:
                sampleColumn = 511
            if sampleRow > 511:
                sampleRow = 511
            sampleIndex = sampleColumn + sampleRow*512
            pixColor = data[sampleIndex]
            newData.append(pixColor)

    scaledImage = Image.new('L', (newLength, newLength), 0xff)
    scaledImage.putdata(newData)
    return scaledImage

def update_image():
    global tkimg 
    global label
    global updateIndex
    global imArr

    if updateIndex < 39:
        updateIndex += 1
    else:
        updateIndex = 0

    startTime = int(round(time.time() * 1000))
    tkimg = ImageTk.PhotoImage(imArr[updateIndex])
    label.config(image = tkimg)
    while (int(round(time.time() * 1000)) < startTime + 15):
        nothing = 0
    label.after(10, update_image)


def capture_image():
    global tkimg2
    global label2
    global updateIndex2
    global imArr2

    if updateIndex2 < len(imArr2) - 1:
        updateIndex2 += 1
    else: 
        updateIndex2 = 0
    tkimg2 = ImageTk.PhotoImage(imArr2[updateIndex2])
    label2.config(image = tkimg2)
    label2.after(1000//int(fps), capture_image)
    

im = Image.new( 'L', (512, 512), 0xFF)
n = int(sys.argv[1])
drawLinePattern(im, n)
s = float(sys.argv[2])
fps = float(sys.argv[3])
main = tk.Tk()
tkimg = ImageTk.PhotoImage(im)
tkimg2 = ImageTk.PhotoImage(im)
label = tk.Label(main, image=tkimg)
label2 = tk.Label(main, image=tkimg2)

updateIndex = 0
multiplier = 360 * s / 40
imArr = []
while len(imArr) < 40:
    im = Image.new( 'L', (512, 512), 0xFF)
    drawLinePattern(im, n, len(imArr)*multiplier)
    imArr.append(im)

updateIndex2 = 0
multiplier2 = 360 * s / fps
imArr2 = []
while len(imArr2) < fps:
    im2 = Image.new( 'L', (512, 512), 0xFF)
    drawLinePattern(im2, n, len(imArr2)*multiplier2)
    imArr2.append(im2)
    

label.pack()
#label2.pack()
main.after(5, update_image)
#main.after(1, capture_image)
main.mainloop()
