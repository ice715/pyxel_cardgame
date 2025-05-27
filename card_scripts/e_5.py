from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Odin"
        self.lv = 5
        self.attribute = "e"
        self.atk = 5
        self.max_hp = 5
        self.hp = self.max_hp
        self.get_design_address()

