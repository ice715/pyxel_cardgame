from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "angel"
        self.lv = 1
        self.attribute = "a"
        self.atk = 1
        self.max_hp = 2
        self.hp = self.max_hp
        self.get_design_address()
    
    def on_summon(self):
        super().on_summon()
        self.owner.hp += self.atk
    
    def on_fusion(self):
        super().on_fusion()
        self.on_summon()
    