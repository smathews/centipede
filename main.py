import curses, time, random

max_x = 60
max_y = 20

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
        
def new_food():
    return (random.randint(1,max_x-1), random.randint(1,max_y-1))

def draw_snake(win, snake):
    for seg in snake:
        x, y = seg
        win.addch(y, x, ord("0"))

def draw_food(win, food):
    x, y = food
    win.addch(y, x, ord("+"))

def collision(head, snake):
    for seg in snake:
        if seg == head:
            return True
    return False

def main(screen):
    curses.curs_set(0)
    screen.clear()

    win = curses.newwin(max_y + 2, max_x + 2, 2, 5)
    win.box()

    x, y = 0, 5
    key = "d"

    snake_len = 5
    snake = [(1,1)]
    food = new_food()
    while True:
        x, y = snake[0]
        dx, dy = get_direction(key)
        x = x + dx
        y = y + dy
        if x == (max_x + 1):
            x = 0
        elif x == 0:
            x = max_x

        if y == (max_y + 1):
            y = 0
        elif y == 0:
            y = max_y
        
        head = (x,y)

        if collision(head, snake):
            for i in range (0, 20):
                screen.addstr(i, 0, "YOU DIED!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                screen.refresh()
                time.sleep(0.05)
            break

        if head == food:
            snake_len += 5
            food = new_food()

        snake = [head] + snake
        if len(snake) > snake_len:
            snake = snake[:snake_len]

        screen.addstr(1,0, "head: (%s,%s)" % head)
        screen.refresh()
        win.box()

        win.clrtobot()
        win.clear()
        draw_snake(win, snake)
        draw_food(win, food)
        win.refresh()
        win.box()


        win.nodelay(True)
        try:
            key = win.getkey()
            if key != curses.ERR:
                screen.addstr(0, 0, "You pressed: %s" % key)
                screen.refresh()
                win.box()
        except (curses.error):
            pass

        win.refresh()
        time.sleep(0.1)
    

    screen.refresh()
    screen.getkey()

curses.wrapper(main)
