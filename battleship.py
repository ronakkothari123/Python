import pygame
from random import random, randint

enemy_hit_board = []
enemy_ship_board = []
player_hit_board = []
player_ship_board = []
enemy_ships = []
player_ships = []

BOARD_WIDTH = 10
BOARD_HEIGHT = 10
CELL_SIZE = 40
MARGIN = 25

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
MAROON = (128, 0, 0)

def get_grid_coordinates(pos):
    """Convert mouse position to grid coordinates."""
    x, y = pos
    if MARGIN <= x < MARGIN + BOARD_WIDTH * CELL_SIZE:
        grid_x = (x - MARGIN) // CELL_SIZE
        grid_y = (y - 30 - MARGIN * 2) // CELL_SIZE
        if 0 <= grid_x < BOARD_WIDTH and 0 <= grid_y < BOARD_HEIGHT:
            return grid_x, grid_y
    return None

class Ship:
    def check_ship_position(self, x_coord, y_coord, enemy):
        # 0 = horizontal, 1 = vertical

        if self.direction == 0:
            if x_coord < BOARD_WIDTH - self.size + 1 and y_coord < BOARD_HEIGHT:
                for i in range(self.size):
                    if enemy and enemy_ship_board[y_coord][x_coord + i] == 1:
                        return False
                    elif not enemy and player_ship_board[y_coord][x_coord + i] == 1:
                        return False

                return True
        elif self.direction == 1:
            if x_coord < BOARD_WIDTH and y_coord < BOARD_HEIGHT - self.size + 1:
                for i in range(self.size):
                    if enemy and enemy_ship_board[y_coord + i][x_coord] == 1:
                        return False
                    elif not enemy and player_ship_board[y_coord + i][x_coord] == 1:
                        return False

                return True

        return False

    def random_position(self):
        # 0 = horizontal, 1 = vertical
        if self.direction == 0:
            return randint(0, BOARD_WIDTH - self.size), randint(0, BOARD_HEIGHT - 1)
        elif self.direction == 1:
            return randint(0, BOARD_WIDTH - 1), randint(0, BOARD_HEIGHT - self.size)

    def __init__(self, name, size, enemy):
        self.name = name
        self.size = size
        self.damage_taken = 0
        self.positions = []

        if enemy:
            # 0 = horizontal, 1 = vertical
            self.direction = randint(0, 1)

            while True:
                (x_coord, y_coord) = self.random_position()

                if self.check_ship_position(x_coord, y_coord, enemy):
                    # 0 = horizontal, 1 = vertical
                    if self.direction == 0:
                        for i in range(self.size):
                            self.positions.append([x_coord + i, y_coord])
                            enemy_ship_board[y_coord][x_coord + i] = 1
                    elif self.direction == 1:
                        for i in range(self.size):
                            self.positions.append([x_coord, y_coord + i])
                            enemy_ship_board[y_coord + i][x_coord] = 1
                    break

        else:
            # 0 = horizontal, 1 = vertical
            print_board(player_ship_board, True)

            while True:
                temp_direction = input(f"Choose a direction for your {self.name} ({self.size} units long) - Horizontal or Vertical: ")

                if temp_direction.casefold() == "horizontal":
                    self.direction = 0
                elif temp_direction.casefold() == "vertical":
                    self.direction = 1
                else:
                    print("Invalid direction")
                    continue

                temp_coords = input(f"Enter the starting coordinates for your {self.name} ({self.size} units long) (e.g., 2, 2 or (2, 2)): ")

                try:
                    temp_coords = temp_coords.replace("(", "").replace(")", "").strip()
                    x_coord, y_coord = map(int, temp_coords.split(","))

                    if self.check_ship_position(x_coord, y_coord, False):
                        if self.direction == 0:
                            for i in range(self.size):
                                self.positions.append([x_coord + i, y_coord])
                                player_ship_board[y_coord][x_coord + i] = 1
                        elif self.direction == 1:
                            for i in range(self.size):
                                self.positions.append([x_coord, y_coord + i])
                                player_ship_board[y_coord + i][x_coord] = 1
                        break
                    else:
                        print("Invalid coordinate! The coordinate you entered either overlaps with another ship or is outside the bounds of the game")

                except ValueError:
                    print("Invalid format! Please enter coordinates in the format 'x, y' or '(x, y)'.")

def print_board(board, coordinate=False):
    if coordinate:
        # Print x-axis labels
        print("   " + " ".join(f"{x:2}" for x in range(len(board[0]))))

    for y, row in enumerate(board):
        if coordinate:
            # Print y-axis labels along with the row
            print(f"{y:2} " + " ".join(f"{cell:2}" for cell in row))
        else:
            # Print the row without y-axis labels
            print(" ".join(f"{cell:2}" for cell in row))
    print("\n")

