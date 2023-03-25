import random
import math

MAX_BLOCKS_PER_VIAL = 5
NUM_PADDING_VIALS = 2
NUM_ROWS_VIALS = 2
MAX_EMPTY_VIALS = 2
MYSTERY_LEVEL_PERCENTAGE = .30
COLORS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")

class Level:
    def __init__(self, level_number):
        self.vials = []
        self.level_number = level_number
        self.is_mystery_level = self.get_if_mystery_level_random()
        self.generate_random_level()

    def get_if_mystery_level_random(self):
        """Player must have at least beaten level 5; Only odd levels can be mystery"""
        return (self.level_number > 5 and self.level_number % 2 and random.random() <= MYSTERY_LEVEL_PERCENTAGE)

    def generate_random_level(self):
        num_vials = math.ceil(math.log2(self.level_number)) + NUM_PADDING_VIALS
        valid_colors = COLORS[:num_vials] * MAX_BLOCKS_PER_VIAL
        random.shuffle(valid_colors)

        for _ in range(num_vials):
            self.add_vial()
            self.vials[-1].fill_vial_random(valid_colors, self.is_mystery_level)
        for _ in range(MAX_EMPTY_VIALS):
            self.vials.append(Vial())

    def check_win(self) -> bool:
        for vial in self.vials:
            if not vial.check_solved():
                return False
        return True

    def add_vial(self, num_blocks=MAX_BLOCKS_PER_VIAL):
        v = Vial(num_blocks)
        self.vials.append(v)

    def display_vials(self):
        """Prints blocks line by line MAX_BLOCKS_PER_VIAL number of times
            split into NUM_ROWS_VIALS number of rows"""
        
        def get_bounds(row):
            left_bound = row * (len(self.vials) // NUM_ROWS_VIALS + 1)
            right_bound = (row+1) * (len(self.vials) // NUM_ROWS_VIALS + 1)
            if row == NUM_ROWS_VIALS-1:
                right_bound = len(self.vials)
            return left_bound, right_bound

        def determine_top_block_content(vial):
            try:
                current_block = vial.blocks[MAX_BLOCKS_PER_VIAL-1 - i]
                if self.is_mystery_level and current_block != vial.blocks[-1] and not current_block.is_revealed:
                    content = "?"
                else:
                    content = current_block.color
            except IndexError:
                content = ' '
            return content

        for row in range(NUM_ROWS_VIALS):
            print("")
            bounds = get_bounds(row)
            vials_in_current_row = self.vials[bounds[0]:bounds[1]]
            if not vials_in_current_row:
                continue

            for i in range(MAX_BLOCKS_PER_VIAL + 2):
                line = ""

                # The bottom (closing) vial line
                if i == MAX_BLOCKS_PER_VIAL:
                    line += "---   " * len(vials_in_current_row)

                # The vial number label below
                elif i == MAX_BLOCKS_PER_VIAL+1:
                    for vial in vials_in_current_row:
                        line += f"{ self.vials.index(vial)+1 :2}    "

                else:
                    for vial in vials_in_current_row:
                        line += f"|{determine_top_block_content(vial)}|   "

                print(line)
            
class Vial:
    """Stack data structure containing stacked WaterBlock objects"""
    def __init__(self, max_blocks_per_vial = MAX_BLOCKS_PER_VIAL):
        self.blocks = []
        self.max_blocks_per_vial = max_blocks_per_vial

    def check_solved(self) -> bool:
        """Checks if vial is empty, or full with same color"""

        if not self.blocks:
            return True

        if not self.is_full():
            return False

        for block in self.blocks:
            if block.color != self.blocks[-1].color or not block.is_revealed:
                return False
        return True

    def is_full(self):
        return len(self.blocks) == self.max_blocks_per_vial

    def is_empty(self):
        return len(self.blocks) == 0

    def fill_vial_random(self, color_choices, is_mystery):
        for i in range(self.max_blocks_per_vial):
            self.blocks.append(WaterBlock(color_choices.pop(), not is_mystery))

    def pour_onto(self, bottom):
        w = self.blocks.pop()
        w.is_revealed = True
        bottom.blocks.append(w)

        if self.blocks and is_valid_move(self, bottom) and self.blocks[-1].is_revealed:
            self.pour_onto(bottom)
        if self.blocks:
            self.blocks[-1].is_revealed = True

        self.check_solved()
        bottom.check_solved()


class WaterBlock:
    """Objects that can only be stacked onto same colors"""
    def __init__(self, color, is_revealed):
        self.color = color
        self.is_revealed = is_revealed

class Player:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.current_level = 1
        self.avg_time_per_level = 0

def is_valid_move(top, bottom) -> bool:
    if top.blocks:
        if not bottom.is_full():
            if bottom.is_empty() or (bottom.blocks[-1].color == top.blocks[-1].color):
                return True
    return False
