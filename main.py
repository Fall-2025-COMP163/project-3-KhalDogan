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
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice
    print("Main Menu: \n 1. New Game \n 2. Load Game \n 3. Exit")
    choice = int(input("Choose your path Noob! (1-3): "))
    return choice

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop
    print("Starting a new game...")
    name = input("Enter your character's name: ")
    char_class = input("Enter your character's class (Warrior, Mage, Rogue, Cleric): ")
    try:
        current_character = character_manager.create_character(name, char_class)
        character_manager.save_character(current_character)
        print(f"Character {name} the {char_class} created successfully!")
        game_loop()
    except InvalidCharacterClassError as e:
        print(f"Error creating character: {e}")
    return

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop
    print("Loading a saved game...")
    saved_characters = character_manager.list_saved_characters()
    if not saved_characters:
        print("First time? Don't be shy.")
    else
        print("Saved Characters:")
        for idx, char_name in enumerate(saved_characters, 1):
            print(f"{idx}. {char_name}")
        choice = int(input("Select a character to load (number): "))
        try:
            selected_name = saved_characters[choice - 1]
            current_character = character_manager.load_character(selected_name)
            print(f"Character {selected_name} loaded successfully!")
            game_loop()
        except (CharacterNotFoundError, SaveFileCorruptedError) as e:
            print(f"Error loading character: {e}")
    return

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action
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
            print("Game saved. Exiting to main menu.")
            game_running = False
        else:
            print("Invalid choice. Please select a valid option.")
        
        # Save game state after each action
        if game_running:
            save_game()
        return

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    # TODO: Implement game menu
    print("\n=== Game Menu ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")
    choice = int(input("Choose an action (1-6): "))
    return choice

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler
    print("\n=== Character Stats ===")
    print(f"Name: {current_character['name']}")
    print(f"Class: {current_character['class']}")
    print(f"Level: {current_character['level']}")
    print(f"Health: {current_character['health']}/{current_character['max_health']}")
    print(f"Gold: {current_character['gold']}")
    print("Stats:")
    for stat, value in current_character['stats'].items():
        print(f"  {stat.capitalize()}: {value}")
    print("Active Quests:")
    active_quests = quest_handler.get_active_quests(current_character, all_quests)
    for quest in active_quests:
        print(f"  - {quest['name']}: {quest['description']}")
    return 

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system
    print("\n=== Inventory ===")
    inventory_system.display_inventory(current_character, all_items)
    return

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler
    print("\n=== Quest Menu ===")
    print("1. View Active Quests")
    print("2. View Available Quests")
    print("3. View Completed Quests")
    print("4. Accept Quest")
    print("5. Abandon Quest")
    print("6. Complete Quest (for testing)")
    print("7. Back")
    choice = int(input("Choose an option (1-7): "))
    if choice == 1:
        active_quests = quest_handler.get_active_quests(current_character, all_quests)
        print("\nActive Quests:")
        for quest in active_quests:
            print(f"  - {quest['name']}: {quest['description']}")
    elif choice == 2:
        available_quests = quest_handler.get_available_quests(current_character, all_quests)
        print("\nAvailable Quests:")
        for quest in available_quests:
            print(f"  - {quest['name']}: {quest['description']}")
    elif choice == 3:
        completed_quests = quest_handler.get_completed_quests(current_character, all_quests)
        print("\nCompleted Quests:")
        for quest in completed_quests:
            print(f"  - {quest['name']}: {quest['description']}")
    elif choice == 4:
        quest_id = input("Enter the Quest ID to accept: ")
        try:
            quest_handler.accept_quest(current_character, quest_id, all_quests)
            print(f"Quest {quest_id} accepted!")
        except (QuestNotFoundError, QuestPrerequisiteNotMetError) as e:
            print(f"Error accepting quest: {e}")
    elif choice == 5:
        quest_id = input("Enter the Quest ID to abandon: ")
        try:
            quest_handler.abandon_quest(current_character, quest_id)
            print(f"Quest {quest_id} abandoned.")
        except QuestNotFoundError as e:
            print(f"Error abandoning quest: {e}")
    elif choice == 6:
        quest_id = input("Enter the Quest ID to complete (for testing): ")
        try:
            quest_handler.complete_quest(current_character, quest_id, all_quests)
            print(f"Quest {quest_id} completed!")
        except (QuestNotFoundError, QuestNotCompleteError) as e:
            print(f"Error completing quest: {e}")
    elif choice == 7:
        return

def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions
    print("\nExploring the world...")
    enemy = combat_system.generate_random_enemy(current_character['level'])
    try:
        result = combat_system.simple_battle(current_character, enemy)
        if result == 'victory':
            print("You defeated the enemy!")
        elif result == 'defeat':
            print("You were defeated...")
            handle_character_death()
    except CombatError as e:
        print(f"Error during combat: {e}")
    return

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    print("\n=== Shop ===")
    print("Available Items:")
    for item_id, item in all_items.items():
        print(f"{item_id}: {item['name']} - {item['cost']} gold")
    print(f"Your Gold: {current_character['gold']}")
    print("1. Buy Item")
    print("2. Sell Item")
    print("3. Back")
    choice = int(input("Choose an option (1-3): "))
    if choice == 1:
        item_id = input("Enter the Item ID to buy: ")
        try:
            inventory_system.buy_item(current_character, item_id, all_items)
            print(f"Item {item_id} purchased!")
        except (ItemNotFoundError, InsufficientGoldError, InventoryFullError) as e:
            print(f"Error buying item: {e}")
    elif choice == 2:
        item_id = input("Enter the Item ID to sell: ")
        try:
            inventory_system.sell_item(current_character, item_id, all_items)
            print(f"Item {item_id} sold!")
        except ItemNotFoundError as e:
            print(f"Error selling item: {e}")
    elif choice == 3:
        return

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    try:
        character_manager.save_character(current_character)
        print("Game saved successfully.")
    except Exception as e:
        print(f"Error saving game: {e}")
    return

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()
    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except MissingDataFileError:
        print("Data files missing. Creating default data files...")
        game_data.create_default_data_files()
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        raise

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False
    print("\nYou have fallen in battle...")
    print("1. Revive (costs 50 gold)")
    print("2. Quit to Main Menu")
    choice = int(input("Choose an option (1-2): "))
    if choice == 1:
        try:
            character_manager.revive_character(current_character, cost=50)
            print("You have been revived!")
        except InsufficientGoldError as e:
            print(f"Cannot revive: {e}")
            game_running = False
    elif choice == 2:
        game_running = False
    return

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

