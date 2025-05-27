from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Amodeus"
        self.attribute = "b"
        self.lv = 3 
        self.atk = 3 
        self.max_hp = 3
        self.hp = self.max_hp
        self.get_design_address()
    