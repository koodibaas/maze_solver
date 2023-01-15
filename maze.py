from tkinter import Tk, BOTH, Canvas
import random, time

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
    def __init__(self, x1, y1, x2, y2, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = win
        self.visited = False


    def draw(self, fill_color):
        if self._win is not None:
            if self.has_left_wall:
                self._win.canvas.create_line(self._x1, self._y1, self._x1, self._y2, fill=fill_color, width=2)
            else:
                self._win.canvas.create_line(self._x1, self._y1, self._x1, self._y2, fill="white", width=2)
            if self.has_right_wall:
                self._win.canvas.create_line(self._x2, self._y1, self._x2, self._y2, fill=fill_color, width=2)
            else:
                self._win.canvas.create_line(self._x2, self._y1, self._x2, self._y2, fill="white", width=2)
            if self.has_top_wall:
                self._win.canvas.create_line(self._x1, self._y1, self._x2, self._y1, fill=fill_color, width=2)
            else:
                self._win.canvas.create_line(self._x1, self._y1, self._x2, self._y1, fill="white", width=2)
            if self.has_bottom_wall:
                self._win.canvas.create_line(self._x1, self._y2, self._x2, self._y2, fill=fill_color, width=2)
            else:
                self._win.canvas.create_line(self._x1, self._y2, self._x2, self._y2, fill="white", width=2)
            self._win.canvas.pack()

    
    def draw_move(self, to_cell, undo=False):
        if undo:
            color = "gray"
        else:
            color = "red"

        __x1 = (self._x2 + self._x1) / 2
        __y1 = (self._y2 + self._y1) / 2
        __x2 = (to_cell._x2 + to_cell._x1) / 2
        __y2 = (to_cell._y2 + to_cell._y1) / 2

        if self._win is not None:
            self._win.canvas.create_line(__x1, __y1, __x2, __y2, fill=color, width=2)
            self._win.canvas.pack()    
        

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        self._create_cells()
        self._break_entrance_and_exit()
        '''
        if seed:
            self.seed = random.seed(seed)
        else:
            self.seed = random.seed(0)
        '''
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
   

    def _create_cells(self):
        self._cells = []
        
        for i in range(0, int(self.num_cols)):
            col_list = []
            for j in range(0, int(self.num_rows)):
                col_list.append(Cell(0, 0, 0, 0, self._win))
            self._cells.append(col_list)

        for i in range(0, int(self.num_cols)):
            for j in range(0, int(self.num_rows)):
                self._draw_cell(i, j)


    def _draw_cell(self, i, j):
        x1 = (i * self.cell_size_x) + self.x1
        y1 = (j * self.cell_size_y) + self.y1
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y

        cell = self._cells[i][j]
        cell._x1 = x1
        cell._x2 = x2
        cell._y1 = y1
        cell._y2 = y2
        cell.draw("blue")
        self._animate()


    def _animate(self):
        if self._win is not None:
            time.sleep(0.05)
            self._win.redraw()


    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        stop = False
        while stop == False:
            cells_to_visit = []
            _i, _j = i, j - 1
            if _j >= 0:
                if self._cells[_i][_j].visited == False:
                        cells_to_visit.append([_i, _j, "up"])
            _i, _j = i + 1, j
            if _i <= self.num_cols - 1:
                if self._cells[_i][_j].visited == False:
                    cells_to_visit.append([_i, _j, "right"])
            _i, _j = i, j + 1
            if _j <= self.num_rows - 1:
                if self._cells[_i][_j].visited == False:
                    cells_to_visit.append([_i, _j, "down"])
            _i, _j = i - 1, j
            if _i >= 0:
                if self._cells[_i][_j].visited == False:
                    cells_to_visit.append([_i, _j, "left"])

            if len(cells_to_visit) == 0:
                self._draw_cell(i, j)
                stop = True
            else:
                next_cell = cells_to_visit[random.randint(0, len(cells_to_visit) - 1)]
                _i, _j, direction = next_cell[0], next_cell[1], next_cell[2]
                if direction == "up":
                    self._cells[i][j].has_top_wall = False
                    self._cells[_i][_j].has_bottom_wall = False
                if direction == "right":
                    self._cells[i][j].has_right_wall = False
                    self._cells[_i][_j].has_left_wall = False
                if direction == "down":
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[_i][_j].has_top_wall = False
                if direction == "left":
                    self._cells[i][j].has_left_wall = False
                    self._cells[_i][_j].has_right_wall = False
                self._break_walls_r(_i, _j)


    def _reset_cells_visited(self):
        for i in range(0, int(self.num_cols)):
            for j in range(0, int(self.num_rows)):
                self._cells[i][j].visited = False


#def run_maze():
if __name__ == "__main__":
    win = Window(800, 600)
    '''
    point1 = Point(2, 2)
    point2 = Point(100, 100)
    
    line = Line(point1.x, point1.y, point2.x, point2.y)
    win.draw_line(line, "red")
    
    cell1 = Cell(point1.x, point1.y, point2.x, point2.y, win)
    cell1.draw("green")
    
    cell2 = Cell(200, 100, 798, 598, win)
    cell2.has_right_wall = False
    cell2.draw("red")
    
    cell1.draw_move(cell2)
    '''
    Maze(4, 3, 6, 8, 99, 99, win)
    
    win.wait_for_close()

#run_maze()
    


