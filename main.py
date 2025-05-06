import curses, time, random

max_x = 60
max_y = 20
dir_keys = "wasd"

class Field:
    _shrooms = []
    _shroom_start_health = 3
    
    def __init__(self, size = (0,0), difficulty = 8):
        self._size = size
        self._difficulty = difficulty
        self.reset()

    def reset(self):
        self._init_shrooms()

    def _init_shrooms(self):
        self._shrooms = []
        max_x, max_y = self._size
        for i in range(max_y - 1):
            y = i + 1
            x_check = []
            for _ in range(self._difficulty):
                x = random.randint(1, max_x)
                if x in x_check:
                    continue
                self._shrooms.append([x, y, self._shroom_start_health])

    def check_collision(self, pos, damage=False):
        for i in range(len(self._shrooms)):
            spos = tuple(self._shrooms[i][:2])
            if spos == pos:
                if damage:
                    self._shrooms[i][2] -= 1
                if self._shrooms[i][2] == 0:
                    del self._shrooms[i]
                return True
        return False
    
    def check_boundary(self, pos):
        x, y = pos
        max_x, max_y = self._size
        if x <= 0 or y <= 1:
            return True
        if x >= max_x or y >= max_y:
            return True
        return False

    def draw(self, win):
        for shroom in self._shrooms:
            x, y, d = shroom
            match d:
                case 3:
                    ch = "&"
                case 2:
                    ch = "#"
                case 1:
                    ch = "+"
                case _:
                    # Shouldn't happen
                    # we may want to throw an exception
                    ch = ""
            win.addch(y, x, ord(ch))
        
    def get_shooter_start(self):
        max_x, max_y = self._size
        return (max_x//2, max_y)

class Centipede:
    def __init__(self, length, field):
        self._length = length
        self._field = field
        self._body = [(1,1)]
        self._direction = (1,0)

    def draw(self, win):
        for seg in self._body:
            x, y = seg
            win.addch(y, x, ord("0"))

    def _reverse(self):
        x, y = self._direction
        self._direction = (x*-1, y)

    def _avoid(self):
        x, y = self._body[0]
        self._reverse()
        return (x, y+1)

    def move(self):
        x, y = self._body[0]
        dx, dy = self._direction
        n = (x + dx, y + dy)
        if self._field.check_collision(n) or self._field.check_boundary(n):
            n = self._avoid()
        
        self._body.insert(0, n)
        if len(self._body) > self._length:
            self._body = self._body[:self._length]

class Shooter:
    def __init__(self, field, centipede):
        self._bullet = None
        self._field = field
        self._centipede = centipede
        self._pos = field.get_shooter_start()

    def draw(self, win):
        x, y = self._pos
        win.addch(y, x-1, ord("/"))
        win.addch(y, x, ord("^"))
        win.addch(y, x+1, ord('\\'))
        if self._bullet != None:
            bx, by = self._bullet
            win.addch(by, bx, ord("|"))
            if self._field.check_collision(self._bullet, True) or self._field.check_boundary(self._bullet):
                self._bullet = None
            else:
                self._bullet = (bx, by-1)

    def move(self, direction):
        x, y = self._pos
        dx, dy = direction
        self._pos = (x+dx, y+dy)

    def shoot(self):
        x, y = self._pos
        if self._bullet == None:
            self._bullet = (x, y-1)

def get_direction(key):
    match key:
        case "w":
            return (0,-1)
        case "a":
            return (-1,0)
        case "s":
            return (0,1)
        case "d":
            return (1,0)

def main(screen):
    curses.curs_set(0)
    screen.clear()

    win = curses.newwin(max_y + 2, max_x + 2, 2, 5)
    win.box()

    field = Field((max_x, max_y), difficulty=4)
    centi = Centipede(10, field)
    shoot = Shooter(field, centi)


    count = 0
    while True:
        count += 1
        win.clear()
        win.box()

        field.draw(win)

        if count % 8 == 0:
            centi.move()
        centi.draw(win)

        win.nodelay(True)
        try:
            key = win.getkey()
            if key != curses.ERR:
                if key in dir_keys:
                    dir = get_direction(key)
                    shoot.move(dir)
                if key == "q":
                    shoot.shoot()
        except (curses.error):
            pass

        shoot.draw(win)

        win.refresh()
        time.sleep(0.01)
    

    screen.refresh()
    screen.getkey()

curses.wrapper(main)
