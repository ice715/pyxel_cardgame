from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Behemoth"
        self.lv = 7
        self.attribute = "c"
        self.atk = 7
        self.max_hp = 7
        self.hp = self.max_hp
        self.get_design_address()

    def summon(self):
        super().summon()
        self.attackable = True
    