"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """Display main menu and get player choice"""
    while True:
        print("\nMain Menu:")
        print(" 1. New Game")
        print(" 2. Load Game")
        print(" 3. Exit")

        choice = input("Choose your path (1-3): ")

        if choice.isdigit() and choice in {"1", "2", "3"}:
            return int(choice)
        print("Invalid input. Try again.")


def new_game():
    """Start a new game and create a character"""
    global current_character

    print("\nStarting a new game...")

    name = input("Enter your character's name: ")
    char_class = input("Enter your class (Warrior, Mage, Rogue, Cleric): ")

    try:
        current_character = character_manager.create_character(name, char_class)
        character_manager.save_character(current_character)
        print(f"Character {name} the {char_class} created successfully!")
        game_loop()
    except InvalidCharacterClassError as e:
        print(f"Error creating character: {e}")


def load_game():
    """Load a saved character"""
    global current_character

    print("\nLoading a saved game...")

    saved_characters = character_manager.list_saved_characters()
    if not saved_characters:
        print("No saved characters found.")
        return

    print("\nSaved Characters:")
    for idx, char_name in enumerate(saved_characters, 1):
        print(f"{idx}. {char_name}")

    while True:
        choice = input("Select a character to load (number): ")
        if choice.isdigit() and 1 <= int(choice) <= len(saved_characters):
            break
        print("Invalid selection.")

    try:
        selected_name = saved_characters[int(choice) - 1]
        current_character = character_manager.load_character(selected_name)
        print(f"Character {selected_name} loaded successfully!")
        game_loop()
    except (CharacterNotFoundError, SaveFileCorruptedError) as e:
        print(f"Error loading character: {e}")

# ============================================================================ 
# GAME LOOP
# ============================================================================

def game_loop():
    """Primary loop for in-game actions"""
    global game_running, current_character
    game_running = True

    while game_running:
        choice = game_menu()

        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Exiting to main menu...")
            game_running = False

        # Save after each action unless quitting
        if game_running:
            save_game()


def game_menu():
    """Display game action menu"""
    while True:
        print("\n=== Game Menu ===")
        print("1. View Character Stats")
        print("2. View Inventory")
        print("3. Quest Menu")
        print("4. Explore (Find Battles)")
        print("5. Shop")
        print("6. Save and Quit")

        choice = input("Choose an action (1-6): ")

        if choice.isdigit() and choice in {"1", "2", "3", "4", "5", "6"}:
            return int(choice)
        print("Invalid choice.")


# ============================================================================ 
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display current character's stats"""
    c = current_character

    print("\n=== Character Stats ===")
    print(f"Name: {c['name']}")
    print(f"Class: {c['class']}")
    print(f"Level: {c['level']}")
    print(f"Health: {c['health']}/{c['max_health']}")
    print(f"Gold: {c['gold']}")

    print("\nStats:")
    for stat, value in c["stats"].items():
        print(f"  {stat.capitalize()}: {value}")

    print("\nActive Quests:")
    active = quest_handler.get_active_quests(current_character, all_quests)
    for q in active:
        print(f"  - {q['name']}: {q['description']}")


def view_inventory():
    """Display and manage inventory"""
    print("\n=== Inventory ===")
    inventory_system.display_inventory(current_character, all_items)


