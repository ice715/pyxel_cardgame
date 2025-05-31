from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "CuChulainn"
        self.lv = 1
        self.attribute = "e"
        self.atk = 2
        self.max_hp = 1
        self.hp = self.max_hp
        self.get_design_address()
    
    def attack(self, target):
        super().attack(target)
        if target.hp < 0:
            self.owner.opponent.hp += target.hp
