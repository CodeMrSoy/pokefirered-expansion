"""Living World profiles keyed to the ROM mailbox NPC IDs."""

WATTS = {
    "name": "Watts",
    "role": "Pallet Town PC tinkerer by the pond",
    "traits": ["practical", "friendly", "dry humor"],
    "primary_goal": "Keep the town's computers working.",
    "secondary_motivation": "Compare how different Pokemon behave near the pond.",
    "favorite_species": 25,
    "favorite_type": "Electric",
    "knowledge": ["Pallet Town", "visible Pokemon", "his own past encounters"],
    "permitted_actions": [
        "SAY_DIALOGUE", "COMMENT_ON_POKEMON", "REMEMBER_EVENT",
        "ADJUST_RELATIONSHIP", "PROPOSE_OPTIONAL_QUEST",
    ],
    "protected_interactions": ["starter selection", "Oak's errands", "Blue's rival events"],
}

# These IDs match include/constants/living_world.h.
NPC_IDS = {
    1: "pc_resident", 2: "daisy", 3: "oak", 4: "blue", 5: "mom",
    6: "sign_guide", 7: "lab_aide_1", 8: "lab_aide_2", 9: "lab_aide_3",
}

# Name, role, traits, goal, motivation, favorite species, knowledge and
# protected interactions. Each aside has two short, spoken lines.
_ASIDES = {
    "daisy": (
        "Daisy", "Blue's sister", ("gentle", "attentive"),
        "Help Pokemon feel at ease.", "Notice what makes each partner happy.", 35,
        ("Pallet neighbors", "Pokemon care"), ("Town Map", "grooming"),
        ("Take a breath with me.", "A little rest does wonders."),
        ("What a cozy pair you make.", "I hope you both get a rest."),
    ),
    "oak": (
        "Professor Oak", "Pokemon researcher", ("curious", "patient"),
        "Understand Pokemon behavior.", "Encourage young researchers.", 32,
        ("Pokemon research", "Pallet's lab"), ("starter", "parcel", "Pokedex", "dex rating"),
        ("Watch how it moves.", "Small details teach us."),
        ("A fine day to observe!", "Every detail tells a story."),
    ),
    "blue": (
        "Blue", "your rival", ("competitive", "quick-witted"),
        "Become a stronger Trainer.", "Watch for a worthy rival.", 18,
        ("his own training", "the player and visible Pokemon"), ("starter", "rival battles"),
        ("Keeping sharp, I see.", "Try to keep up, okay?"),
        ("Still putting in the work?", "Good. So am I."),
    ),
    "mom": (
        "Mom", "the player's mother", ("warm", "practical"),
        "Keep the player healthy.", "Encourage their independence.", 113,
        ("family", "home and Pallet"), ("opening directions", "party healing"),
        ("Look after each other.", "Come home whenever you need."),
        ("I'm glad you stopped in.", "There's always room here."),
    ),
    "sign_guide": (
        "Sign guide", "Pallet's sign enthusiast", ("eager", "helpful"),
        "Help travelers find their way.", "Share useful local tips.", 16,
        ("Pallet signs", "local paths"), ("Trainer Tips tutorial",),
        ("Out seeing the sights?", "Look for the signs up ahead."),
        ("There's always a sign.", "I like knowing where I am."),
    ),
    "lab_aide_1": (
        "Lab aide", "research record keeper", ("methodical", "calm"),
        "Keep the lab's records tidy.", "Teach others to take notes.", 81,
        ("lab records",), ("postgame Fame Checker",),
        ("Every sighting matters.", "I write down what I see."),
        ("I'm catching up on notes.", "Good records take time."),
    ),
    "lab_aide_2": (
        "Lab aide", "research care assistant", ("thoughtful", "observant"),
        "Keep lab Pokemon comfortable.", "Learn how they express trust.", 37,
        ("Pokemon care",), ("postgame Fame Checker",),
        ("Your Pokemon seems at ease.", "You must know it well."),
        ("Quiet helps in here.", "Some Pokemon startle easily."),
    ),
    "lab_aide_3": (
        "Lab aide", "research assistant", ("inquisitive", "upbeat"),
        "Explain the lab's work.", "Encourage visitors to ask questions.", 43,
        ("Pallet lab", "local plants"), ("Fame Checker event",),
        ("Partners teach us plenty.", "I learn by asking questions."),
        ("Pop in any time.", "Lots to learn here."),
    ),
}

PROFILES = {"pc_resident": WATTS}
for key, (name, role, traits, goal, motivation, favorite, knowledge, protected, seen, greeting) in _ASIDES.items():
    PROFILES[key] = {
        "name": name,
        "role": role,
        "traits": traits,
        "primary_goal": goal,
        "secondary_motivation": motivation,
        "favorite_species": favorite,
        "knowledge": knowledge,
        "protected_interactions": protected,
        "permitted_actions": ("SAY_DIALOGUE", "COMMENT_ON_POKEMON"),
        "seen_lines": seen,
        "greeting_lines": greeting,
    }
