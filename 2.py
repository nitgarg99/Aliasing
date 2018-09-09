from PIL import Image, ImageDraw, ImageTk
from math import tan, radians
import tkinter as tk

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
    global im
    global updateIndex
    global n
    im = Image.new( 'L', (512, 512), 0xFF)
    drawLinePattern(im, n, updateIndex*3.6)
    tkimg = ImageTk.PhotoImage(im)
    label.config(image = tkimg)
    label.after(10, update_image)
    updateIndex += 1




        
im = Image.new( 'L', (512, 512), 0xFF)
print('Type number of lines:', sep=' ')
n = int(input())
drawLinePattern(im, n)
print('Type scale:', sep=' ')
scale = float(input())
im.show()
main = tk.Tk()
tkimg = ImageTk.PhotoImage(im)
label = tk.Label(main, image=tkimg)
updateIndex = 1
print ("Loaded")
label.pack()
main.after(1000, update_image)
main.mainloop()
