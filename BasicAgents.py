# This file contains Agent 2 from project 2 without any improvements
# In the place where it would have picked a random choice from project 2
# it will now do the specific function passed to the agent (rand_choice, min_risk, min_cost)
import random
import pygame
from Minesweeper import Minesweeper
from Knowledgebase import A2 as KB

# Color tuples for pygame
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 00)
GREEN = (0, 250, 0)
BLUE = (0, 0, 255)

ORIGIN = (0, 0)

# Stuff for graphics
pygame.init()
screen_size = 960
screen = pygame.display.set_mode((screen_size, screen_size))
screen.fill(WHITE)
pygame.display.flip()
pygame.event.get()



def basic_agent(game, choice_func):
    # initializing knowledge base
    knowledge_base = KB(game)

    # variable to stop querying if the game is over (All mines have been queried or flagged
    game_over = False

    # Picks first move
    analyze_kb(game, knowledge_base, choice_func)

    # game loop, queries till game is over
    while not game_over:

        # Checks if there is any cells that are safe and can be queried
        while len(knowledge_base.safe) > 0:

            # Takes off the first cell to query
            cell = knowledge_base.safe.pop(0)

            # querying that cell returns if it was a mine and clue
            clue = game.query(cell.row, cell.col)

            # Updating pygame window (Graphics)
            game_update(game, cell.row, cell.col)

            # Updating Knowledgebase (consists of updating information about querried cells and making deductions)
            knowledge_base.update(cell.row, cell.col, clue[1], clue[0])

            # Using Deductions to add safe cells to safe
            analyze_kb(game, knowledge_base, choice_func)

        # checks if game is over if so prints score and ends game
        if game.game_over():
            score = game.calculate_score()
            game_over = True
            return score

# This function analyzes the current state of the knowledge base. It looks to see if any cells can be moved to safe
# and if a cell is 100% a mine it will flag it and update the knowledge base
def analyze_kb(game, kb, choice_func):

    # Variable to tell if an action has been made.
    action = True

    # knowledgebase analysis will happen again with the new deductions from each action
    while action:
        action = False
        # List of Lists in unsafe to be removed
        remove_after = []

        # List of cells that have been flagged and need to be removed
        update_as_flagged = []

        # Using deductions made in knowledgebase to make choice on which cells can be querried
        for i in range(len(kb.unsafe)):
            # Checking each list in Unsafe and seeing if there is 0 mines within those cells
            if kb.unsafe[i][0] == 0:
                action = True
                # if there are no mines within those cells it will add them to safe and add them
                # to a remove_after list to remove them. Can not remove on the spot because it will mess up the for loop
                remove_after.append(kb.unsafe[i])
                for j in range(1, len(kb.unsafe[i])):
                    kb.safe.append(kb.unsafe[i][j])

            # If there is still mines within those cells it will check if the number of cells is equal to the number of
            # mines. If so it will flag all those cells
            elif len(kb.unsafe[i][1:]) == kb.unsafe[i][0]:
                action = True
                # adds to remove after list
                remove_after.append(kb.unsafe[i])

                # for each cell in the list it will flag those cells
                for cell in kb.unsafe[i][1:]:
                    # Flag cell
                    game.flag(cell.row, cell.col)
                    # Update pygame window (Graphics)
                    game_update(game, cell.row, cell.col)
                    # Add cell to a list so that the KB can be updated
                    update_as_flagged.append(cell)
        # Removing all lists in unsafe that need to be removed
        for i in remove_after:
            kb.unsafe.remove(i)

        # Updates KB with cells that have been flagged and makes new deductions based on these
        for cell in update_as_flagged:
            kb.update(cell.row, cell.col, -1, True)

    # If after knowledgebase analysis there are no safe cells
    # it will do passed function (rand choice, min cost, or min risk)
    if len(kb.safe) == 0:
        choice_func(game, kb)


def rand_choice(game, kb):
    while True:
        if game.game_over():
            break
        # picks random row and col
        row = random.randint(0, game._dim - 1)
        col = random.randint(0, game._dim - 1)

        # checks to make sure random row and col is covered if so adds it to safe
        if kb.knowledge_base[row][col].covered and not kb.knowledge_base[row][col].mine:
            kb.safe.append(kb.knowledge_base[row][col])
            return

def min_risk(game, kb):
    # TODO: Put in min risk stuff here (remove pass)
    pass

def min_cost(game, kb):
    # TODO: Put in min cost stuff here (remove pass)
    pass

# for graphics: will update full screen
def game_full_update(game):
    game_updated = game.draw(screen_size)
    pygame.display.set_mode((game_updated.get_size()[0], game_updated.get_size()[1]))
    screen.blit(game_updated, ORIGIN)
    pygame.display.update()

# for graphics: will update part of screen specified by the row and col
def game_update(game, row, col):
    ret_draw = game.draw_single(screen_size, row, col)
    game_updated = ret_draw[0]
    img_size = ret_draw[1]
    screen.blit(game_updated, (col * img_size, row * img_size))
    pygame.display.update((col * img_size, row * img_size, img_size, img_size))
    pygame.event.get()

if __name__ == '__main__':

    try:
        ipt = int(input("To run a single game of minesweeper enter 0 "
                        "otherwise to run our testing method to figure out success rate per density enter 1 \n"))
    except ValueError:
        print("Incorrect Entry")

    if ipt == 0:
        set = False
        while not set:
            try:
                cfunc = int(input("To run the game using random choice enter 0"
                                "\nTo run the game using min cost enter 1"
                                "\nTo run the game using min risk enter 2 \n"))
                set = True
            except ValueError:
                print("Incorrect Entry")
        set = False
        while not set:
            try:
                size = int(input("Enter the size, for example enter 30 for a 30 x 30 grid\n"))
                set = True
            except ValueError:
                print("Incorrect Entry")
        set = False
        while not set:
            try:
                num_mines = int(input("Enter the number of mines\n"))
                set = True
            except ValueError:
                print("Incorrect Entry")

        game = Minesweeper(size, num_mines)
        game_full_update(game)
        score = 0

        if cfunc == 0:
            score = basic_agent(game, rand_choice)
        elif cfunc == 1:
            score = basic_agent(game, min_cost)
        elif cfunc == 2:
            score = basic_agent(game, min_risk)
        else:
            print("Quiting")
            pygame.quit()
            quit()

        print("Score: " + str(score))
        print("press X on pygame window to quit")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    elif ipt == 1:
        pass
        # size = 30
        # density = 0
        # total_score = 0
        # while density <= 1:
        #     num_tests = 100
        #     for i in range(num_tests):
        #         game = Minesweeper(size, int((size**2) * density))
        #         game_full_update(game)
        #         score = basic_agent(game)
        #         total_score += score
        #     print(str(density) + ", " + str(total_score/num_tests))
        #     total_score = 0
        #     density += 0.05
        #     density = round(density, 2)
        #
        # running = True
        # while running:
        #     for event in pygame.event.get():
        #         # print(event)
        #         if event.type == pygame.QUIT:
        #             running = False
    else:
        print("Quiting")

    pygame.quit()
    quit()