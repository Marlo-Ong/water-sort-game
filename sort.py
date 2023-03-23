import random

MIN_NUM_VIALS = 5
MAX_NUM_VIALS = 10
MAX_BLOCKS = 4
MAX_EMPTY_VIALS = 2
colors = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

class Level:
    def __init__(self):
        self.vials = []
        self.difficulty = "Easy"
        self.is_mystery_level = False
        self.generate_random_level()

    def generate_random_level(self):
        """Generates random number of vials
            containing random valid water blocks.
            An empty vial is included at the end"""

        num_vials = random.randint(MIN_NUM_VIALS, MAX_NUM_VIALS)
        valid_colors = colors[:num_vials]*MAX_BLOCKS
        random.shuffle(valid_colors)

        for _ in range(num_vials):
            v = Vial()
            v.generate_random_vial(valid_colors)
            self.vials.append(v)
        for _ in range(MAX_EMPTY_VIALS):
            self.vials.append(Vial())

    def check_win(self) -> bool:
        for vial in self.vials:
            if not vial.check_solved():
                return False
        return True

    def display_vials(self):
        for k in range(2):
            print("")
            lined_vials = self.vials[:len(self.vials)//2]

            if k == 1:
                lined_vials = self.vials[len(self.vials)//2:]

            for i in range(6):
                line = ""

                if i == 4:
                    line += "---   "*len(lined_vials)

                elif i == 5:
                    for j in range(len(lined_vials)):
                        line += f"{j+1+k*len(self.vials)//2:2}    "

                else:
                    for vial in lined_vials:
                        try:
                            e = vial.blocks[MAX_BLOCKS-i-1].color
                        except IndexError:
                            e = ' '
                        line += f"|{e}|   "
                print(line)
            
class Vial:
    """Stack data structure containing stacked WaterBlock objects"""
    def __init__(self):
        self.blocks = []
        self.max_blocks = MAX_BLOCKS

    def check_solved(self) -> bool:
        """Checks if vial is empty, or full with same color"""

        if not self.blocks:
            return True

        if not self.is_full():
            return False

        for block in self.blocks:
            if block.color != self.blocks[-1].color:
                return False
        return True

    def is_full(self):
        return len(self.blocks) == self.max_blocks

    def is_empty(self):
        return len(self.blocks) == 0

    def generate_random_vial(self, color_choices):
        for _ in range(self.max_blocks):
            self.blocks.append(WaterBlock(color_choices.pop()))

    def pour_onto(self, bottom):
        w = self.blocks.pop()
        bottom.blocks.append(w)

        if self.blocks and is_valid_move(self, bottom):
            self.pour_onto(bottom)

        self.check_solved()
        bottom.check_solved()

class WaterBlock:
    """Objects that can only be stacked onto same colors"""
    def __init__(self, color):
        self.color = color

def is_valid_move(top, bottom) -> bool:
    if top.blocks:
        if not bottom.is_full():
            if bottom.is_empty() or (bottom.blocks[-1].color == top.blocks[-1].color):
                return True
    return False

while __name__ == "__main__":
    print('Water Sort Terminal Game!\n\
    How to Play: Match the letters so that each vial as the same letter.\n\
    You cannot "pour" a letter into a different letter or into a full vial!\n\n\
    Input "e e" to exit or "g g" to give up.\n')

    def main():
        e = Level()

        while not e.check_win():
            e.display_vials()
            try:
                top, bottom = input("\n Input the numbered vial to pour from, then the vial to pour to. (Ex: 1 3): ").split()
                if top == "e":
                    return 1
                if top == "g":
                    print("\nGG! New level starting...\n")
                    return 0
                
                top_vial = e.vials[int(top)-1]
                bottom_vial = e.vials[int(bottom)-1]
            except IndexError:
                print("\nThat vial does not exist!")
                continue
            except ValueError:
                print("Invalid input")
                continue  

            if is_valid_move(top_vial, bottom_vial):
                top_vial.pour_onto(bottom_vial)
            else:
                print("Invalid move.")

        exit = input("\nYou win! Input any key to continue, or 'e' to exit. ")
        if exit.lower() == 'e':
            return 1

    exit = main()
    if exit:
        print("Thanks for playing!")
        break
