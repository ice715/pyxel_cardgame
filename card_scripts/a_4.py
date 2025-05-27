from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Kamael"
        self.lv = 3
        self.attribute = "a"
        self.atk = 5
        self.max_hp = 4
        self.hp = self.max_hp
        self.get_design_address()
    
    def summon(self):
        super().summon()
        self.owner.hp += 3
    