def quest_menu():
    """Quest management options"""
    global current_character

    print("\n=== Quest Menu ===")
    print("1. View Active Quests")
    print("2. View Available Quests")
    print("3. View Completed Quests")
    print("4. Accept Quest")
    print("5. Abandon Quest")
    print("6. Complete Quest (TESTING)")
    print("7. Back")

    choice = input("Choose (1-7): ")

    if choice == "1":
        print("\nActive Quests:")
        for q in quest_handler.get_active_quests(current_character, all_quests):
            print(f"- {q['name']}: {q['description']}")

    elif choice == "2":
        print("\nAvailable Quests:")
        for q in quest_handler.get_available_quests(current_character, all_quests):
            print(f"- {q['name']}: {q['description']}")

    elif choice == "3":
        print("\nCompleted Quests:")
        for q in quest_handler.get_completed_quests(current_character, all_quests):
            print(f"- {q['name']}")

    elif choice == "4":
        quest_id = input("Enter Quest ID: ")
        try:
            quest_handler.accept_quest(current_character, quest_id, all_quests)
            print("Quest accepted!")
        except (QuestNotFoundError, QuestPrerequisiteNotMetError) as e:
            print(f"Error: {e}")

    elif choice == "5":
        quest_id = input("Enter Quest ID: ")
        try:
            quest_handler.abandon_quest(current_character, quest_id)
            print("Quest abandoned.")
        except QuestNotFoundError as e:
            print(f"Error: {e}")

    elif choice == "6":
        quest_id = input("Enter Quest ID: ")
        try:
            quest_handler.complete_quest(current_character, quest_id, all_quests)
            print("Quest completed!")
        except (QuestNotFoundError, QuestNotCompleteError) as e:
            print(f"Error: {e}")

    elif choice == "7":
        return


def explore():
    """Trigger a random combat encounter"""
    print("\nExploring...")
    enemy = combat_system.generate_random_enemy(current_character["level"])

    try:
        result = combat_system.simple_battle(current_character, enemy)
        if result == "victory":
            print("Victory!")
        else:
            print("You were defeated...")
            handle_character_death()
    except CombatError as e:
        print(f"Combat Error: {e}")


def shop():
    """Buy and sell items"""
    print("\n=== Shop ===")

    print("Available Items:")
    for item_id, item in all_items.items():
        print(f"{item_id}: {item['name']} ({item['cost']} gold)")

    print(f"\nYour Gold: {current_character['gold']}")

    print("\n1. Buy Item")
    print("2. Sell Item")
    print("3. Back")

    choice = input("Choose (1-3): ")

    if choice == "1":
        item_id = input("Item ID to buy: ")
        try:
            inventory_system.buy_item(current_character, item_id, all_items)
            print("Item purchased!")
        except (ItemNotFoundError, InventoryFullError, InsufficientGoldError) as e:
            print(f"Error: {e}")

    elif choice == "2":
        item_id = input("Item ID to sell: ")
        try:
            inventory_system.sell_item(current_character, item_id, all_items)
            print("Item sold!")
        except ItemNotFoundError as e:
            print(f"Error: {e}")


# ============================================================================ 
# HELPERS
# ============================================================================

def save_game():
    try:
        character_manager.save_character(current_character)
        print("Game saved.")
    except Exception as e:
        print(f"Error saving: {e}")


def load_game_data():
    global all_quests, all_items

    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except MissingDataFileError:
        print("Missing data files. Creating defaults...")
        game_data.create_default_data_files()
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except InvalidDataFormatError as e:
        print(f"Invalid data format: {e}")
        raise


def handle_character_death():
    global game_running

    print("\n💀 You have fallen in battle 💀")
    print("1. Revive (50 gold)")
    print("2. Quit to main menu")

    choice = input("Choose (1-2): ")

    if choice == "1":
        try:
            character_manager.revive_character(current_character, cost=50)
            print("You have been revived!")
        except InsufficientGoldError as e:
            print(f"Cannot revive: {e}")
            game_running = False
    else:
        game_running = False


def display_welcome():
    print("=" * 50)
    print(" QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("Welcome, hero.")


# ============================================================================ 
# ENTRY POINT
# ============================================================================

def main():
    display_welcome()

    try:
        load_game_data()
        print("Game data loaded!")
    except InvalidDataFormatError:
        print("Data files corrupted. Fix them and try again.")
        return

    while True:
        choice = main_menu()
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("Thanks for playing Quest Chronicles!")
            break


if __name__ == "__main__":
    main()

