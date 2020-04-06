from random import randint
import pygame

d = pygame.image.load("Assets/bd.png")
f = pygame.image.load("Assets/bf.png")
m = pygame.image.load("Assets/bm.png")
p = dict()
p[0] = pygame.image.load("Assets/bp0.png")
p[1] = pygame.image.load("Assets/bp1.png")
p[2] = pygame.image.load("Assets/bp2.png")
p[3] = pygame.image.load("Assets/bp3.png")
p[4] = pygame.image.load("Assets/bp4.png")
p[5] = pygame.image.load("Assets/bp5.png")
p[6] = pygame.image.load("Assets/bp6.png")
p[7] = pygame.image.load("Assets/bp7.png")
p[8] = pygame.image.load("Assets/bp8.png")


class Minesweeper:

    def __init__(self, dim, num_mines):
        # making sure mines will fit
        if num_mines > dim**2:
            raise ValueError("Number of Mines Too High!!")

        self.__env = []
        self._dim = dim
        self._num_mines = num_mines
        self.__mines = []
        # creating minesweeper environment
        for row in range(dim):
            self.__env.append([])
            for col in range(dim):
                self.__env[row].append(Minecell())

        # setting mines in random places
        for i in range(num_mines):
            mine_set = False
            while not mine_set:
                row = randint(0, dim-1)
                col = randint(0, dim-1)
                if not self.__env[row][col].mine:
                    self.__env[row][col].mine = True
                    self.__mines.append(self.__env[row][col])
                    mine_set = True

        # below is for debugging sets mines only in 1,1 and 2,2
        # self.__env[1][1].mine = True
        # self.__mines.append(self.__env[1][1])
        # self.__env[2][2].mine = True
        # self.__mines.append(self.__env[2][2])

        # Setting clue for each cell
        for row in range(dim):
            for col in range(dim):
                mine_counter = 0

                # Setting clue if cell contain mine to -1
                if self.__env[row][col].mine:
                    self.__env[row][col].value = -1
                    continue

                # incrementing mine count for above and to the left cell
                if row - 1 >= 0 and col - 1 >= 0 and self.__env[row - 1][col - 1].mine:
                    mine_counter += 1


                # incrementing mine count for above cell
                if row - 1 >= 0 and col < dim and self.__env[row - 1][col].mine:
                    mine_counter += 1

                # incrementing mine count for above and to the right cell
                if row - 1 >= 0 and col + 1 < dim and self.__env[row - 1][col + 1].mine:
                    mine_counter += 1

                # incrementing mine count for the left cell
                if row >= 0 and col - 1 >= 0 and self.__env[row][col - 1].mine:
                    mine_counter += 1

                # incrementing mine count for the right cell
                if row >= 0 and col + 1 < dim and self.__env[row][col + 1].mine:
                    mine_counter += 1


                # incrementing mine count for below and to the left cell
                if row + 1 < dim and col - 1 >= 0 and self.__env[row + 1][col - 1].mine:
                    mine_counter += 1

                # incrementing mine count for below cell
                if row + 1 < dim and col >= 0 and self.__env[row + 1][col].mine:
                    mine_counter += 1

                # incrementing mine count for below and to the right cell
                if row + 1 < dim and col + 1 < dim and self.__env[row + 1][col + 1].mine:
                    mine_counter += 1

                # setting mine count to the value of the cell
                self.__env[row][col].value = mine_counter

    # function to query a cell that agent will use
    def query(self, row, col):
        return self.__env[row][col].query()

    # function to flag a cell that agent will use
    def flag(self, row, col):
        self.__env[row][col].flag()

    # function to calculate score
    def calculate_score(self):
        count = 0
        for cell in self.__mines:
            if cell.flagged and not cell.queried:
                count += 1
        if self._num_mines == 0:
            return 100
        return (count / self._num_mines) * 100

    # function to check if game is over
    def game_over(self):
        count = 0
        for row in self.__env:
            for cell in row:
                if cell.flagged or cell.queried:
                    count += 1
        return self._dim**2 == count

    # Function for graphics to draw the minesweeper game
    def draw(self, screen_size):
        img_size = int(screen_size / self._dim)
        surface_dim = img_size * self._dim
        surface = pygame.Surface((surface_dim, surface_dim))

        for row in range(len(self.__env)):
            for col in range(len(self.__env)):
                cell = self.__env[row][col]
                if not cell.queried and not cell.flagged:
                    surface.blit(pygame.transform.smoothscale(d, (img_size, img_size)), (col * img_size, row * img_size))
                elif cell.mine and cell.queried:
                    surface.blit(pygame.transform.smoothscale(m, (img_size, img_size)), (col * img_size, row * img_size))
                elif cell.flagged:
                    surface.blit(pygame.transform.smoothscale(f, (img_size, img_size)), (col * img_size, row * img_size))
                else:
                    surface.blit(pygame.transform.smoothscale(p[cell.value], (img_size, img_size)), (col * img_size, row * img_size))
        return surface

    # Function for graphics to draw the minesweeper game (only updates portion specified)
    def draw_single(self, screen_size, row, col):
        img_size = int(screen_size / self._dim)
        surface_dim = img_size
        surface = pygame.Surface((surface_dim, surface_dim))

        cell = self.__env[row][col]

        if not cell.queried and not cell.flagged:
            surface.blit(pygame.transform.smoothscale(d, (img_size, img_size)), (0, 0))
        elif cell.mine and cell.queried:
            surface.blit(pygame.transform.smoothscale(m, (img_size, img_size)), (0, 0))
        elif cell.flagged:
            surface.blit(pygame.transform.smoothscale(f, (img_size, img_size)), (0, 0))
        else:
            surface.blit(pygame.transform.smoothscale(p[cell.value], (img_size, img_size)), (0, 0))

        return surface, img_size


class Minecell:

    mine = False
    value = -1
    flagged = False
    queried = False

    def __init__(self):
        pass

    def __str__(self):
        return self.value

    def query(self):
        self.queried = True
        return self.mine, self.value

    def flag(self):
        if not self.queried:
            self.flagged = True

    def unflag(self):
        self.flagged = False





