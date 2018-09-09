import time
import tkinter
from PIL import Image, ImageTk

class SimpleApp(object):
    def __init__(self, master, filename, **kwargs):
        self.master = master
        self.filename = filename
        self.canvas = tkinter.Canvas(master, width=500, height=500)
        self.canvas.pack()

        self.update = self.draw().__next__  # Using "next(self.draw())" doesn't work
        master.after(1, self.update)

    def draw(self):
        image = Image.open(self.filename)
        angle = 0
        while True:
            tkimage = ImageTk.PhotoImage(image.rotate(angle))
            canvas_obj = self.canvas.create_image(250, 250, image=tkimage)
            self.master.after_idle(self.update)
            yield
            self.canvas.delete(canvas_obj)
            angle += 1
            angle %= 360

root = tkinter.Tk()
app = SimpleApp(root, 'test.png')
root.mainloop()
