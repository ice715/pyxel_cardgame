from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Viṣṇu"
        self.lv = 9
        self.attribute = "e"
        self.atk = 10
        self.max_hp = 10
        self.hp = self.max_hp
        self.get_design_address()

