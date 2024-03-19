import consts


class Snake:

    dx = {'UP': 0, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}
    dy = {'UP': -1, 'DOWN': 1, 'LEFT': 0, 'RIGHT': 0}

    def __init__(self, keys, game, pos, color, direction):
        self.keys = keys
        self.cells = [pos]
        self.game = game
        self.game.add_snake(self)
        self.color = color
        self.direction = direction
        game.get_cell(pos).set_color(color)

    def get_head(self):
        return self.cells[-1]

    def val(self, x):
        if x < 0:
            x += self.game.size

        if x >= self.game.size:
            x -= self.game.size

        return x

    def next_move(self):
        head = self.get_head()
        x = self.val(head[0] + Snake.dx[self.direction])
        y = self.val(head[1] + Snake.dy[self.direction])
        next_pos = (x, y)
        next_color = self.game.get_cell(next_pos).color
        if next_color == consts.block_color:
            self.game.kill(self)
            return
        elif next_color == consts.fruit_color:
            self.cells.append(next_pos)
            self.game.get_cell(next_pos).set_color(self.color)
            return
        else:
            prev_pos = self.cells.pop(0)
            self.game.get_cell(prev_pos).set_color(consts.back_color)
            self.cells.append(next_pos)
            self.game.get_cell(next_pos).set_color(self.color)

    def handle(self, keys):
        for key in keys:
            try:
                key_move = self.keys[key]
                if (self.direction in ["LEFT", "RIGHT"]) and (key_move in ["UP", "DOWN"]):
                    self.direction = key_move

                elif (self.direction in ["UP", "DOWN"]) and (key_move in ["RIGHT", "LEFT"]):
                    self.direction = key_move
            except:
                continue

        self.next_move()

