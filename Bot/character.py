from enum import Enum
from commands import utils
import random
import re

class Attack:

    def __init__(self, name, atk_bonus, damage, other_descriptions):
        self.name = name
        self.atk_bonus = atk_bonus
        self.damage = damage
        self.other_descriptions = descriptions

    def __str__(self):

        pass

class Description:
    
    def __init__(self, title, description):
        self.title = title
        self.description = description

class Dice:

    def __init__(self, amount, sides):
        self.amount = amount
        self.sides = sides

    def roll(self):
        result = [];
        for i in range(0, self.amount):
            result.append(random.randint(1, self.sides))
        return result

class CharacterCompletion(Enum):
    START = 0
    NAME = 1
    RACE = 2
    CLASS = 3
    BACKGROUND = 4
    ALIGNMENT = 5
    LEVEL = 6
    EXP = 7
    STR = 8
    DEX = 9
    CON = 10
    INT = 11
    WIS = 12
    CHA = 13
    MODS = 14
    SAVES = 15
    INSPIRATION = 16
    PROFICIENCY_MODIFIER = 17
    SKILLS = 18
    PROFICIENCIES = 19
    LANGUAGES = 20
    OTHER_PROFICIENCIES = 21
    CURRENCY = 22
    EQUIPMENT = 23
    ATTACKS = 24
    OTHER_ATTACKS = 24
    ARMOR_CLASS = 25
    INITIATIVE = 26
    SPEED = 27
    HIT_DICE = 28
    MAX_HP = 29
    HP = 30
    DEATH_SAVES = 31
    FEATURES = 32
    PERSONALITY = 33
    IDEALS = 34
    BONDS = 35
    FLAWS = 36
    FINISH = 37
    CANCEL = -1

