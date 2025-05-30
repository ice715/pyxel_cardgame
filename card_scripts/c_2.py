from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "phoenix"
        self.lv = 2
        self.attribute = "c"
        self.atk = 1
        self.max_hp = 1
        self.hp = self.max_hp
        self.rebornable = False
        self.get_design_address()
    
    def on_summon(self):
        super().on_summon()
        self.rebornable = False
    
    def destruction(self):
        if self.hp <= 0:
            self.rebornable = True
        super().destruction()
    
    def discard(self):
        super().discard()
        self.rebornable = False
    
    def turn_end(self):
        if self.rebornable and (self in self.owner.graveyard):
            self.reborn()
            self.rebornable = False
    