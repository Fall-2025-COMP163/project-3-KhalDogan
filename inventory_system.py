"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    # Add item_id to character['inventory'] list
    inventory = character.get("inventory", [])
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Don't you feel Heavy Yet?")
    inventory.append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    # Check if item exists in inventory
    # Remove item from list
    inventory = character.get("inventory", [])
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")
    inventory.remove(item_id)
    return True


def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check
    return item_id in character.get("inventory", [])

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method
    inventory = character.get("inventory", [])
    return inventory.count(item_id)
    
def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    # TODO: Implement space calculation
    inventory = character.get("inventory", [])
    return MAX_INVENTORY_SIZE - len(inventory)

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list
    removed = character.get("inventory", []).copy()
    character["inventory"] = []
    return removed
# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # TODO: Implement item usage
    # Check if character has the item
    # Check if item type is 'consumable'
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    # Apply effect to character
    # Remove item from inventory
    inventory = character.get("inventory", [])

    if item_id not in inventory:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")

    if item_data.get("type") != "consumable":
        raise InvalidItemTypeError(f"Item {item_id} is not a consumable")

    # Parse effect
    stat_name, value = parse_item_effect(item_data.get("effect", ""))

    # Apply stat effect
    apply_stat_effect(character, stat_name, value)

    # Remove item from inventory
    inventory.remove(item_id)

    return f"Used {item_data.get('name', item_id)}. {stat_name} increased by {value}."


def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon. Handles unequip logic and stat bonuses.
    """
    inventory = character.get("inventory", [])

    if item_id not in inventory:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")

    if item_data.get("type") != "weapon":
        raise InvalidItemTypeError(f"Item {item_id} is not a weapon")

    # Parse effect (e.g., "strength:5")
    stat, value = parse_item_effect(item_data["effect"])

    # If already equipped, unequip old weapon
    old_weapon_id = character.get("equipped_weapon")
    if old_weapon_id:
        old_weapon_data = character["item_data"][old_weapon_id]
        old_stat, old_value = parse_item_effect(old_weapon_data["effect"])
        apply_stat_effect(character, old_stat, -old_value)  # remove bonus
        add_item_to_inventory(character, old_weapon_id)

    # Apply new weapon bonus
    apply_stat_effect(character, stat, value)

    # Set equipped weapon
    character["equipped_weapon"] = item_id
    inventory.remove(item_id)

    return f"Equipped weapon {item_data['name']} (+{value} {stat})."


def equip_armor(character, item_id, item_data):
    """Equip armor; similar to weapons but affects health/max_health/etc."""
    inventory = character.get("inventory", [])

    if item_id not in inventory:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")

    if item_data.get("type") != "armor":
        raise InvalidItemTypeError(f"Item {item_id} is not armor")

    stat, value = parse_item_effect(item_data["effect"])

    # Unequip previous armor
    old_armor_id = character.get("equipped_armor")
    if old_armor_id:
        old_armor_data = character["item_data"][old_armor_id]
        old_stat, old_value = parse_item_effect(old_armor_data["effect"])
        apply_stat_effect(character, old_stat, -old_value)
        add_item_to_inventory(character, old_armor_id)

    apply_stat_effect(character, stat, value)

    character["equipped_armor"] = item_id
    inventory.remove(item_id)

    return f"Equipped armor {item_data['name']} (+{value} {stat})."


def unequip_weapon(character):
    """
    Unequip weapon and return it to inventory.
    """
    weapon_id = character.get("equipped_weapon")
    if not weapon_id:
        return None

    weapon_data = character["item_data"][weapon_id]
    stat, value = parse_item_effect(weapon_data["effect"])

    # Remove stat bonuses
    apply_stat_effect(character, stat, -value)

    # Try adding back to inventory
    add_item_to_inventory(character, weapon_id)

    character["equipped_weapon"] = None
    return weapon_id


def unequip_armor(character):
    """
    Unequip armor and return it to inventory.
    """
    armor_id = character.get("equipped_armor")
    if not armor_id:
        return None

    armor_data = character["item_data"][armor_id]
    stat, value = parse_item_effect(armor_data["effect"])
    apply_stat_effect(character, stat, -value)

    add_item_to_inventory(character, armor_id)

    character["equipped_armor"] = None
    return armor_id

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """Buy an item from the shop."""
    cost = item_data.get("cost", 0)

    if character["gold"] < cost:
        raise InsufficientResourcesError(f"Do you have {cost} gold?")

    if len(character.get("inventory", [])) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("We got that at home!")  # your joke preserved

    character["gold"] -= cost
    character["inventory"].append(item_id)
    return True


def sell_item(character, item_id, item_data):
    """Sell an item for half price."""
    inventory = character.get("inventory", [])

    if item_id not in inventory:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")

    price = item_data.get("cost", 0) // 2
    character["gold"] += price
    inventory.remove(item_id)
    return price


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """Parse 'stat:value' into (stat, int(value))."""
    if ":" not in effect_string:
        raise InvalidItemTypeError(f"Invalid effect format: {effect_string}")
    stat, value = effect_string.split(":")
    return stat.strip(), int(value.strip())


def apply_stat_effect(character, stat_name, value):
    """
    Apply bonus to character stats.
    """
    character[stat_name] = character.get(stat_name, 0) + value

    # Health cannot exceed max_health
    if stat_name == "health":
        max_hp = character.get("max_health", character["health"])
        if character["health"] > max_hp:
            character["health"] = max_hp


def display_inventory(character, item_data_dict):
    """
    Display inventory in a readable format.
    """
    inventory = character.get("inventory", [])
    counts = {}

    for item_id in inventory:
        counts[item_id] = counts.get(item_id, 0) + 1

    print("Inventory:")
    if not counts:
        print("- (empty)")
        return

    for item_id, count in counts.items():
        name = item_data_dict.get(item_id, {}).get("name", "Unknown Item")
        print(f"- {name} (x{count})")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")

