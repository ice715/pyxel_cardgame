from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Lucifugus"
        self.attribute = "b"
        self.lv = 4
        self.atk = 4
        self.max_hp = 4
        self.hp = self.max_hp
        self.get_design_address()
    