from tkinter import Tk, BOTH, Canvas
import time

class Window():
    def __init__(self, width, height):
        self.root = Tk()
        self.root.geometry(f"{width}x{height}")
        self.root.title("Test Title")
        self.canvas = Canvas(self.root, width=width, height=height, bg="white")
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


    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)


    def draw_cell(self, cell, fill_color):
        cell.draw(self.canvas, fill_color)


    def draw_move(self, cell, to_cell, undo=False):
        cell.draw_move(self.canvas, to_cell, undo)


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


    def draw(self, canvas, fill_color):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=fill_color, width=2)
        canvas.pack()


class Cell():
    def __init__(self, x1, y1, x2, y2, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = win


    def draw(self, canvas, fill_color):
        if self.has_left_wall:
            canvas.create_line(self._x1, self._y1, self._x1, self._y2, fill=fill_color, width=2)
            #canvas.pack()
        if self.has_right_wall:
            canvas.create_line(self._x2, self._y1, self._x2, self._y2, fill=fill_color, width=2)
            #canvas.pack()
        if self.has_top_wall:
            canvas.create_line(self._x1, self._y1, self._x2, self._y1, fill=fill_color, width=2)
            #canvas.pack()
        if self.has_bottom_wall:
            canvas.create_line(self._x1, self._y2, self._x2, self._y2, fill=fill_color, width=2)
        canvas.pack()

    
    def draw_move(self, canvas, to_cell, undo=False):
        if undo:
            color = "gray"
        else:
            color = "red"

        __x1 = (self._x2 + self._x1) / 2
        __y1 = (self._y2 + self._y1) / 2
        __x2 = (to_cell._x2 + to_cell._x1) / 2
        __y2 = (to_cell._y2 + to_cell._y1) / 2

        canvas.create_line(__x1, __y1, __x2, __y2, fill=color, width=2)
        canvas.pack()    
        

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._create_cells()

    
    def _create_cells(self):
        self._cell = []
        col_offset = self.cell_size_y / 2
        row_offset = self.cell_size_x / 2
        
        for i in range(1, int(self.num_cols + 1)):
            col_list = []
            for j in range(1, int(self.num_rows + 1)):
                col_list.append([
                    (i * row_offset) + self.x1, 
                    (j * col_offset) + self.y1
                    ])
            self._cell.append(col_list)
                    
        for col in self._cell:
            for cell in col:
                self._draw_cell(cell[0], cell[1])

    def _draw_cell(self, i, j):
        x1 = i - (self.cell_size_x / 2)
        x2 = i + (self.cell_size_x / 2)
        y1 = j - (self.cell_size_y / 2)
        y2 = j + (self.cell_size_y / 2)

        cell = Cell(x1, y1, x2, y2, True)
        self.win.draw_cell(cell, "blue")
        self._animate()


    def _animate(self):
        time.sleep(0.05)
        self.win.redraw()

def main():
    win = Window(800, 600)
    
    #point1 = Point(2, 2)
    #point2 = Point(100, 100)
    #line = Line(point1.x, point1.y, point2.x, point2.y)
    #win.draw_line(line, "red")
    
    #cell1 = Cell(point1.x, point1.y, point2.x, point2.y, True)
    #win.draw_cell(cell1, "green")
    
    #cell2 = Cell(200, 100, 798, 598, True)
    #cell2.has_top_wall = False
    #win.draw_cell(cell2, "blue")
    
    #win.draw_move(cell1, cell2, True)
    
    Maze(100, 100, 10, 10, 10, 10, win)

    win.wait_for_close()

main()
    


