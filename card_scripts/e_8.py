from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Norun"
        self.lv = 8
        self.attribute = "e"
        self.atk = 8
        self.max_hp = 8
        self.hp = self.max_hp
        self.get_design_address()

