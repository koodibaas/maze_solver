from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("Test Title")
        self.canvas = Canvas(self.root)
        self.canvas.pack()
        self.running = False

    
    def redraw(self):
        self.root.update()
        self.root.update_idletasks()

    
    def wait_for_close(self):
        self.running = True
        while self.running == True:
            self.redraw()


    def close(self):
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)


def main():
    win = Window(800, 600)
    win.wait_for_close()

main()
    


