from Tkinter import *
import math, Tkinter
import detect

def poly_oval(x0,y0, x1,y1, steps=100, rotation=0):
    """return an oval as coordinates suitable for create_polygon"""

    # x0,y0,x1,y1 are as create_oval

    # rotation is in degrees anti-clockwise, convert to radians
    rotation = rotation * math.pi / 180.0

    # major and minor axes
    a = (x1 - x0) / 2.0
    b = (y1 - y0) / 2.0

    # center
    xc = x0 + a
    yc = y0 + b

    point_list = []

    # create the oval as a list of points
    for i in range(steps):

        # Calculate the angle for this step
        # 360 degrees == 2 pi radians
        theta = (math.pi * 2) * (float(i) / steps)

        x1 = a * math.cos(theta)
        y1 = b * math.sin(theta)

        # rotate x, y
        x = (x1 * math.cos(rotation)) + (y1 * math.sin(rotation))
        y = (y1 * math.cos(rotation)) - (x1 * math.sin(rotation))

        point_list.append(round(x + xc))
        point_list.append(round(y + yc))

    return point_list


class Painter:
    in_line_space = 10
    line_space = 20
    note_height_map = {
        0: (0, False),
        1: (0, True ),
        2: (1, False),
        3: (1, True ),
        4: (2, False),
        5: (3, False),
        6: (3, True ),
        7: (4, False),
        8: (4, True ),
        9: (5, False),
       10: (5, True ),
       11: (6, False),
       12: (7, False),
    }
    def _getNoteInfo(self, level):
        h = level / 12 * 7
        index = level % 12
        h += self.note_height_map[index][0]
        return (h, self.note_height_map[index][1])
        
    def __init__(self, tk, w, h):
        self.canvas = Tkinter.Canvas(tk, width=w, height=h)
        self.canvas.pack()
        self.width = w
        self.height = h
        self.nextLine()
    def nextLine(self):
        if hasattr(self, 'y'):
            self.y += self.in_line_space*4 + self.line_space
        else:
            self.y = 50
        self.x = 50
    def drawLines(self, w):
        for i in range(5):
            n = self.y + self.in_line_space * i
            self.canvas.create_line(self.x, n, self.x + w, n, width=1, fill='#111111')
    def drawNote(self, note_level):
        note_width = 14
        note_height = 10
        note_space_x = 8
        has_appendix = True
        appendix_offset_x = -5
        appendix_width = 10
        x_inc = note_width + note_space_x
        note_info = self._getNoteInfo(int(note_level))
        if note_info[1]:
            x_inc += appendix_width + appendix_width + appendix_offset_x
        offset_y_fix = self.in_line_space * 4.5
        pos_x = self.x
        pos_y = self.y + offset_y_fix - note_info[0] * self.in_line_space / 2
        if self.x + x_inc > self.width:
            self.nextLine()
        dict = {}
        dict['outline'] = 'black'
        dict['fill']   = 'black'
        dict['smooth'] = 'true'
        apply(self.canvas.create_polygon,
            tuple(poly_oval(pos_x, pos_y, pos_x + note_width,
                            pos_y + note_height, rotation=20)
            ), dict)
        if note_info[1]:
            pos_y += note_height/2
            pos_x += note_space_x + note_width + appendix_offset_x
            self.canvas.create_text(pos_x, pos_y, text='#')
        self.drawLines(x_inc)
        self.x += x_inc


def detecting():
    global tk, painter
    note = round(detect.getNote())
    #print note
    painter.drawNote(note)
    tk.after(100, detecting)
    
tk = Tkinter.Tk()
painter = Painter(tk, 1000, 600)
tk.after(100, detecting)
tk.protocol('WM_DELETE_WINDOW', tk.quit)
tk.mainloop()
