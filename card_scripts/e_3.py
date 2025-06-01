from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Siegfried"
        self.lv = 3
        self.attribute = "e"
        self.atk = 4
        self.max_hp = 3
        self.hp = self.max_hp
        self.get_design_address()
    
    def attack(self, target):
        if self.attackable:
            super().attack(target)
            self.hp = min(self.max_hp, self.hp + self.atk)
            
