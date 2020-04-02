class Shapes:

    currentShape = None

    def __init__(self):
        # initial coordinates of each shape
        self.box = [[120, 840], [120, 880], [160, 840], [160, 880]]
        self.el_right = [[120, 840], [120, 880], [120, 920], [160, 840]]
        self.el_left = [[120, 840], [160, 840], [160, 880], [160, 920]]
        self.zee_right = [[120, 840], [120, 880], [160, 880], [160, 920]]
        self.zee_left = [[120, 920], [120, 880], [160, 880], [160, 840]]
        self.line = [[120, 840], [120, 880], [120, 920], [120, 960]]
        self.tri = [[120, 840], [160, 840], [200, 840], [160, 880]]
        self.shapes = [self.box, self.el_right, self.el_left, self.tri, self.line, self.zee_left, self.zee_right]

    def generate_new_shape(self, num):
        # giving equal probability to each shape
        if num == 7:
            num = 0
        elif num == 8:
            num = 3
        elif num == 9:
            num = 4
        self.currentShape = self.shapes[num]

    def get_shape(self):
        num = self.get_shape_number()
        if num == 0:
            color = 'green'
        elif num == 1 or num == 2:
            color = 'orange'
        elif num == 3:
            color = 'pink'
        elif num == 4:
            color = 'blue'
        elif num == 5 or num == 6:
            color = 'yellow'

        return self.currentShape, color

    def get_shape_number(self):
        return self.shapes.index(self.currentShape)

