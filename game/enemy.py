class Enemy:
    def __init__(self, name, level, hp, attack, defense, speed):
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
    
    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "attack": self.attack,
            "defense": self.defense,
            "speed": self.speed
        }
    
    def from_dict(self, data):
        self.name = data.get("name", "敌人")
        self.level = data.get("level", 1)
        self.hp = data.get("hp", 50)
        self.max_hp = data.get("max_hp", 50)
        self.attack = data.get("attack", 10)
        self.defense = data.get("defense", 5)
        self.speed = data.get("speed", 10)
        return self
    
    def attack_player(self, player):
        damage = max(1, self.attack - player.defense)
        player.hp = max(0, player.hp - damage)
        return damage
