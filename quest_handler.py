"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    """
    # 1. Check quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} not found")
    quest = quest_data_dict[quest_id]

    active = character.get("active_quests", [])
    completed = character.get("completed_quests", [])
    level = character.get("level", 1)

    # 2. Level requirement
    if level < quest["required_level"]:
        raise InsufficientLevelError(
            f"Level {quest['required_level']} required for {quest_id}"
        )

    # 3. Prerequisite requirement
    prereq = quest.get("prerequisite", "NONE")
    if prereq != "NONE" and prereq not in completed:
        raise QuestRequirementsNotMetError(
            f"Must complete {prereq} before starting {quest_id}"
        )

    # 4. Not already completed
    if quest_id in completed:
        raise QuestAlreadyCompletedError(f"{quest_id} already completed")

    # 5. Not already active
    if quest_id in active:
        raise QuestAlreadyCompletedError(f"{quest_id} is already active")

    # 6. Accept quest
    active.append(quest_id)
    character["active_quests"] = active
    return True


def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    """
    # 1. Exists?
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} not found")
    quest = quest_data_dict[quest_id]

    active = character.get("active_quests", [])
    completed = character.get("completed_quests", [])

    # 2. Must be active
    if quest_id not in active:
        raise QuestNotActiveError(f"Quest {quest_id} is not active")

    # 3. Remove from active
    active.remove(quest_id)
    character["active_quests"] = active

    # 4. Add to completed
    if quest_id not in completed:
        completed.append(quest_id)
    character["completed_quests"] = completed

    # 5. Reward
    xp = quest["reward_xp"]
    gold = quest["reward_gold"]

    # Character manager functions assumed implemented elsewhere
    # Add XP
    if "experience" in character:
        character["experience"] += xp

    # Add gold
    if "gold" in character:
        character["gold"] += gold

    return {"reward_xp": xp, "reward_gold": gold}


def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    """
    active = character.get("active_quests", [])
    if quest_id not in active:
        raise QuestNotActiveError(f"Quest {quest_id} is not active")

    active.remove(quest_id)
    character["active_quests"] = active
    return True


def get_active_quests(character, quest_data_dict):
    """
    Return full quest dictionaries for active quests
    """
    active = character.get("active_quests", [])
    return [quest_data_dict[qid] for qid in active if qid in quest_data_dict]


def get_completed_quests(character, quest_data_dict):
    """
    Return full quest dictionaries for completed quests
    """
    completed = character.get("completed_quests", [])
    return [quest_data_dict[qid] for qid in completed if qid in quest_data_dict]


def get_available_quests(character, quest_data_dict):
    """
    Quests character can accept right now
    """
    active = set(character.get("active_quests", []))
    completed = set(character.get("completed_quests", []))
    level = character.get("level", 1)

    available = []

    for qid, quest in quest_data_dict.items():
        prereq = quest.get("prerequisite", "NONE")

        # Requirements
        if qid in active:
            continue
        if qid in completed:
            continue
        if level < quest["required_level"]:
            continue
        if prereq != "NONE" and prereq not in completed:
            continue

        available.append(quest)

    return available

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    return quest_id in character.get("completed_quests", [])


def is_quest_active(character, quest_id):
    return quest_id in character.get("active_quests", [])


def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Boolean-only version of accept_quest
    """
    if quest_id not in quest_data_dict:
        return False
    quest = quest_data_dict[quest_id]

    active = set(character.get("active_quests", []))
    completed = set(character.get("completed_quests", []))
    level = character.get("level", 1)
    prereq = quest.get("prerequisite", "NONE")

    if level < quest["required_level"]:
        return False
    if prereq != "NONE" and prereq not in completed:
        return False
    if quest_id in completed:
        return False
    if quest_id in active:
        return False

    return True


def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Returns a list from earliest prerequisite to the quest itself
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} not found")

    chain = []
    current = quest_id

    while True:
        if current not in quest_data_dict:
            raise QuestNotFoundError(f"Quest {current} not found")

        chain.insert(0, current)

        prereq = quest_data_dict[current].get("prerequisite", "NONE")
        if prereq == "NONE":
            break

        current = prereq

    return chain

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    total = len(quest_data_dict)
    if total == 0:
        return 0.0

    completed = len(character.get("completed_quests", []))
    return (completed / total) * 100


def get_total_quest_rewards_earned(character, quest_data_dict):
    total_xp = 0
    total_gold = 0

    for qid in character.get("completed_quests", []):
        if qid in quest_data_dict:
            q = quest_data_dict[qid]
            total_xp += q["reward_xp"]
            total_gold += q["reward_gold"]

    return {"total_xp": total_xp, "total_gold": total_gold}


def get_quests_by_level(quest_data_dict, min_level, max_level):
    return [
        quest
        for quest in quest_data_dict.values()
        if min_level <= quest["required_level"] <= max_level
    ]

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Required Level: {quest_data['required_level']}")
    print(f"Prerequisite: {quest_data['prerequisite']}")
    print(f"Rewards: {quest_data['reward_xp']} XP, {quest_data['reward_gold']} Gold")


def display_quest_list(quest_list):
    print("\n=== Quest List ===")
    for q in quest_list:
        print(f"- {q['title']} (Level {q['required_level']}): "
        f"{q['reward_xp']} XP, {q['reward_gold']} Gold")


def display_character_quest_progress(character, quest_data_dict):
    active_count = len(character.get("active_quests", []))
    completed_count = len(character.get("completed_quests", []))
    pct = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)

    print("\n=== Quest Progress ===")
    print(f"Active Quests: {active_count}")
    print(f"Completed Quests: {completed_count}")
    print(f"Completion Percentage: {pct:.2f}%")
    print(f"Total XP Earned: {rewards['total_xp']}")
    print(f"Total Gold Earned: {rewards['total_gold']}")
# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    for qid, data in quest_data_dict.items():
        prereq = data.get("prerequisite", "NONE")
        if prereq != "NONE" and prereq not in quest_data_dict:
            raise QuestNotFoundError(
                f"Prerequisite {prereq} for quest {qid} not found"
            )
    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")

