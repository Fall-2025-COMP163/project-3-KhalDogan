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
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest data file not found: {filename}")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            raw = f.read()
    except OSError as e:
        # Permission denied, unreadable, etc.
        raise CorruptedDataError(f"Could not read quest data file: {filename}") from e

    # Split into blocks separated by blank lines
    blocks = []
    current = []
    for line in raw.splitlines():
        if line.strip() == "":
            if current:
                blocks.append(current)
                current = []
        else:
            current.append(line.rstrip("\n"))
    if current:
        blocks.append(current)

    quests = {}
    for idx, block in enumerate(blocks, start=1):
        try:
            quest = parse_quest_block(block)
        except InvalidDataFormatError as e:
            raise InvalidDataFormatError(f"Error parsing quest block #{idx}: {e}") from e

        # Validate parsed quest structure
        try:
            validate_quest_data(quest)
        except InvalidDataFormatError as e:
            raise InvalidDataFormatError(f"Invalid quest data in block #{idx}: {e}") from e

        quest_id = quest.get("quest_id")
        if quest_id in quests:
            raise InvalidDataFormatError(f"Duplicate quest_id '{quest_id}' in file '{filename}'.")
        quests[quest_id] = quest

    return quests

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
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item data file not found: {filename}")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            raw = f.read()
    except OSError as e:
        raise CorruptedDataError(f"Could not read item data file: {filename}") from e

    # Split into blocks separated by blank lines
    blocks = []
    current = []
    for line in raw.splitlines():
        if line.strip() == "":
            if current:
                blocks.append(current)
                current = []
        else:
            current.append(line.rstrip("\n"))
    if current:
        blocks.append(current)

    items = {}
    for idx, block in enumerate(blocks, start=1):
        try:
            item = parse_item_block(block)
        except InvalidDataFormatError as e:
            raise InvalidDataFormatError(f"Error parsing item block #{idx}: {e}") from e

        # Validate parsed item structure
        try:
            validate_item_data(item)
        except InvalidDataFormatError as e:
            raise InvalidDataFormatError(f"Invalid item data in block #{idx}: {e}") from e

        item_id = item.get("item_id")
        if item_id in items:
            raise InvalidDataFormatError(f"Duplicate item_id '{item_id}' in file '{filename}'.")
        items[item_id] = item

    return items

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
    if not isinstance(quest_dict, dict):
        raise InvalidDataFormatError("Quest data must be a dictionary.")

    required_fields = [
        "quest_id", "title", "description",
        "reward_xp", "reward_gold", "required_level", "prerequisite"
    ]
    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing required field: {field}")

    # Check numeric fields
    for num_field in ("reward_xp", "reward_gold", "required_level"):
        value = quest_dict.get(num_field)
        if not isinstance(value, int):
            raise InvalidDataFormatError(f"Field '{num_field}' must be an integer (got {type(value).__name__}).")

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
    if not isinstance(item_dict, dict):
        raise InvalidDataFormatError("Item data must be a dictionary.")

    required_fields = ["item_id", "name", "type", "effect", "cost", "description"]
    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing required field: {field}")

    if item_dict["type"] not in ("weapon", "armor", "consumable"):
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")

    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("Field 'cost' must be an integer.")

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
    os.makedirs(data_dir, exist_ok=True)

    quests_path = os.path.join(data_dir, "quests.txt")
    items_path = os.path.join(data_dir, "items.txt")

    # Only create if missing
    if not os.path.isfile(quests_path):
        with open(quests_path, "w", encoding="utf-8") as f:
            f.write(
                "QUEST_ID: quest_001\n"
                "TITLE: The Beginning\n"
                "DESCRIPTION: Start your adventure by completing your first quest.\n"
                "REWARD_XP: 100\n"
                "REWARD_GOLD: 50\n"
                "REQUIRED_LEVEL: 1\n"
                "PREREQUISITE: NONE\n"
            )

    if not os.path.isfile(items_path):
        with open(items_path, "w", encoding="utf-8") as f:
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
    if not lines:
        raise InvalidDataFormatError("Empty quest block.")

    quest = {}
    for raw in lines:
        if ": " not in raw:
            raise InvalidDataFormatError(f"Invalid line format (expected 'KEY: value'): '{raw}'")
        key, value = raw.split(": ", 1)
        key = key.strip().lower()
        value = value.strip()

        if key in ("reward_xp", "reward_gold", "required_level"):
            try:
                value = int(value)
            except ValueError:
                raise InvalidDataFormatError(f"Field '{key}' must be an integer (got '{value}').")

        # Normalize prerequisite to "NONE" (uppercase) if specified as none/None
        if key == "prerequisite":
            if value.upper() == "NONE":
                value = "NONE"

        quest[key] = value

    # Map canonical field names: allow author to use either QUEST_ID or quest_id etc.
    # Ensure quest_id key exists
    if "quest_id" not in quest:
        raise InvalidDataFormatError("Missing 'QUEST_ID' in quest block.")

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
    if not lines:
        raise InvalidDataFormatError("Empty item block.")

    item = {}
    for raw in lines:
        if ": " not in raw:
            raise InvalidDataFormatError(f"Invalid line format (expected 'KEY: value'): '{raw}'")
        key, value = raw.split(": ", 1)
        key = key.strip().lower()
        value = value.strip()

        if key == "cost":
            try:
                value = int(value)
            except ValueError:
                raise InvalidDataFormatError(f"Field 'COST' must be an integer (got '{value}').")

        item[key] = value

    if "item_id" not in item:
        raise InvalidDataFormatError("Missing 'ITEM_ID' in item block.")

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

