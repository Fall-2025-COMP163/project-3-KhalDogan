COMP 163: Project 3 – Quest Chronicles

AI Usage: Free Use (with explanation requirement)

Overview

This project implements a modular RPG adventure game focused on exceptions, modules, data handling, and game logic structure.
The game includes characters, combat, quests, inventory management, and data loading/validation.

Getting Started
Step 1: Accept Assignment

Click the assignment link on Blackboard

Accept the assignment → creates your personal GitHub repository

Clone the repository locally:

git clone [your-repo-url]
cd quest_chronicles

Step 2: Understand the Project Structure

Your project includes the following modules:

quest_chronicles/
├── main.py                     # Game launcher (STUDENT IMPLEMENTS)
├── character_manager.py        # Character creation + levelling (STUDENT IMPLEMENTS)
├── inventory_system.py         # Items + equipment (STUDENT IMPLEMENTS)
├── quest_handler.py            # Quest acceptance, completion, tracking (STUDENT IMPLEMENTS)
├── combat_system.py            # Turn-based combat mechanics (STUDENT IMPLEMENTS)
├── game_data.py                # Data loading + validation (STUDENT IMPLEMENTS)
├── custom_exceptions.py        # All custom exception classes (PROVIDED)
├── data/
│   ├── quests.txt              # Quest definitions (PROVIDED or auto-generated)
│   ├── items.txt               # Item database (PROVIDED or auto-generated)
│   └── save_games/             # Save files folder
├── tests/
│   ├── test_module_structure.py
│   ├── test_exception_handling.py
│   └── test_game_integration.py
└── README.md

Step 3: Development Workflow
# Work on one module at a time
# Run tests frequently

git add .
git commit -m "Implement quest_handler"
git push

# Check GitHub test runner for pass/fail results

Module Architecture (Required for README)

This project is organized using Python modules, each responsible for a core game system.

Module	Purpose	Key Functions
main.py	Runs game & menus	start_game(), menu loops
character_manager.py	Creates & manages characters	create_character(), level_up()
inventory_system.py	Handles item storage	add_item(), equip_item()
quest_handler.py	Quest logic	accept_quest(), complete_quest()
combat_system.py	Battle calculations	attack(), take_turn(), resolve_fight()
game_data.py	Loads + validates items/quests	load_items(), load_quests()
custom_exceptions.py	Error handling	QuestNotFoundError, InventoryError, etc.
Exception Strategy (Required for README)

Each module raises exceptions to prevent invalid game states.

Exception	Trigger
QuestNotFoundError	Quest ID doesn't exist
QuestRequirementsNotMetError	Missing prerequisite quest
QuestAlreadyCompletedError	Trying to re-accept a finished quest
QuestNotActiveError	Completing or abandoning a non-active quest
InsufficientLevelError	Character level too low for a quest
ItemNotFoundError	Using or equipping an unknown item
InvalidDataFormatError	Data files missing required fields
CharacterCreationError	Unsupported class or invalid stats

All modules use these exceptions to ensure the game does not crash and invalid states are safely blocked.

Design Choices (Required for README)

You will fill these in based on your custom game design.
Here are template examples:

- Characters start with higher base HP for better early-game balance.
- Quests scale XP rewards based on required level.
- Inventory allows unlimited item storage for simplicity.
- Combat includes critical hits for more dynamic battles.
- Rogue class specializes in speed-based dodge mechanics.
- Orc enemies have higher strength but lower accuracy.


Replace or expand these with your actual decisions.

How to Play (Required for README)
Run the Game
python main.py

Basic Gameplay Loop

Choose a character class

View and accept available quests

Fight enemies in combat encounters

Gain XP and gold

Purchase or find items

Complete quests to progress the storyline

Automated Testing & Validation (60 Points)

Your repository includes automated GitHub tests that verify:

Modules exist with required functions

Exceptions are properly raised

Game systems integrate correctly

Data loading is valid

You must push commits to run these tests.

Interview Component (40 Points)

You must explain:

How your modules interact

Why you chose your game design

How your exception system works

What customizations you added

Creativity earns bonus points.

AI Usage (Required Statement)

Example (replace with your details):

AI Usage:
ChatGPT was used to generate README formatting and assist in code documentation.
All logic, debugging, and implementation decisions were made by me.

Protected Files Warning

Do not modify any test files.
Tampering triggers academic integrity violations and automatic failure.

You may view tests to understand expected behavior, but you must not edit them.