from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Satan"
        self.attribute = "b"
        self.lv = 9 
        self.atk = 9
        self.max_hp = 10
        self.hp = self.max_hp
        self.get_design_address()
    