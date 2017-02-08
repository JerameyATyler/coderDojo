"""
Hope you aren't afraid of snakes because your job is to finish the incomplete python functions.
When all of the functions are functioning (pun intended) correctly you will be able to play
the old arcade game snake. To test your code you can un-comment (remove the '# ') from corresponding
lines in '__main__' at the bottom.
"""
from snake import Snake
import curses


# This should return the player's score after it has been updated. What do you think would
# make a good scoring system?
def update_score(score):
    """
    Rating: *
    The player's snake just got the food, what should their new score be?
    :param score: The player's current score
    :return: The player's new score
    """
    return score


# This should return the new position of the food as a tuple. A tuple
# is just two things together as a pair, like (x, y) or (2, 8). You can make a new tuple
# like tuple(verticle_position, horizontal_position)
def get_new_food_location(snake, width, height):
    """
    Rating: **
    The snake just got the food but it's still hungry. Where should we put the next piece
    of food? Are there any places that we shouldn't place the food?
    :param snake: A list of all of the positions that the snake occupies
    :param width: The width of the game area
    :param height: The height of the game area
    :return: A tuple that has the position of the new piece of food. (height_position, width_position)
    """
    return tuple((30, 10))


# This function should return the snake with each of its pieces updated to move in the
# correct direction.
def move(key, snake):
    """
    Rating: ***
    The snake will never catch anything to eat if it never moves. We know the player pressed
    an arrow key but which one and what do we do about it?
    HINT: The arrow keys are [curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_LEFT, curses.KEY_DOWN]
    :param key: The key that the player pressed
    :param snake: A list of all of the positions that the snake occupies
    :return: Return the snake after all of it's positions have been updated
    """

    return snake


# This function should return True if the most recent move caused the snake to touch itself or go out
# of bounds.
def collision_detection(snake, width, height):
    """
    Rating: ****
    Did the snake bite itself? Did the snake go out of bounds? If either of these happened we should tell someone.
    HINT: The width and height are the width and height of the game area, not the entire window. Don't forget
    about the border and score.
    :param snake: A list of all of the positions that the snake occupies
    :param width: The width of the game area
    :param height: The height of the game area
    :return: A Boolean (True or False) value that represents whether or not the most recent move was a good one
    """
    return False


# This function should detect whether or not the snake found the food
def eat(food, snake):
    """
    Rating: *
    Did the snake find the food?
    :param food: The current position of the food
    :param snake: A list of all of the positions that the snake occupies
    :return: A Boolean (True or False) value that represents whether or not the snake found the food
    """
    return False


# This function increases the size of the snake
def grow_snake(key, snake):
    """
    Rating: ***
    The snake ate too much and how has to shed it's skin and grow. If we add a new piece to the snake where
    should it go?
    :param key: The key that the player pressed
    :param snake: A list of all of the positions that the snake occupies
    :return: Return the snake after you've increased it's size
    """
    return snake

if __name__ == '__main__':
    funcs = dict()
    '''
        Each of the lines below correspond to one of the functions above. If you want to test
        your remove the '#' from the front of the appropriate line. These lines are the only changes
        that you should make to __main__
    '''
    # funcs['score'] = lambda score: update_score(score)
    # funcs['food'] = lambda snake, width, height: get_new_food_location(snake, width, height)
    # funcs['move'] = lambda key, snake: move(key, snake)
    # funcs['collision'] = lambda snake, width, height: collision_detection(snake, width, height)
    # funcs['eat'] = lambda food, snake: eat(food, snake)
    # funcs['grow'] = lambda key, snake: grow_snake(key, snake)
    '''Create the snake object'''
    s = Snake(funcs)
