class Player:
    def __init__(self, name="主角", level=1, realm="练气期"):
        self.name = name
        self.level = level
        self.realm = realm
        self.hp = 100
        self.max_hp = 100
        self.mp = 50
        self.max_mp = 50
        self.attack = 20
        self.defense = 10
        self.speed = 15
        self.skills = ["剑斩", "火球术"]
        self.inventory = []
    
    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "realm": self.realm,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "mp": self.mp,
            "max_mp": self.max_mp,
            "attack": self.attack,
            "defense": self.defense,
            "speed": self.speed,
            "skills": self.skills,
            "inventory": self.inventory
        }
    
    def from_dict(self, data):
        self.name = data.get("name", "主角")
        self.level = data.get("level", 1)
        self.realm = data.get("realm", "练气期")
        self.hp = data.get("hp", 100)
        self.max_hp = data.get("max_hp", 100)
        self.mp = data.get("mp", 50)
        self.max_mp = data.get("max_mp", 50)
        self.attack = data.get("attack", 20)
        self.defense = data.get("defense", 10)
        self.speed = data.get("speed", 15)
        self.skills = data.get("skills", ["剑斩", "火球术"])
        self.inventory = data.get("inventory", [])
        return self
    
    def attack_enemy(self, enemy):
        damage = max(1, self.attack - enemy.defense)
        enemy.hp = max(0, enemy.hp - damage)
        return damage
    
    def use_skill(self, skill_name, enemy):
        if skill_name == "剑斩":
            damage = max(1, self.attack * 1.5 - enemy.defense)
            enemy.hp = max(0, enemy.hp - damage)
            return damage
        elif skill_name == "火球术":
            if self.mp >= 10:
                self.mp -= 10
                damage = max(1, self.attack * 2 - enemy.defense)
                enemy.hp = max(0, enemy.hp - damage)
                return damage
            else:
                return 0
        return 0
