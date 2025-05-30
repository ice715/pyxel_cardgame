from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Ramiel"
        self.lv = 2
        self.attribute = "a"
        self.atk = 1
        self.max_hp = 1
        self.hp = self.max_hp
        self.get_design_address()
    
    def attacked(self, target):
        self.hp += 1
        return super().attacked(target)
        
    