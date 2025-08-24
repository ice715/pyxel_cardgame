from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Bael"
        self.attribute = "b"
        self.lv = 5
        self.atk = 6
        self.max_hp = 5
        self.hp = self.max_hp
        self.get_design_address()
    