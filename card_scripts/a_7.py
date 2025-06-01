from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Raphael"
        self.lv = 7
        self.attribute = "a"
        self.atk = 7 
        self.max_hp = 8
        self.hp = self.max_hp
        self.get_design_address()
    
