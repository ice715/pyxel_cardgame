from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Belial"
        self.attribute = "b"
        self.lv = 7
        self.atk = 8
        self.max_hp = 7
        self.hp = self.max_hp
        self.get_design_address()
    