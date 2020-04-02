from time import sleep
import pyglet.window
from pyglet.window import key
from src.Shapes import Shapes
from random import randint
import pyglet.clock


# 90 degrees clockwise rotation
def transformation(x, y):
    temp = x
    x = y
    y = -temp
    return x, y


class Game(pyglet.window.Window):
    # shape object
    shape = Shapes()
    score = 0
    # loading images of square blocks, which make up the shapes
    blue = pyglet.resource.image('src/assets/blue.png')
    green = pyglet.resource.image('src/assets/green.png')
    orange = pyglet.resource.image('src/assets/orange.png')
    pink = pyglet.resource.image('src/assets/pink.png')
    yellow = pyglet.resource.image('src/assets/yellow.png')
    # the stone slab at the bottom of the window
    stone_slab = pyglet.resource.image('src/assets/stone.png')
    game_over_flag = False
    # Game board created as a 2D array. 0 represents the position is empty. 
    # 1 means the position is occupied by a block.
    # The coordinates of shapes are calculated using: index*40, where index is the index of the location on board
    board = [[0 for x in range(11)] for y in range(24)]
    # the bottom of the board is occupied by stone slab
    board[0] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    # number of the shape
    num = 0
    # shape rotation flag
    rotationFlag = True
    # slab is the stone slab at the bottom
    slab = []
    # base represents the blocks which have been fixed on the board.
    base = []
    # a shape/piece is made of four separate blocks, each having same colour and different x,y coordinates
    piece = [[], [], [], []]
    # color of the shape. shapes have been classified using colours.
    # color is used to assign the image given to the shape
    color = None
    one_block = 40          # 40 pixels

    def __init__(self):
        super().__init__(440, 720, 'Tetris')
        self.set_location(500, 50)
        
        # creating sprites of stone slabs so they can be rendered.
        for p in range(0, 440, self.one_block):
            self.slab.append(pyglet.sprite.Sprite(img=self.stone_slab, x=p, y=0))

        self.label = pyglet.text.Label('0', font_name='Times New Roman', font_size=36, x=5, y=680)
        self.label2 = pyglet.text.Label('Game Over', font_name='Times New Roman', font_size=60,
                                   x=self.width // 2, y=self.height // 2, anchor_x='center', anchor_y='center')
        self.shape.generate_new_shape(randint(0, 6))
        self.get_new_shape()
        self.num = self.shape.get_shape_number()
        pyglet.clock.schedule_interval(self.update, 0.3)
        pyglet.app.run()

    # keyboard event handler
    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            if self.piece[0].x >= self.one_block and self.piece[1].x >= self.one_block and self.piece[2].x >= self.one_block and self.piece[3].x >= self.one_block and self.left_side_check():
                for x in range(4):
                    self.piece[x].x -= self.one_block

        elif symbol == key.RIGHT:
            if self.piece[0].x <= 360 and self.piece[1].x <= 360 and self.piece[2].x <= 360 and self.piece[
                3].x <= 360 and self.right_side_check():
                for x in range(4):
                    self.piece[x].x += self.one_block

        elif symbol == key.UP:
            self.rotate_piece()

        elif symbol == key.DOWN:
            while not self.collision_test():
                self.move_shape()

    # renders images onto the window
    def on_draw(self):
        self.clear()
        for p in range(len(self.slab)):
            self.slab[p].draw()
        for i in range(4):
            self.piece[i].draw()
        for k in range(len(self.base)):
            self.base[k].draw()
        self.label.draw()
        if self.game_over_flag:
            self.label2.draw()

    # returns True if the the shape has collided with the base blocks, as to prevent overlap,
    # and stopping the shape there
    def collision_test(self):
        if self.board[self.piece[0].y // self.one_block - 1][self.piece[0].x // self.one_block] == 1:
            return True
        elif self.board[self.piece[1].y // self.one_block - 1][self.piece[1].x // self.one_block] == 1:
            return True
        elif self.board[self.piece[2].y // self.one_block - 1][self.piece[2].x // self.one_block] == 1:
            return True
        elif self.board[self.piece[3].y // self.one_block - 1][self.piece[3].x // self.one_block] == 1:
            return True
        else:
            return False

    # checks if there is a block to the right of the shape
    def right_side_check(self):
        if self.board[self.piece[0].y // self.one_block][self.piece[0].x // self.one_block + 1] == 1:
            return False
        elif self.board[self.piece[1].y // self.one_block][self.piece[1].x // self.one_block + 1] == 1:
            return False
        elif self.board[self.piece[2].y // self.one_block][self.piece[2].x // self.one_block + 1] == 1:
            return False
        elif self.board[self.piece[3].y // self.one_block][self.piece[3].x // self.one_block + 1] == 1:
            return False
        else:
            return True

    # checks if there is a block to the left of the shape
    def left_side_check(self):
        if self.board[self.piece[0].y // self.one_block][self.piece[0].x // self.one_block - 1] == 1:
            return False
        elif self.board[self.piece[1].y // self.one_block][self.piece[1].x // self.one_block - 1] == 1:
            return False
        elif self.board[self.piece[2].y // self.one_block][self.piece[2].x // self.one_block - 1] == 1:
            return False
        elif self.board[self.piece[3].y // self.one_block][self.piece[3].x // self.one_block - 1] == 1:
            return False
        else:
            return True

    # rotate the shape
    def rotate_piece(self):
        # no need to rotate the box, hence this check
        if self.num != 0:
            # centre of rotation defined. same for all shapes
            centre = [self.piece[1].x, self.piece[1].y]
            # the rotation is tested on dummy coordinates first and checked if it valid. Then applied to the shape
            testpiece = [[], [], [], []]

            for p in range(4):
                testpiece[p] = [self.piece[p].x, self.piece[p].y]
                testpiece[p][0], testpiece[p][1] = testpiece[p][0] - centre[0], testpiece[p][1] - centre[1]
                testpiece[p][0], testpiece[p][1] = transformation(testpiece[p][0], testpiece[p][1])
                testpiece[p][0], testpiece[p][1] = testpiece[p][0] + centre[0], testpiece[p][1] + centre[1]

            for p in range(4):
                if testpiece[p][0] < 0:
                    testpiece[0][0] += self.one_block
                    testpiece[1][0] += self.one_block
                    testpiece[2][0] += self.one_block
                    testpiece[3][0] += self.one_block
                    p = 0
                elif testpiece[p][0] > 400:
                    testpiece[0][0] -= self.one_block
                    testpiece[1][0] -= self.one_block
                    testpiece[2][0] -= self.one_block
                    testpiece[3][0] -= self.one_block
                    p = 0
                if self.board[testpiece[p][1] // self.one_block][testpiece[p][0] // self.one_block] == 1:
                    self.rotationFlag = False

            if self.rotationFlag:
                for p in range(4):
                    self.piece[p].x, self.piece[p].y = testpiece[p][0], testpiece[p][1]
            else:
                self.rotationFlag = True

    # checks if a block has gone beyond the top of the screen
    def game_over(self):
        for t in range(11):
            if self.board[18][t] == 1:
                self.game_over_flag = True

    def move_shape(self):

        if self.collision_test():
            self.change_piece()

        for i in range(4):
            self.piece[i].y -= self.one_block

    def update_score(self, counter):
        self.score += 40 * counter
        self.label = pyglet.text.Label(str(self.score), font_name='Times New Roman', font_size=36, x=5, y=680)

    def remove_row(self, row):
        sleep(0.5)
        # brings all the rows of the board down by one unit
        for t in range(row, 23):
            for e in range(11):
                self.board[t][e] = self.board[t + 1][e]

        k = len(self.base)
        i = 0
        while i < k:
            if self.base[i].y == row * self.one_block:
                self.base.pop(i)
                i -= 1
            i += 1
            k = len(self.base)
        # updates the base array by removing blocks which are present int the removed row
        for n in range(len(self.base)):
            if self.base[n].y > row * self.one_block:
                self.base[n].y -= self.one_block

    def points_scored(self):
        counter = 0
        for w in range(1, 24):
            if self.board[w].count(1) == len(self.board[w]):
                counter += 1
                self.remove_row(w)
        self.update_score(counter)

    # this is the main event loop
    # this function has been scheduled to run until game is over
    def update(self, dt):
        self.move_shape()
        self.points_scored()
        self.game_over()
        # unschedule the function, ending the event loop, finishing the program
        if self.game_over_flag:
            pyglet.clock.unschedule(self.update)

    def get_new_shape(self):
        (piece, color) = self.shape.get_shape()

        if color == 'orange':
            self.piece[0] = pyglet.sprite.Sprite(self.orange, x=piece[0][0], y=piece[0][1])
            self.piece[1] = pyglet.sprite.Sprite(self.orange, x=piece[1][0], y=piece[1][1])
            self.piece[2] = pyglet.sprite.Sprite(self.orange, x=piece[2][0], y=piece[2][1])
            self.piece[3] = pyglet.sprite.Sprite(self.orange, x=piece[3][0], y=piece[3][1])
        elif color == 'pink':
            self.piece[0] = pyglet.sprite.Sprite(self.pink, x=piece[0][0], y=piece[0][1])
            self.piece[1] = pyglet.sprite.Sprite(self.pink, x=piece[1][0], y=piece[1][1])
            self.piece[2] = pyglet.sprite.Sprite(self.pink, x=piece[2][0], y=piece[2][1])
            self.piece[3] = pyglet.sprite.Sprite(self.pink, x=piece[3][0], y=piece[3][1])
        elif color == 'blue':
            self.piece[0] = pyglet.sprite.Sprite(self.blue, x=piece[0][0], y=piece[0][1])
            self.piece[1] = pyglet.sprite.Sprite(self.blue, x=piece[1][0], y=piece[1][1])
            self.piece[2] = pyglet.sprite.Sprite(self.blue, x=piece[2][0], y=piece[2][1])
            self.piece[3] = pyglet.sprite.Sprite(self.blue, x=piece[3][0], y=piece[3][1])
        elif color == 'green':
            self.piece[0] = pyglet.sprite.Sprite(self.green, x=piece[0][0], y=piece[0][1])
            self.piece[1] = pyglet.sprite.Sprite(self.green, x=piece[1][0], y=piece[1][1])
            self.piece[2] = pyglet.sprite.Sprite(self.green, x=piece[2][0], y=piece[2][1])
            self.piece[3] = pyglet.sprite.Sprite(self.green, x=piece[3][0], y=piece[3][1])
        elif color == 'yellow':
            self.piece[0] = pyglet.sprite.Sprite(self.yellow, x=piece[0][0], y=piece[0][1])
            self.piece[1] = pyglet.sprite.Sprite(self.yellow, x=piece[1][0], y=piece[1][1])
            self.piece[2] = pyglet.sprite.Sprite(self.yellow, x=piece[2][0], y=piece[2][1])
            self.piece[3] = pyglet.sprite.Sprite(self.yellow, x=piece[3][0], y=piece[3][1])

        self.color = color

    def get_color_image(self):
        if self.color == 'orange':
            return self.orange
        if self.color == 'pink':
            return self.pink
        if self.color == 'green':
            return self.green
        if self.color == 'blue':
            return self.blue
        if self.color == 'yellow':
            return self.yellow

    def change_piece(self):

        # self.color gives the color of the blocks to be added to the base
        for i in range(4):
            self.board[self.piece[i].y // self.one_block][self.piece[i].x // self.one_block] = 1
            self.base.append(pyglet.sprite.Sprite(img=self.get_color_image(), x=self.piece[i].x, y=self.piece[i].y))

        # using 0 to 9, to give every shape equal probability, as there are two variants of one shape present as well
        self.shape.generate_new_shape(randint(0, 9))
        self.get_new_shape()
        self.num = self.shape.get_shape_number()
