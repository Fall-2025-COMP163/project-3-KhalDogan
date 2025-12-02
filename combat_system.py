"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

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
    enemy_types = {
        "goblin": { 'name': 'Goblin', 'health': 50, 'max_health': 50, 'strength': 8, 'magic': 2, 'xp_reward': 25, 'gold_reward': 10 },
        "orc":    { 'name': 'Orc',    'health': 80, 'max_health': 80, 'strength': 12,'magic': 5, 'xp_reward': 50, 'gold_reward': 25 },
        "dragon": { 'name': 'Dragon', 'health': 200,'max_health': 200,'strength': 25,'magic': 15,'xp_reward': 200,'gold_reward': 100 }
    }

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
        while self.combat_active:
            self.turn_counter += 1
            self.player_turn()
            if not self.combat_active:
                break
            self.enemy_turn()
            result = self.check_battle_end()
            if result:
                self.combat_active = False
                if result == 'player':
                    rewards = get_victory_rewards(self.enemy)
                    return {
                        'winner': 'player',
                        'xp_gained': rewards['xp'],
                        'gold_gained': rewards['gold']
                    }
                else:
                    raise CharacterDeadError("Plays Mario Bros death sound")
    
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
        if self.combat_active:
            battle_options = input("\nWhat You Wanna do, Bro?\nFight \nUse an Item\n Run): ").strip().lower()
            if battle_options == 'fight':
                fight_options = input("\nChoose your attack:\n Basic Attack \n Special Ability\n").strip().lower()
                if fight_options == 'special ability':
                    ability_result = use_special_ability(self.character, self.enemy)
                    display_battle_log(ability_result)
                elif fight_options == 'basic attack':
                    damage = self.calculate_damage(self.character, self.enemy)
                    self.apply_damage(self.enemy, damage)
                    display_battle_log(f"You attacked the {self.enemy['name']} for {damage} damage!")              
            elif battle_options == 'use an item':
                # Placeholder for item usage
                display_battle_log("You rummaged through your bag but found nothing useful!")
            elif battle_options == 'run':
                run_chance = random.int(1, 100)
                if run_chance > 50:
                    display_battle_log("What You Running for?")
                    self.combat_active = False
                else:
                    display_battle_log("Escape failed! The battle continues.")
        else:
            raise CombatNotActiveError("Womp Womp! \n FuFu go get the Lion!")
    
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
        if self.combat_active:
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
        self.damage = attacker['strength'] - (defender['strength'] // 4)
        if self.damage < 1:
            print(f'Power level is too low.')
        else:
            self.damage = self.damage = attacker['strength'] - (defender['strength'] // 4)
        return self.damage
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        target['health'] -= damage
        if target['health'] < 0:
            target['health'] = 0
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        if combat_active == False:
            if self.enemy['health'] <= 0:
                return 'player'
            else:
                return 'enemy'
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        escape_chance = random.randint(1, 100)
        if escape_chance > 50:
            self.combat_active = False
            return True

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
    char_class = character['class'].lower()
    if char_class == 'warrior':
        warrior_power_strike(character, enemy)
        return f"{character['name']} used Power Strike on {enemy['name']}!"
    elif char_class == 'mage':
        mage_fireball(character, enemy)
        return f"{character['name']} cast Fireball on {enemy['name']}!"
    elif char_class == 'rogue':
        rogue_critical_strike(character, enemy)
        return f"{character['name']} performed Critical Strike on {enemy['name']}!"
    elif char_class == 'cleric':
        cleric_heal(character)
        return f"{character['name']} healed themselves!"

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    power_strike = character['strength'] * 2 - (enemy['strength'] // 2)
    # ensure at least 1 damage, apply to enemy and clamp health to zero
    power_strike_cooldown = 3 tuns
    return damage

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    fireball = character['magic'] * 2 - (enemy['magic'] // 4)
    fireball_cooldown = 2 turns
    return damage

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    critical_chance = random.randint(1, 100)
    if critical_chance <= 50:
        critical_strike = character['strength'] * 3 - (enemy['strength'] // 2)
    else:
        critical_strike = character['strength'] - (enemy['strength'] // 2)
    critical_strike_cooldown = 4 turns
    return damage

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    healing_amount = 30
    if character['health'] + healing_amount > character['max_health']:
        healing_amount = character['max_health'] - character['health']
    healing_amount_cooldown = 5 turns
    return healing_amount

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    if character['health'] > 0:
        return True
    else:
        return False

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    if enemy_health <= 0:
        rewards = {
            'xp': enemy['xp_reward'],
            'gold': enemy['gold_reward']
        }

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    print(display_combat_stats)

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

