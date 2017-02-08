'''
Modified from code found at https://gist.github.com/sanchitgangwar/2158089
Original author: Sanchit Gangwar (sanchitgangwar)

Written for use by Albany NY Coder Dojo.
Description: A modularized version of the old arcade game snake. The intention is to provide a pre-compiled version
 of this code as a module to the students. Students are broken up into groups and given started code that contains a
 main, imports, and function prototypes and the pre-compiled library. Students will be able to instantiate the object
  and complete their own assigned functions. At the end everyone's functions can be brought together to create a working
   version of snake.
Author: Jeramey Tyler
'''

# curses is used to handle the window and key events
from curses import wrapper
import curses
# Random is used to find the next food location
import random


class Snake:
    # The current direction the snake is travelling
    key = curses.KEY_RIGHT
    # The current score. Increases in increments of 1000
    score = 0

    # Position of the snake
    snake = [[4, 10], [4, 9], [4, 8]]
    # Position of the food
    food = [10, 20]

    # Window dimensions
    width = 60
    height = 20

    # Here's where it gets a little weird. This is dictionary of lambda functions. The Key is a label and the value is a
    # lambda function. Example funcs['score']() is the same as self.update_score(). I use this so that I can dynamically
    # assign operations to different functions depending on what is passed to the constructor.
    funcs = {}

    # The curses window object
    win = ''
    # The previous key that was pressed
    prevKey = key

    # Constructor for snake. Requires a dictionary like funcs above. The basic idea is that  by storing lambda functions
    # that point to actual functions within this class
    def __init__(self, new_funcs):
        # Set all of the standard implementations of snake game
        self.funcs['score'] = lambda score: self.update_score(score)
        self.funcs['food'] = lambda snake, width, height: self.get_new_food_location(snake, width, height)
        self.funcs['pause'] = lambda: self.pause()
        self.funcs['move'] = lambda key, snake: self.move(key, snake)
        self.funcs['collision'] = lambda snake, width, height: self.collision_detection(snake, width, height)
        self.funcs['eat'] = lambda food, snake: self.eat(food, snake)
        self.funcs['end'] = lambda: self.end()
        self.funcs['print'] = lambda: self.print()
        self.funcs['grow'] = lambda key, snake: self.grow_snake(key, snake)

        # Now iterate over the alternate functions passed in.
        for f in new_funcs.keys():
            if f in self.funcs.keys():
                self.funcs[f] = new_funcs[f]

        # This is used by curses to handle the screen (I think)
        wrapper(self.run)

    # The function that runs the game
    def run(self, stdscr):
        # This is the curses window
        self.win = stdscr
        # Allows keypad keys
        self.win.keypad(1)
        # This makes getch a non-blocking function call
        self.win.nodelay(1)

        curses.noecho()
        curses.curs_set(0)

        # While the escape key hasn't been pressed
        cont = True
        while cont:
            # Print the screen
            self.funcs['print']()

            # Get key press
            self.prevKey = self.key
            event = stdscr.getch()

            # If the getch event is valid assign the key to self.key
            self.key = self.key if event == -1 else event

            # If key pressed was space bar then pause game
            if self.key == ord(' '):
                self.funcs['pause']()
                # If the escape key (or alt I think) is pressed quit the game
            elif self.key == 27:
                cont = False
            # if the key that was pressed was a direction key
            elif self.key not in [curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_LEFT, curses.KEY_DOWN]:
                self.key = self.prevKey
            else:
                # Move the snake and check for collisions or whether or not the snake
                # got the food
                self.snake = self.funcs['move'](self.key, self.snake)
                if self.funcs['collision'](self.snake, self.width, self.height):
                    self.key = 27
                else:
                    if self.funcs['eat'](self.food, self.snake):
                        self.score = self.funcs['score'](self.score)
                        self.food = self.funcs['food'](self.snake, self.width, self.height)
                        self.snake = self.funcs['grow'](self.key, self.snake)

            # Refresh the screen
            stdscr.refresh()
        self.funcs['end']()

    # Increment the score accordingly
    def update_score(self, score):
        # Completely arbitrary scoring system here.
        return score + 1000

    # Get the next location for food
    def get_new_food_location(self, snake, width, height):
        food = []
        # Generate a set of random coordinates between the borders. If the set is inside
        # of the snake repeat
        while not food:
            food = [random.randint(2, height + 1), random.randint(1, width)]
            if food in snake:
                food = []
        return food

    # Because this function waits for input I don't think I can pass this as a lambda
    def pause(self):
        self.key = -1
        # While the space bar isn't pressed
        while self.key != ord(' '):
            self.key = self.win.getch()
        # set the snake direction in the direction of the most recent key press before the pause
        self.key = self.prevKey

    # Find the new position of the snake's head
    def move(self, key, snake):
        if key == curses.KEY_RIGHT:
            snake.insert(0, [snake[0][0], snake[0][1] + 1])
        elif key == curses.KEY_UP:
            snake.insert(0, [snake[0][0] - 1, snake[0][1]])
        elif key == curses.KEY_LEFT:
            snake.insert(0, [snake[0][0], snake[0][1] - 1])
        elif key == curses.KEY_DOWN:
            snake.insert(0, [snake[0][0] + 1, snake[0][1]])
        snake.pop()
        return snake

    # Detect if the snake intersected itself or if the snake went out of bounds
    def collision_detection(self, snake, width, height):
        # if the snake's head has intersected it's body or if it has left the board
        if snake[0] in snake[1:] \
                or snake[0][0] <= 1 or snake[0][1] <= 0 \
                or snake[0][0] > height + 1 or snake[0][1] > width:
            return True
        return False

    # Detect if the snake found the food
    def eat(self, food, snake):
        if snake[0] == food:
            return True
        else:
            return False

    # Increase the size of the snake
    def grow_snake(self, key, snake):
        # Copy the last element in the snake and adjust it accordingly
        snake_length = len(snake)
        snake.append(snake[snake_length - 1])
        if key == curses.KEY_RIGHT:
            snake[snake_length][1] -= 1
        elif key == curses.KEY_UP:
            snake[snake_length][0] += 1
        elif key == curses.KEY_LEFT:
            snake[snake_length][1] += 1
        elif key == curses.KEY_DOWN:
            snake[snake_length][0] -= 1
        return snake

    # The function that closes the application
    def end(self):
        self.key = 0
        while self.key != 27 and self.key != ord(' '):
            # Delete anything on the screen already
            self.win.clear()

            # Print score and title
            self.funcs['print']()
            self.win.addstr(9, 25, 'Game Over')

            # Set delay time
            self.win.timeout(int(150 - (len(self.snake) / 5 + len(self.snake) / 10) % 120))

            # Get key press
            self.prevKey = self.key
            event = self.win.getch()

            self.key = self.key if event == -1 else event

            # If key pressed was space bar then pause game
            if self.key == ord(' '):
                self.score = 0

                self.snake = [[4, 10], [4, 9], [4, 8]]
                self.food = [10, 20]
        if self.key == 27:
            curses.endwin()
        else:
            self.key = curses.KEY_RIGHT
            self.run(self.win)

    def print(self):

        # Delete anything on the screen already
        self.win.clear()

        # Print score, title, and border
        self.win.addstr(0, 2, 'Score : ' + str(self.score) + ' ')
        self.win.addstr(0, 27, ' SNAKE ')
        self.win.addstr(1, 0, '-' * (self.width + 2))
        self.win.addstr(2 + self.height, 0, '-' * (self.width + 2))

        for i in range(self.height):
            self.win.addch(i + 2, 0, '|')
            self.win.addch(i + 2, self.width + 1, '|')

        # Set delay time
        self.win.timeout(int(150 - (len(self.snake) / 5 + len(self.snake) / 10) % 120))

        # Add food to screen
        self.win.addch(self.food[0], self.food[1], '*')

        for s in self.snake:
            self.win.addch(s[0], s[1], '+')


if __name__ == '__main__':
    s = Snake({})
