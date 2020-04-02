# This file contains Agent 2 from project 2 without any improvements
# In the place where it would have picked a random choice from project 2
# it will now do the specific function passed to the agent (rand_choice, min_risk, min_cost)
import random
import pygame
import copy
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

aaaaaaaaaaaaaa = 0


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
    global aaaaaaaaaaaaaa
    while True:
        if game.game_over():
            break
        # picks random row and col
        # row = random.randint(0, game._dim - 1)
        # col = random.randint(0, game._dim - 1)
        if aaaaaaaaaaaaaa == 0:
            row = 0
            col = 0
        elif aaaaaaaaaaaaaa == 1:
            row = 3
            col = 3
        elif aaaaaaaaaaaaaa == 2:
            row = 1
            col = 2
        else:
            row = random.randint(0, game._dim - 1)
            col = random.randint(0, game._dim - 1)

        # checks to make sure random row and col is covered if so adds it to safe
        if kb.knowledge_base[row][col].covered and not kb.knowledge_base[row][col].mine:
            kb.safe.append(kb.knowledge_base[row][col])
            aaaaaaaaaaaaaa = aaaaaaaaaaaaaa + 1
            return

def min_cost(game, kb_original):
    # TODO: Put in min cost stuff here (remove pass)
    # creating sections, Sections are made from all the clues in unsafe -- If any 2 clues contain atleast
    # one of the same cells they are in the same section

    kb = copy.deepcopy(kb_original)
    sections = []
    for current in kb.unsafe:
        current_cells = current[1:]
        found_section = []
        for section in sections:
            for clue in section:
                cells_in_clue = clue[1:]
                sectionclue_as_set = set(cells_in_clue)
                intersect = [value for value in current_cells if value in sectionclue_as_set]
                if len(intersect) >= 1:
                    found_section.append(section)
                    break
        if len(found_section) >= 1:
            found_section[0].append(current)
            the_rest = found_section[1:]
            for temp in the_rest:
                for clue in temp:
                    found_section[0].append(clue)
                sections.remove(temp)
            break
        else:
            sections.append([current])

    sections_as_kbs = []
    for section in sections:
        temp = KB(game)
        temp.manual_add_unsafe(section)
        sections_as_kbs.append(temp)

    # Put this in get mine configuration function ---------------------------------------------------------------
    # Figuring out all possible configuration of mines
    for section_original in sections_as_kbs:
        section = copy.deepcopy(section_original)
        cells_in_section = []
        for unsafe_list in section.unsafe:
            cells_in_section = cells_in_section + unsafe_list[1:]

        cells_in_section = list(set(cells_in_section))

        mine_configs = list()
        while len(cells_in_section) > 0:
            section = copy.deepcopy(section_original)
            simulated_mine_list = []
            while len(section.unsafe) > 0:
                current = section.knowledge_base[cells_in_section[0].row][cells_in_section[0].col]
                for clue in section.unsafe:
                    if current in clue[1:]:
                        cells_in_section.pop(0)
                        simulated_mine_list.append(current)
                        break
                section.update(current.row, current.col, -1, True)

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
                    for i in range(len(section.unsafe)):
                        # Checking each list in Unsafe and seeing if there is 0 mines within those cells
                        if section.unsafe[i][0] == 0:
                            action = True
                            # if there are no mines within those cells it will add them to safe and add them
                            # to a remove_after list to remove them. Can not remove on the spot because it will mess up the for loop
                            remove_after.append(section.unsafe[i])
                            for j in range(1, len(section.unsafe[i])):
                                section.safe.append(section.unsafe[i][j])

                        # If there is still mines within those cells it will check if the number of cells is equal to the number of
                        # mines. If so it will flag all those cells
                        elif len(section.unsafe[i][1:]) == section.unsafe[i][0]:
                            action = True
                            # adds to remove after list
                            remove_after.append(section.unsafe[i])
                            # for each cell in the list it will flag those cells
                            for cell in section.unsafe[i][1:]:
                                simulated_mine_list.append(cell)
                                # Add cell to a list so that the KB can be updated
                                update_as_flagged.append(cell)
                    # Removing all lists in unsafe that need to be removed
                    for i in remove_after:
                        section.unsafe.remove(i)

                    # Updates KB with cells that have been flagged and makes new deductions based on these
                    for cell in update_as_flagged:
                        section.update(cell.row, cell.col, -1, True)
                    section.simplify()
            mine_configs.append(simulated_mine_list)
        for config in mine_configs:
            print("\n")
            for mine in config:
                print(str(mine) + ", ", end=" ")
    print("\n\n\n\n")


    # Put above in get mine configuration function ---------------------------------------------------------------

    # If no probabilities can be derived reverts back to unsafe
    rand_choice(game, kb_original)
    # row = 0
    # col = 0
    # kb.safe.append(kb.knowledge_base[row][col])



def min_risk(game, kb):
    # TODO: Put in min risk stuff here (remove pass)
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
        is_set = False
        while not is_set:
            try:
                cfunc = int(input("To run the game using random choice enter 0"
                                "\nTo run the game using min cost enter 1"
                                "\nTo run the game using min risk enter 2 \n"))
                is_set = True
            except ValueError:
                print("Incorrect Entry")
        is_set = False
        while not is_set:
            try:
                size = int(input("Enter the size, for example enter 30 for a 30 x 30 grid\n"))
                is_set = True
            except ValueError:
                print("Incorrect Entry")
        is_set = False
        while not is_set:
            try:
                num_mines = int(input("Enter the number of mines\n"))
                is_set = True
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