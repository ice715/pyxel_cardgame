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
        self.attackable = True
        self.get_design_address()

    def on_summon(self):
        super().on_summon()
        self.attackable = True