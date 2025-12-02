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
    inventory = character.get('inventory', [])
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
    inventory = character.get('inventory', [])
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")
    else:
        inventory.remove(item_id)

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check
    inventory = character.get('inventory', [])
    if item_id in inventory:
        return True
    else:
        return False

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method
    item_count = 0
    inventory = character.get('inventory', [])
    for x in item_id in inventory:
        item_count += 1
    return item_count
    
    
def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    # TODO: Implement space calculation
    inventory = character.get('inventory', [])
    space_remaining = MAX_INVENTORY_SIZE - len(inventory)
    return space_remaining

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list
    removed_items = character.get('inventory', []).copy()
    character['inventory'] = []

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
    inventory = character.get('inventory', [])
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # TODO: Implement weapon equipping
    # Check item exists and is type 'weapon'
    # Handle unequipping current weapon if exists
    # Parse effect and apply to character stats
    # Store equipped_weapon in character dictionary
    # Remove item from inventory
    weapon.get('type')
    inventory = character.get('inventory', [])
    equip_weapon = character.get('equipped_weapon', weapon)
    print(equip_weapon)
    
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")
    if item_data.get('type') != 'weapon':
        raise InvalidItemTypeError(f"Item {item_id} is not a weapon")
    return f"Equipped weapon {item_id}."

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    # TODO: Implement armor equipping
    # Similar to equip_weapon but for armor
    inventory = character.get('inventory', [])
    equip_armor = character.get('equipped_armor', armor)
    print(equip_armor)
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")
    if item_data.get('type') != 'armor':
        raise InvalidItemTypeError(f"Item {item_id} is not armor")
    return f"Equipped armor {item_id}."

def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement weapon unequipping
    # Check if weapon is equipped
    # Remove stat bonuses
    # Add weapon back to inventory
    # Clear equipped_weapon from character
    unequip_weapon = character.get('equipped_weapon', weapon)
    print(unequip_weapon)
    if InventoryFullError:
        raise InventoryFullError
    return unequip_weapon

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement armor unequipping
    unequip_armor = character.get('equipped_armor', armor)
    print(unequip_armor)
    if InventoryFullError:
        raise InventoryFullError
    return unequip_armor

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    # TODO: Implement purchasing
    # Check if character has enough gold
    # Check if inventory has space
    # Subtract gold from character
    # Add item to inventory
    print(character)
    shop_item = item_data.get('cost', 0)
    print(shop_item)
    if character['gold'] < shop_item:
        raise InsufficientResourcesError(f"Do you have {shop_item} gold?") #Do you have Mcdonalds money?
    if len(character.get('inventory', [])) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError(f"We got {shop_item} at home!") #We got Mcdonalds at home
    character['gold'] -= shop_item
    character['inventory'].append(item_id)
    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement selling
    # Check if character has item
    # Calculate sell price (cost // 2)
    # Remove item from inventory
    # Add gold to character
    inventory = character.get('inventory', [])
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")
    sell_price = item_data.get('cost', 0) // 2
    character['gold'] += sell_price
    inventory.remove(item_id)
    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    # TODO: Implement effect parsing
    # Split on ":"
    # Convert value to integer
    stat_name, value = effect_string.split(":")
    stat_name = stat_name.strip()
    value = int(value.strip())
    return (stat_name, value)

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    # TODO: Implement stat application
    # Add value to character[stat_name]
    # If stat is health, ensure it doesn't exceed max_health
    if stat_name not in character:
        character[stat_name] = 0
    character[stat_name] += value
    if stat_name == 'health':
        if character['health'] > character.get('max_health', character['health']):
            character['health'] = character.get('max_health', character['health'])
    return character

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    # TODO: Implement inventory display
    # Count items (some may appear multiple times)
    # Display with item names from item_data_dict
    inventory = character.get('inventory', [])
    item_counts = {}
    for item_id in inventory:
        if item_id in item_counts:
            item_counts[item_id] += 1
        else:
            item_counts[item_id] = 1
    print("Inventory:")
    for item_id, count in item_counts.items():
        item_name = item_data_dict.get(item_id, {}).get('name', 'Unknown Item')
        print(f"- {item_name} (x{count})")
    return display_inventory

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

