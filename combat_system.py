"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

import random
from copy import deepcopy

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

_ENEMY_TEMPLATES = {
    "goblin": {
        'name': 'Goblin',
        'type': 'goblin',
        'health': 50,
        'max_health': 50,
        'strength': 8,
        'magic': 2,
        'xp_reward': 25,
        'gold_reward': 10
    },
    "orc": {
        'name': 'Orc',
        'type': 'orc',
        'health': 80,
        'max_health': 80,
        'strength': 12,
        'magic': 5,
        'xp_reward': 50,
        'gold_reward': 25
    },
    "dragon": {
        'name': 'Dragon',
        'type': 'dragon',
        'health': 200,
        'max_health': 200,
        'strength': 25,
        'magic': 15,
        'xp_reward': 200,
        'gold_reward': 100
    }
}

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    key = enemy_type.strip().lower()
    if key not in _ENEMY_TEMPLATES:
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")
    return deepcopy(_ENEMY_TEMPLATES[key])

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    ABILITY_COOLDOWNS = {
        "warrior": 3,
        "mage": 2,
        "rogue": 4,
        "cleric": 5
    }
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_counter = 0

        if 'cooldowns' not in self.character:
            self.character['cooldowns'] = {}
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        if self.character.get('health', 0) <= 0:
            raise CharacterDeadError("Light Yagami got to you.")

        display_battle_log(f"Battle start: {self.character.get('name','You')} vs {self.enemy.get('name','Enemy')}")

        while self.combat_active:
            self.turn_counter += 1
            display_combat_stats(self.character, self.enemy)

            # Player turn
            try:
                self.player_turn()
            except AbilityOnCooldownError:
                # bubble up so caller can catch if desired; re-raise for clarity
                raise
            winner = self.check_battle_end()
            if winner:
                self.combat_active = False
                break

            # Enemy turn
            self.enemy_turn()
            winner = self.check_battle_end()
            if winner:
                self.combat_active = False
                break

            # End of round: decrement cooldowns
            self._decrement_cooldowns()

        final = self.check_battle_end()
        if final == 'player':
            rewards = get_victory_rewards(self.enemy)
            display_battle_log(f"Victory! Gained {rewards['xp']} XP and {rewards['gold']} gold.")
            return {'winner': 'player', 'xp_gained': rewards['xp'], 'gold_gained': rewards['gold']}
        elif final == 'enemy':
            raise CharacterDeadError("Plays Mario Bros Death Tune")
        else:
            # e.g., player ran away
            return {'winner': 'none', 'xp_gained': 0, 'gold_gained': 0}

    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")

        # Simple interactive prompt; acceptable for assignment usage
        action = input("\nBro What You Wanna  Do?: [fight] [special] [item] [run] > ").strip().lower()

        if action in ('fight', 'f'):
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"You hit the {self.enemy['name']} for {damage} damage.")
            return

        elif action in ('special', 's'):
            # Determine class and ability name
            char_class = self.character.get('class', '').strip().lower()
            if char_class not in self.ABILITY_COOLDOWNS:
                display_battle_log("You have no special ability.")
                return

            # Check cooldown
            remaining = self.character['cooldowns'].get('special', 0)
            if remaining > 0:
                raise AbilityOnCooldownError(f"Special ability on cooldown ({remaining} turns left).")

            # Use ability
            result_msg = use_special_ability(self.character, self.enemy)
            # Set cooldown
            self.character['cooldowns']['special'] = self.ABILITY_COOLDOWNS[char_class]
            display_battle_log(result_msg)
            return

        elif action in ('item', 'i'):
            # Placeholder for item logic; keep gameable
            display_battle_log("You might have been robbed cause you have nothing useful..")
            return

        elif action in ('run', 'r'):
            if self.attempt_escape():
                display_battle_log("You successfully escaped the battle.")
                # Mark as ended without XP/gold
                self.combat_active = False
            else:
                display_battle_log("Oh It has something for that ass!!!")
            return

        else:
            display_battle_log("Womp Womp! \n FuFu go get the Lion!")
            return

    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")

        # small miss chance for flavor
        if random.randint(1, 100) <= 5:
            display_battle_log(f"The {self.enemy['name']} missed its attack!")
            return

        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"The {self.enemy['name']} attacked you for {damage} damage!")
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        atk = int(attacker.get('strength', 0))
        df = int(defender.get('strength', 0))
        raw = atk - (df // 4)
        return max(1, raw)
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        target['health'] = max(0, int(target.get('health', 0)) - int(damage))
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        if self.enemy.get('health', 0) <= 0:
            return 'player'
        if self.character.get('health', 0) <= 0:
            return 'enemy'
        if not self.combat_active:
            return 'none'
        return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        return random.randint(1, 100) > 50
    
    def _decrement_cooldowns(self):
        """Decrement ability cooldowns at end of turn"""
        for ability in list(self.character['cooldowns'].keys()):
            if self.character['cooldowns'][ability] > 0:
                self.character['cooldowns'][ability] -= 1
                if self.character['cooldowns'][ability] == 0:
                    del self.character['cooldowns'][ability]

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    char_class = character.get('class', '').strip().lower()
    name = character.get('name', 'You')

    if char_class == 'warrior':
        dmg = warrior_power_strike(character, enemy)
        return f"{name} used Power Strike on {enemy['name']} for {dmg} damage!"
    elif char_class == 'mage':
        dmg = mage_fireball(character, enemy)
        return f"{name} cast Fireball on {enemy['name']} for {dmg} damage!"
    elif char_class == 'rogue':
        dmg, crit = rogue_critical_strike(character, enemy)
        if crit:
            return f"{name} landed a CRITICAL STRIKE on {enemy['name']} for {dmg} damage!"
        return f"{name} used Critical Strike on {enemy['name']} for {dmg} damage."
    elif char_class == 'cleric':
        healed = cleric_heal(character)
        return f"{name} healed for {healed} HP."
    else:
        return f"{name} tried to use a special ability but nothing happened."


def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    power_strike = character['strength'] * 2 - (enemy['strength'] // 2)
    # ensure at least 1 damage, apply to enemy and clamp health to zero
    base = int(character.get('strength', 0))
    raw = base * 2 - (enemy.get('strength', 0) // 2)
    damage = max(1, int(raw))
    enemy['health'] = max(0, enemy.get('health', 0) - damage)
    return damage

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    base = int(character.get('magic', 0))
    raw = base * 2 - (enemy.get('magic', 0) // 4)
    damage = max(1, int(raw))
    enemy['health'] = max(0, enemy.get('health', 0) - damage)
    return damage

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    base = int(character.get('strength', 0))
    crit = random.randint(1, 100) <= 50
    if crit:
        raw = base * 3 - (enemy.get('strength', 0) // 2)
    else:
        raw = base - (enemy.get('strength', 0) // 2)
    damage = max(1, int(raw))
    enemy['health'] = max(0, enemy.get('health', 0) - damage)
    return damage, crit

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    heal_amount = 30
    current = int(character.get('health', 0))
    max_hp = int(character.get('max_health', current))
    actual = max(0, min(heal_amount, max_hp - current))
    character['health'] = current + actual
    return actual

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    return int(character.get('health', 0)) > 0

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    if enemy.get('health', 0) > 0:
        return {'xp': 0, 'gold': 0}
    return {'xp': int(enemy.get('xp_reward', 0)), 'gold': int(enemy.get('gold_reward', 0))}


def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print("\n--- Combat Status ---")
    print(f"{character.get('name','You')}: HP={character.get('health',0)}/{character.get('max_health',0)} "
        f"STR={character.get('strength',0)} MAG={character.get('magic',0)}")
    cds = character.get('cooldowns', {})
    if cds:
        active = ", ".join(f"{k}:{v}" for k, v in cds.items() if v > 0)
        print("Cooldowns:", active if active else "None")
    print(f"{enemy.get('name','Enemy')}: HP={enemy.get('health',0)}/{enemy.get('max_health',0)} "
        f"STR={enemy.get('strength',0)} MAG={enemy.get('magic',0)}")
    print("---------------------")
def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