class Character:

    skills_list = ["Acrobatics",
                  "Animal Handling",
                  "Arcana",
                  "Athletics",
                  "Deception",
                  "History",
                  "Insight",
                  "Intimidation",
                  "Investigation",
                  "Medicine",
                  "Nature",
                  "Perception",
                  "Performance",
                  "Persuasion",
                  "Religion",
                  "Sleight of Hand",
                  "Stealth",
                  "Survival"]

    def __init__(self):
        self.name = ""
        self.race = ""
        self.chara_class = ""
        self.background = ""
        self.alignment = ""

        self.level = 1
        self.exp = 0

        self.str = 0
        self.dex = 0
        self.con = 0
        self.int = 0
        self.wis = 0
        self.cha = 0
        self.str_mod = 0
        self.dex_mod = 0
        self.con_mod = 0
        self.int_mod = 0
        self.wis_mod = 0
        self.cha_mod = 0
        self.str_save = 0
        self.dex_save = 0
        self.con_save = 0
        self.int_save = 0
        self.wis_save = 0
        self.cha_save = 0

        self.inspiration = 0
        self.proficiency_bonus = 0
        self.passive_perception = 0
        self.skills = zip(skills_list, [0] * len(skills_list))
        
        self.proficiencies = []
        self.languages = []
        self.other_proficiencies = [] # set of Description

        self.currency = [0, 0, 0, 0, 0] # CP, SP, EP, GP, PP
        self.inventory = []

        self.attacks = []
        self.other_attacks = [] # set of Description

        self.armor_class = 0
        self.initiative_modifier = self.dex_mod
        self.speed = 0
        self.hit_dice = None # Dice object
        self.max_hp = 0
        self.current_hp = self.max_hp
        self.temp_hp = 0
        self.death_save_success = 0
        self.death_save_failure = 0

        self.features = [] # set of Description

        self.personality_trait = ""
        self.ideals = ""
        self.bonds = ""
        self.flaws = ""

        self.creation_progress = CharacterCompletion.START
        self.current_message = "What will the name of your character be?"
        self.confirmation = False

    # as of right now the only creation input will be "fully custom" i.e. all inputs will be manual
    # later, an implementation of a guided creation process (more beginner friendly) will be available
    def continue_create(self, input):
        input_lower = input.lower()
        if input_lower == "cancel" or input_lower == "exit":
            self.confirmation = True
            self.creation_progress = CharacterCompletion.CANCEL
            return "Are you sure you want to exit character creation? All of your progress will be deleted! (y/yes to confirm, any other input to cancel)"
        if self.creation_progress == CharacterCompletion.CANCEL and self.confirmation:
            if utils.is_positive_input(input_lower):
                return "Character creation has been cancelled."
            else:
                return "Character creation will continue. {}".format(self.current_message)
        if self.creation_progress == CharacterCompletion.START:
            current_step = CharacterCompletion.NAME
            next_msg = "What will the race of your character be?"
            verification = lambda str : "\n" not in str
            error_msg = "Your name may not contain newline characters! Try again:"
            change_var = self.set_name
            confirmation_msg = "Your character's name will be {}, are you sure? (y/yes to confirm, any other input to cancel)"
            return self.check_input(input, current_step, next_msg, verification, error_msg, change_var, confirmation_msg)
        elif self.creation_progress == CharacterCompletion.NAME:
            current_step = CharacterCompletion.RACE
            next_msg = "What will the class of your character be?"
            verification = lambda str : True # TODO verification
            error_msg = ""
            change_var = self.set_race
            confirmation_msg = "Your character's race will be {}, are you sure? (y/yes to confirm, any other input to cancel)"
            return self.check_input(input, current_step, next_msg, verification, error_msg, change_var, confirmation_msg)
        elif self.creation_progress == CharacterCompletion.RACE:
            current_step = CharacterCompletion.CLASS
            next_msg = "What will the background of your character be?"
            verification = lambda str : True # TODO verification
            error_msg = ""
            change_var = self.set_class
            confirmation_msg = "Your character's class will be {}, are you sure? (y/yes to confirm, any other input to cancel)"
            return self.check_input(input, current_step, next_msg, verification, error_msg, change_var, confirmation_msg)
        elif self.creation_progress == CharacterCompletion.CLASS:
            current_step = CharacterCompletion.BACKGROUND
            next_msg = "What will the alignment of your character be?"
            verification = lambda str : True # TODO verification
            error_msg = ""
            change_var = self.set_background
            confirmation_msg = "Your character's background will be {}, are you sure? (y/yes to confirm, any other input to cancel)"
            return self.check_input(input, current_step, next_msg, verification, error_msg, change_var, confirmation_msg)
        elif self.creation_progress == CharacterCompletion.BACKGROUND:
            current_step = CharacterCompletion.ALIGNMENT
            next_msg = "Enter the level of your character: (Input 1 if it is a new character)"
            verification = lambda str : True # TODO verification
            error_msg = ""
            change_var = self.set_alignment
            confirmation_msg = "Your character's alignment will be {}, are you sure? (y/yes to confirm, any other input to cancel)"
            return self.check_input(input, current_step, next_msg, verification, error_msg, change_var, confirmation_msg)
        elif self.creation_progress == CharacterCompletion.ALIGNMENT:
            current_step = CharacterCompletion.LEVEL
            next_msg = "Enter the EXP amount for your character: (Input 0 if it is a new character)"
            verification = lambda str : re.fullmatch("\\d+") is not None
            error_msg = "Input must be a nonnegative integer! Try again:"
            change_var = self.set_level
            confirmation_msg = "Your character's level will be {}, are you sure? (y/yes to confirm, any other input to cancel)"
            return self.check_input(input, current_step, next_msg, verification, error_msg, change_var, confirmation_msg)
        elif self.creation_progress == CharacterCompletion.LEVEL:
            current_step = CharacterCompletion.EXP
            next_msg = "Enter the STR, DEX, CON, INT, WIS, CHA stats of your character in the format of [STR] [STR modifier] [STR saving-roll], [DEX] [DEX modifier] [DEF saving-roll] and so on."
            verification = lambda str : re.fullmatch("\\d+") is not None
            error_msg = "Input must be a nonnegative integer! Try again:"
            change_var = self.set_exp
            confirmation_msg = "Your character's exp will be {}, are you sure? (y/yes to confirm, any other input to cancel)"
            return self.check_input(input, current_step, next_msg, verification, error_msg, change_var, confirmation_msg)
        elif self.creation_progress == CharacterCompletion.EXP:
            current_step = CharacterCompletion.SAVES
            next_msg = "Enter the inspiration of your character: (Input 0 if it is a new character)"
            verification = lambda str : re.fullmatch("(\\d+\\s+-?\\d+\\s+-?\\d+,\\s*){5}(\\d+\\s+-?\\d+\\s+-?\\d+)") is not None
            error_msg = "Input must in the format of [STR] [STR modifier] [STR saving-roll], [DEX] [DEX modifier] [DEF saving-throws] and all numbers must be an integer! Example input: `15 2 2, 8 -1 -1 ...`.\nTry again:"
            change_var = self.set_stats
            confirmation_msg = "Your character's stats will be {}, are you sure? (y/yes to confirm, any other input to cancel)"
            return self.check_input(input, current_step, next_msg, verification, error_msg, change_var, confirmation_msg)
        elif self.creation_progress == CharacterCompletion.SAVES:
            current_step = CharacterCompletion.INSPIRATION
            next_msg = "Enter the Proficiency Modifier of your character: (Input 2 if it is a new character)"
            verification = lambda str : re.fullmatch("-?\\d+") is not None
            error_msg = "Input must be an integer! Try again:"
            change_var = self.set_inspiration
            confirmation_msg = "Your character's inspiration will be {}, are you sure? (y/yes to confirm, any other input to cancel)"
            return self.check_input(input, current_step, next_msg, verification, error_msg, change_var, confirmation_msg)
        elif self.creation_progress == CharacterCompletion.INSPIRATION:
            current_step = CharacterCompletion.PROFICIENCY_MODIFIER
            next_msg = "Enter the skill values of your character, in the given order, separated with commas: " + ", ".join(skills_list)
            verification = lambda str : re.fullmatch("-?\\d+") is not None
            error_msg = "Input must be an integer! Try again:"
            change_var = self.set_proficiency_modifier
            confirmation_msg = "Your character's Proficiency Modifier will be {}, are you sure? (y/yes to confirm, any other input to cancel)"
            return self.check_input(input, current_step, next_msg, verification, error_msg, change_var, confirmation_msg)
        elif self.creation_progress == CharacterCompletion.PROFICIENCY_MODIFIER:
            current_step = CharacterCompletion.SKILLS
            next_msg = "Enter the proficiencies of your character (separated by commas): "
            verification = lambda str : re.fullmatch("(-?\\d+\\s*,\\s*){17}-?\\d+\\s*") is not None
            error_msg = "Input must be a list of 18 integers! Try again:"
            change_var = self.set_skills
            confirmation_msg = "Your character's skills will be `{}`, are you sure? (y/yes to confirm, any other input to cancel)"
            return self.check_input(input, current_step, next_msg, verification, error_msg, change_var, confirmation_msg)
        elif self.creation_progress == CharacterCompletion.SKILLS:
            current_step = CharacterCompletion.PROFICIENCIES
            next_msg = "Enter the languages of your character (separated by commas): "
            verification = lambda str : True
            error_msg = ""
            change_var = self.set_proficiencies
            confirmation_msg = "Your character's proficiencies will be `{}`, are you sure? (y/yes to confirm, any other input to cancel)"
            return self.check_input(input, current_step, next_msg, verification, error_msg, change_var, confirmation_msg)
        elif self.creation_progress == CharacterCompletion.PROFICIENCIES:
            current_step = CharacterCompletion.LANGUAGES
            next_msg = "Enter the other proficiencies of your character, in the format `[Title1]: [Description1],, [Title2]: [Description2]` and so on: (\"None\" if there are none)"
            verification = lambda str : True
            error_msg = ""
            change_var = self.set_languages
            confirmation_msg = "Your character's proficiencies will be `{}`, are you sure? (y/yes to confirm, any other input to cancel)"
            return self.check_input(input, current_step, next_msg, verification, error_msg, change_var, confirmation_msg)
        elif self.creation_progress == CharacterCompletion.LANGUAGES:
            current_step = CharacterCompletion.OTHER_PROFICIENCIES
            next_msg = "Enter the amount of starting wealth of your character (in the format of `[CP] [SP] [EP] [GP] [PP]`:"
            verification = lambda str : str == "None" or re.fullmatch("(.+,.+|)*.+,.+") is not None
            error_msg = "Incorrect format! Try again:"
            change_var = self.set_other_proficiencies
            confirmation_msg = "Your character's other proficiencies will be `{}`, are you sure? (y/yes to confirm, any other input to cancel)"
            return self.check_input(input, current_step, next_msg, verification, error_msg, change_var, confirmation_msg)
        elif self.creation_progress == CharacterCompletion.OTHER_PROFICIENCIES:
            current_step = CharacterCompletion.CURRENCY
            next_msg = "Enter the current inventory of the character (separated by commas):"
            verification = lambda str : re.fullmatch("\\d+\\s+\\d+\\s+\\d+\\s+\\d+\\s+\\d+") is not None
            error_msg = "Incorrect format! Make sure it is in [CP] [SP] [EP] [GP] [PP]. Try again:"
            change_var = self.set_currency
            confirmation_msg = "Your character's starting wealth will be `{}`, are you sure? (y/yes to confirm, any other input to cancel)"
            return self.check_input(input, current_step, next_msg, verification, error_msg, change_var, confirmation_msg)
        elif self.creation_progress == CharacterCompletion.CURRENCY:
            current_step = CharacterCompletion.INVENTORY
            next_msg = "Enter the attacks that the character has, in the format `[name], [atk bonus], [damage], [other descriptions] | [name], [atk bonus], [damage], [other descriptions]` etc.:"
            verification = lambda str : True
            error_msg = "Incorrect format! Try again:"
            change_var = self.set_inventory
            confirmation_msg = "Your character's inventory will be {}, are you sure? (y/yes to confirm, any other input to cancel)"
            return self.check_input(input, current_step, next_msg, verification, error_msg, change_var, confirmation_msg)
        elif self.creation_progress == CharacterCompletion.INVENTORY:
            current_step = CharacterCompletion.ATTACKS
            next_msg = "Enter the other attacks of your character, in the format `[Title1]: [Description1],, [Title2]: [Description2]` and so on: (\"None\" if there are none)"
            verification = lambda str : str == "None" or re.fullmatch("(.+,.+,.+,.+|)*.+,.+,.+,.+") is not None
            error_msg = "Incorrect format! Try again, and remember that it should be in the format `[name], [atk bonus], [damage], [other descriptions] | [name], [atk bonus], [damage], [other descriptions]`:"
            change_var = self.set_attacks
            confirmation_msg = "Your character's attacks will be `{}`, are you sure? (y/yes to confirm, any other input to cancel)"
            return self.check_input(input, current_step, next_msg, verification, error_msg, change_var, confirmation_msg)
        elif self.creation_progress == CharacterCompletion.ATTACKS:
            current_step = CharacterCompletion.OTHER_ATTACKS
            next_msg = ""
            verification = lambda str : str == "None" or re.fullmatch("(.+,.+|)*.+,.+") is not None
            error_msg = "Incorrect format! Try again:"
            change_var = self.set_other_proficiencies
            confirmation_msg = "Your character's other attacks will be `{}`, are you sure? (y/yes to confirm, any other input to cancel)"
            return self.check_input(input, current_step, next_msg, verification, error_msg, change_var, confirmation_msg)
        elif self.creation_progress == CharacterCompletion.OTHER_ATTACKS:
            self.creation_progress = CharacterCompletion.FINISH
            return "Remaining implementation is unfinished."
        elif self.creation_progress == CharacterCompletion.FLAWS:
            self.creation_progress = CharacterCompletion.FINISH
            return "Character complete!"
        else:
            return "An unknown error has occurred."

    def check_input(self, input, current_step, next_msg, verification, error_msg, change_var, confirmation_msg):
        input_lower = input.lower()
        if self.confirmation: # this is the response to the confirmation message
            self.confirmation = False
            if utils.is_positive_input(input_lower):
                self.creation_progress = current_step
                self.current_message = next_msg
            return self.current_message
        else:
            if not verification(input):
                return error_msg
            change_var(input)
            self.confirmation = True
            return confirmation_msg.format(input)

    # functions to change variables, to pass to check_input
    def set_name(self, val):
        self.name = val

    def set_race(self, val):
        self.race = val

    def set_class(self, val):
        self.chara_class = val

    def set_background(self, val):
        self.background = val

    def set_alignment(self, val):
        self.alignment = val

    def set_level(self, val):
        self.level = int(val)

    def set_exp(self, val):
        self.exp = int(val)

    # in the format of STR STR_MOD STR_SAVE, DEX DEX_MOD DEX_SAVE and so on
    def set_stats(self, val):
        vals = re.split("\\s*[(,?)(\\s+)]", val)
        self.str = int(vals[0])
        self.str_mod = int(vals[1])
        self.str_save = int(vals[2])
        self.dex = int(vals[3])
        self.dex_mod = int(vals[4])
        self.dex_save = int(vals[5])
        self.cop = int(vals[6])
        self.cop_mod = int(vals[7])
        self.cop_save = int(vals[8])
        self.int = int(vals[9])
        self.int_mod = int(vals[10])
        self.int_save = int(vals[11])
        self.wis = int(vals[12])
        self.wis_mod = int(vals[13])
        self.wis_save = int(vals[14])
        self.cha = int(vals[15])
        self.cha_mod = int(vals[16])
        self.cha_save = int(vals[17])

    def set_inspiration(self, val):
        self.inspiration = int(val)

    def set_proficiency_bonus(self, val):
        self.proficiency_bonus = int(val)

    # in the format [Acrobatics], [Animal Handling] and so on
    def set_skills(self, val):
        vals = list(map(lambda str : int(str), re.split("\\s*,\\s*", val)))
        self.skills = zip(skills_list, vals)
        self.passive_perception = skills["Perception"] + 10

    # in the format [proficiency], [proficiency] etc.
    def set_proficiencies(self, val):
        self.proficiencies = re.split("\\s*,\\s*", val)

    # in the format [language], [language] etc.
    def set_languages(self, val):
        self.languages = re.split("\\s*,\\s*", val)

    # in the format [Title]: [Description],, [Title]: [Description] and so on
    def set_other_proficiencies(self, val):
        vals = re.split("\\s*,,\\s*", val)
        for str in vals:
            i = vals.index(":")
            self.other_proficiencies.append(Description(vals[:i], vals[i + 1:].strip()))

    # in the format [CP] [SP] [EP] [GP] [PP]
    def set_currency(self, val):
        self.currency = list(map(lambda str : int(str), re.split(" +", val)))

    # in the format [item], [item] and so on
    def set_inventory(self, val):
        self.inventory = re.split("\\s*,\\s*", val)

    # in the format [name], [atk bonus], [damage], [other descriptions] | [name], [atk bonus], [damage], [other descriptions] etc.
    def set_attacks(self, val):
        vals = re.split("\\s*|\\s*", val)
        for atk in vals:
            components = re.split("\\s*,\\s*", atk)
            self.attacks.append(Attack(components[0], int(components[1]), components[2], components[3]))

    # in the format [Name]: [Description],, [Name]: [Description] and so on
    def set_other_attacks(self, val):
        vals = re.split("\\s*,,\\s*", val)
        for str in vals:
            i = vals.index(":")
            self.other_attacks.append(Description(vals[:i], vals[i + 1:].strip()))
    
    def set_armor_class(self, val):
        self.armor_class = int(val)
        
    def set_initiative_modifier(self, val):
        self.initiative_modifier = int(val)
        
    def set_speed(self, val):
        self.speed = int(val)
        
    # in the format [#]d[sides]
    def set_hit_dice(self, val):
        i = val.index("d")
        self.hit_dice = Dice(int(val[:i]), int(val[i + 1:]))
        
    def set_max_hp(self, val):
        self.max_hp = int(val)
        
    def set_current_hp(self, val):
        self.current_hp = int(val)
        
    # in the format [success] [failure]
    def set_death_saves(self, val):
        vals = re.split(" +", val)
        self.death_save_success = int(vals[0])
        self.death_save_failure = int(vals[1])
        
    # in the format [Name]: [Description],, [Name]: [Description] and so on
    def set_features(self, val):
        vals = re.split("\\s*,,\\s*", val)
        for str in vals:
            i = vals.index(":")
            self.features.append(Description(vals[:i], vals[i + 1:].strip()))

    def set_personality_trait(self, val):
        self.personality_trait = val

    def set_ideals(self, val):
        self.ideals = val

    def set_bonds(self, val):
        self.bonds = val

    def set_flaws(self, val):
        self.flaws = val

    def __str__(self):
        # Character sheet

        # returns str of character stats

        #Hit_dice = hit_dice.sides in str so hit_dice must not be none

        #Is death save successs/fail supposed to be printed like that


        chara_str = 'Name: {} \
                    \nClass: {} \
                    \nLevel: {}\
                    \nBackground: {}\
                    \nPlayer Name: {}\
                    \nRace: {}\
                    \nExp: {} \
                    \n\nStrength: {} Mod: {} Save: {}\
                    \nDexterity: {} Mod: {} Save: {}\
                    \nConstitution: {} Mod: {} Save: {}\
                    \nIntelligence: {} Mod: {} Save: {}\
                    \nWisdom: {} Mod: {} Save: {}\
                    \nCharisma: {} Mod: {} Save: {}\
                    \n\nInspiration: {}\
                    \nProficiency Bonus: {}\
                    \nPassive Perception: {}\
                    \n\nLanguages:  {}\
                    \nProficiencies: {}\
                    \nOther Proficiencies: {} \
                    \n\nCurrency: \
                    \nCP: {}\
                    \nSP: {}\
                    \nEP: {}\
                    \nGP: {}\
                    \nPP: {} \
                    \n\nInventory: {}\
                    \nAttacks: {}\
                    \nOther Attacks: {}\
                    \n\nInitiative Modifier: {}\
                    \nSpeed: {}\
                    \nHit Dice: {}\
                    \nMax HP: {}\
                    \nCurrent HP: {}\
                    \nDeath Save Successes: {}\
                    \nDeath Save Failures: {}\
                    \n\nFeatures: {}\
                    \n\nPersonality Trait: {}\
                    \nIdeals: {}\
                    \nBonds: {}\
                    \nFlaws: {}' \
            .format(self.name, self.chara_class, self.level, self.background, self.player_name, self.race,
                    self.exp,
                    self.str, self.str_mod, self.str_save, self.dex, self.dex_mod, self.dex_save, self.con,
                    self.con_mod, self.con_save,
                    self.int, self.int_mod, self.int_save, self.wis, self.wis_mod, self.wis_save, self.cha,
                    self.cha_mod, self.cha_save,
                    self.inspiration, self.proficiency_bonus, self.passive_perception,
                    str([*self.languages.values()]).replace("'", '').replace('[', '').replace(']', ''),
                    str([*self.proficiencies.values()]).replace("'", '').replace('[', '').replace(']', ''),
                    str([*self.other_proficiencies.values()]).replace("'", '').replace('[', '').replace(']', '')
                    , self.currency[0],
                    self.currency[1], self.currency[2], self.currency[3], self.currency[4],
                    str([*self.inventory.values()]).replace("'", '').replace('[', '').replace(']', ''),
                    str([*self.attacks.values()]).replace("'", '').replace('[', '').replace(']', ''),
                    str([*self.other_attacks.values()]).replace("'", '').replace('[', '').replace(']', ''),
                    self.initiative_modifier, self.speed, self.hit_dice.sides, self.max_hp, self.current_hp,
                    self.death_save_success, self.death_save_failure,
                    str([*self.features.values()]).replace("'", '').replace('[', '').replace(']', ''),
                    self.personality_trait, self.ideals, self.bonds, self.flaws)

        return chara_str