def initialize_game():
    global enemy_ship_board, enemy_hit_board, player_ship_board, player_hit_board

    enemy_ship_board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    enemy_hit_board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    player_ship_board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    player_hit_board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]

    enemy_ships.extend([Ship("Carrier", 5, True), Ship("Battleship", 4, True), Ship("Destroyer", 3, True), Ship("Submarine", 3, True), Ship("Patrol Boat", 2, True)])
    player_ships.extend([Ship("Carrier", 5, False), Ship("Battleship", 4, False), Ship("Destroyer", 3, False), Ship("Submarine", 3, False), Ship("Patrol Boat", 2, False)])

    print_board(player_ship_board)
    print("This is your final board.")
    print_board(enemy_ship_board)

def main():
    initialize_game()

    pygame.init()
    screen = pygame.display.set_mode((BOARD_WIDTH * CELL_SIZE * 2 + MARGIN * 3, BOARD_HEIGHT * CELL_SIZE + 100))
    pygame.display.set_caption("Battleship")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    ai_target_mode = False
    ai_target_hits = []

    global running

    running = True

    while running:
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                rect = pygame.Rect(
                    MARGIN + x * CELL_SIZE,
                    30 + MARGIN * 2 + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE)
                if enemy_hit_board[y][x] == " H":
                    color = RED  # Enemy ship hit
                elif enemy_hit_board[y][x] == " M":
                    color = GRAY  # Missed shot
                elif enemy_hit_board[y][x] == " X":
                    color = MAROON  # Missed shot
                else:
                    color = BLUE  # Water (ships are hidden)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, WHITE, rect, 1)  # Border

            # Draw the computer board
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                rect = pygame.Rect(
                    MARGIN * 2 + BOARD_WIDTH * CELL_SIZE + x * CELL_SIZE,
                    30 + MARGIN * 2 + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                )
                if player_ship_board[y][x] == 1:
                    color = GREEN
                else:
                    color = BLUE

                if player_hit_board[y][x] == " H":
                    color = RED
                elif player_hit_board[y][x] == " M":
                    color = GRAY
                elif player_hit_board[y][x] == " X":
                    color = MAROON

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, WHITE, rect, 1)  # Border

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                coords = get_grid_coordinates(pos)
                if coords:
                    x_coord, y_coord = coords

                    if enemy_hit_board[y_coord][x_coord] == 0:
                        if enemy_ship_board[y_coord][x_coord] == 1:
                            enemy_hit_board[y_coord][x_coord] = " H"
                            print("You hit their ship!")

                            for ship in enemy_ships:
                                if [x_coord, y_coord] in ship.positions:
                                    ship.damage_taken += 1

                                    print(f"Damage taken: {ship.damage_taken}, Ship Size: {ship.size}")

                                    if ship.damage_taken == ship.size:
                                        for coord in ship.positions:
                                            enemy_hit_board[coord[1]][coord[0]] = " X"

                                        print("You sunk their ship!")
                                        enemy_ships.remove(ship)
                                    break

                        else:
                            print("You missed their ship!")
                            enemy_hit_board[y_coord][x_coord] = " M"
                    else:
                        print("You attacked this spot already. Try another spot.")
                        continue

                    if not enemy_ships:
                        print("You win!")
                        running = False
                        break

                    print("\n Computer's turn:")
                    if ai_target_mode and ai_target_hits:
                        x_coord, y_coord = ai_target_hits.pop(0)
                    else:
                        while True:
                            x_coord = randint(0, BOARD_WIDTH - 1)
                            y_coord = randint(0, BOARD_HEIGHT - 1)
                            if player_hit_board[y_coord][x_coord] == 0:
                                break

                    if player_ship_board[y_coord][x_coord] == 1:
                        player_hit_board[y_coord][x_coord] = " H"
                        print(f"Computer hit your ship at ({x_coord}, {y_coord})!")

                        ai_target_mode = True
                        if x_coord > 0 and player_hit_board[y_coord][x_coord - 1] == 0:
                            ai_target_hits.append((x_coord - 1, y_coord))
                        if x_coord < BOARD_WIDTH - 1 and player_hit_board[y_coord][x_coord + 1] == 0:
                            ai_target_hits.append((x_coord + 1, y_coord))
                        if y_coord > 0 and player_hit_board[y_coord - 1][x_coord] == 0:
                            ai_target_hits.append((x_coord, y_coord - 1))
                        if y_coord < BOARD_HEIGHT - 1 and player_hit_board[y_coord + 1][x_coord] == 0:
                            ai_target_hits.append((x_coord, y_coord + 1))

                        for ship in player_ships:
                            if [x_coord, y_coord] in ship.positions:
                                ship.damage_taken += 1

                                print(f"Damage taken: {ship.damage_taken}, Ship Size: {ship.size}")

                                if ship.damage_taken == ship.size:
                                    for coord in ship.positions:
                                        player_hit_board[coord[1]][coord[0]] = " X"
                                    print("Computer sunk your ship!")
                                    player_ships.remove(ship)
                                    ai_target_mode = False
                                break
                    else:
                        player_hit_board[y_coord][x_coord] = " M"
                        print(f"Computer missed at ({x_coord}, {y_coord}).")

                    if not player_ships:
                        print("You lose!")
                        running = False
                        break

                    print("\n Your Turn")

main()