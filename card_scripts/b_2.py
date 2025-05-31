from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Naamah"
        self.attribute = "b"
        self.lv = 2
        self.atk = 1
        self.max_hp = 1
        self.hp = self.max_hp
        self.get_design_address()
    
    def attack(self, target):
        return super().attack(target)