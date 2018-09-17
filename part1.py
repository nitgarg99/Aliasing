from PIL import Image, ImageDraw
from math import tan, radians
import sys

def drawLine(im, x, y):
    draw = ImageDraw.Draw(im)
    draw.line ([(im.size[0]/2, im.size[1]/2), (x, y)], 0, 1)
    del draw

def drawLinePattern(im, n):
    sep_degrees = 360/n
    for i in range (n):
        degree = i*sep_degrees
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
            #DEBUG: print('Drawing line to (', x, im.size[1], ')')
            drawLine(im, x, im.size[1])
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
            #DEBUG: print('Drawing line to (', x, 0, ')')
            drawLine(im, x, 0)
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

#We will filter by averaging the 9 pixels, the one we are looking at + 8 adjacent to it.
def filter (im):
    data = list(im.getdata())
    filteredData = []
    for row in range (0, 512):
        for column in range (0, 512):
            total = 0
            count = 0
            #Average adjacent pixels in left column
            if column-1 >= 0:
                if row-1 >= 0:
                    total += data[(column-1) + ((row-1)*512)]
                    count += 1
                if row+1 < 512:
                    total += data[(column-1) + ((row+1)*512)]
                    count += 1
                total += data[(column-1) + (row*512)]
                count += 1
            #Now middle column
            if row-1 >= 0:
                total += data[(column) + ((row-1)*512)]
                count += 1
            if row+1 < 512:
                total += data[(column) + ((row+1)*512)]
                count +=1
            total += data[(column) + (row*512)]
            count +=1
            #Now right column
            if column+1 < 512:
                if row-1 >= 0:
                    total += data[(column+1) + ((row-1)*512)]
                    count += 1
                if row+1 < 512:
                    total += data[(column+1) + ((row+1)*512)]
                    count +=1
                total += data[(column+1) + (row*512)]
                count += 1
        
            #Calculate average
            average = total/count
            filteredData.append(average)
    return filteredData

#Get user input        
n = int(sys.argv[1])
scale = float(sys.argv[2])
aliasing = int(sys.argv[3])

#Do Image things
im = Image.new( 'L', (512, 512), 0xFF)
drawLinePattern(im, n)
im.show()
if aliasing:
    filteredData = filter(im)
    im.putdata(filteredData)

im2 = resize(im, scale)
im2.show()
