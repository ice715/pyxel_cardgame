from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Astaroth"
        self.attribute = "b"
        self.lv = 10 
        self.atk = 12 
        self.max_hp = 12
        self.hp = self.max_hp
        self.get_design_address()
    