from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Uriel"
        self.lv = 6
        self.attribute = "a"
        self.atk = 6
        self.max_hp = 7
        self.hp = self.max_hp
        self.get_design_address()
    