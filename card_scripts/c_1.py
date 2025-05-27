from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "chimera"
        self.lv = 1
        self.attribute = "c"
        self.atk = 2
        self.max_hp = 1
        self.hp = self.max_hp
        self.get_design_address()

    def summon(self):
        super().summon()
        self.attackable = True
    