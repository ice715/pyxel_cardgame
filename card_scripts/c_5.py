from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Leviathan"
        self.lv = 5
        self.attribute = "c"
        self.atk = 6
        self.max_hp = 5
        self.hp = self.max_hp
        self.get_design_address()

    def attacked(self, target):
        self.hp = self.max_hp
        super().attacked(target)
    
    def destruction(self):
        if self.hp <= 0:
            self.owner.hp += self.atk
        super().destruction()