from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Odin"
        self.lv = 5
        self.attribute = "e"
        self.atk = 6
        self.max_hp = 5
        self.hp = self.max_hp
        self.get_design_address()
    
    def on_fusion(self):
        super().on_fusion()
        self.deal_damage(5, self.owner)
        self.owner.max_n_summon += 1
        self.owner.max_n_fusion += 1
    

