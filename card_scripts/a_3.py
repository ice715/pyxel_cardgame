from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Gabriel"
        self.lv = 3
        self.attribute = "a"
        self.atk = 6
        self.max_hp = 5
        self.hp = self.max_hp
        self.get_design_address()
    
    def summon(self):
        super().summon()
        self.owner.hp += 3
    