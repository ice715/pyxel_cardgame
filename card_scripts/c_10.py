from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Dragon"
        self.lv = 10
        self.attribute = "c"
        self.atk = 13
        self.max_hp = 13
        self.hp = self.max_hp
        self.get_design_address()

    def summon(self):
        super().summon()
        self.attackable = True
    