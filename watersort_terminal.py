import sort
import pickle

FILE_NAME = "sortdata.dat"

def main(player):
    current_level = sort.Level(player.current_level)

    while not current_level.check_win():
        print(f"\nLevel {player.current_level}")
        current_level.display_vials()
        try:
            top, bottom = input("\n Input the numbered vial to pour from, then the vial to pour to. (Ex: 1 3): ").split()
            
            # Update to Python 3.10 for match case
            if top == "e":
                return 1
            elif top == "g":
                print("\nGG! New level starting...\n")
                return 0
            elif top == "a":
                current_level.add_vial(1)
            else:
                top_vial = current_level.vials[int(top)-1]
                bottom_vial = current_level.vials[int(bottom)-1]
                if sort.is_valid_move(top_vial, bottom_vial):
                    top_vial.pour_onto(bottom_vial)
                else:
                    print("Invalid move.")

        except IndexError:
            print("\nThat vial does not exist!")
            continue
        except ValueError:
            print("Invalid input")
            continue  

    current_level.display_vials()
    player.current_level += 1
    exit = input("\nYou win! Input any key to continue, or 'e' to exit. ")
    if exit.lower() == 'e':
        return 1

def save_db(player_db):
    with open(FILE_NAME, 'wb') as save_file:
        pickle.dump(player_db, save_file)

def load_db():
    try:
        with open(FILE_NAME, 'rb') as save_file:
            player_db = pickle.load(save_file)
            return player_db  

    except FileNotFoundError:
        pass
    except EOFError:
        pass
    except ValueError:
        print('\nSome data could not be loaded.')
    except TypeError:
        pass

def load_player(db):
    while True:
        try:
            give_name = input("\nEnter your username: ")
            give_pass = input("Enter your password: ")
            if db[give_name].password != give_pass:
                print("\nThe password is incorrect.")
            else:
                break
        except KeyError:
            db[give_name] = sort.Player(give_name, give_pass)
            print("\nWe did not find an account with that username.")
            print("An account was made for you using your username and password.")
            break
    return db[give_name]

if __name__ == "__main__":
    exit = 0

    print('Water Sort Terminal Game!\n\
    How to Play: Match the letters so that each vial as the same letter.\n\
    You cannot "pour" a letter into a different letter or into a full vial!\n\n\
    Input "e e" to exit or "g g" to give up.\n')

    all_players = load_db()
    if not all_players:
        all_players = {}
    current_player = load_player(all_players)

    while not exit:
        exit = main(current_player)

    save_db(all_players)
    print("Thanks for playing!")