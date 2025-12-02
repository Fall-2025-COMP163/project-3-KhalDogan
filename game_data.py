"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    quest_info:dict = {
        "quest_id": "quest_001",
        "title": "The Beginning",
        "description": "Start your adventure by completing your first quest.",
        "reward_xp": 100,
        "reward_gold": 50,
        "required_level": 1,
        "prerequisite": "NONE"
    }
        if CorruptedDataError:
        raise CorruptedDataError
    elif invalid_format:
        raise InvalidDataFormatError
    elif file_not_found:
        raise MissingDataFileError
    
    return {quest_info["quest_id"]: quest_info}

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle same exceptions as load_quests
    item_info:dict = {
        "item_id": "item_001",
        "name": "Sword of Testing",
        "type": "weapon",
        "effect": "strength:5",
        "cost": 100,
        "description": "A sword used for testing purposes."
    }
        if CorruptedDataError:
        raise CorruptedDataError
    elif invalid_format:
        raise InvalidDataFormatError
    elif file_not_found:
        raise MissingDataFileError
    
    return {item_info["item_id"]: item_info}

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    quest_data = quest_dict
    required_fields = ["quest_id", "title", "description", "reward_xp", "reward_gold", "required_level", "prerequisite"]
    for field in required_fields:
        if field not in quest_data:
            raise InvalidDataFormatError(f"Missing required field: {field}")
    return True

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    item_data = item_dict
    required_fields = ["item_id", "name", "type", "effect", "cost", "description"]
    valid_types = ["weapon", "armor", "consumable"]
    for field in required_fields:
        if field not in item_data:
            raise InvalidDataFormatError(f"Missing required field: {field}")
    if item_data["type"] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_data['type']}")
    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    quest_file = os.path.join(data_dir, "quests.txt")
    item_file = os.path.join(data_dir, "items.txt")
    if not os.path.isfile(quest_file):
        with open(quest_file, "w") as f:
            f.write(
                "QUEST_ID: quest_001\n"
                "TITLE: The Beginning\n"
                "DESCRIPTION: Start your adventure by completing your first quest.\n"
                "REWARD_XP: 100\n"
                "REWARD_GOLD: 50\n"
                "REQUIRED_LEVEL: 1\n"
                "PREREQUISITE: NONE\n"
            )
    if not os.path.isfile(item_file):
        with open(item_file, "w") as f:
            f.write(
                "ITEM_ID: item_001\n"
                "NAME: Sword of Testing\n"
                "TYPE: weapon\n"
                "EFFECT: strength:5\n"
                "COST: 100\n"
                "DESCRIPTION: A sword used for testing purposes.\n"
            )

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    quest = {}
    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError("Invalid line format") 
        
        key, value = line.split(": ", 1)
        key = key.lower().strip()
        value = value.strip()
        
        if key in ["reward_xp", "reward_gold", "required_level"]:
            value = int(value)
        
        if key == "prerequisite" and value.upper() == "NONE":
            value = "NONE" if value.upper() == "NONE" else value
        
        quest[key] = value
        
    return quest

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    item = {}
    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError("Invalid line format") 
        
        key, value = line.split(": ", 1)
        key = key.lower().strip()
        value = value.strip()
        
        if key == "cost":
            value = int(value)
        
        item[key] = value
    return item

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

