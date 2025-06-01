from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Michael"
        self.lv = 8
        self.attribute = "a"
        self.atk = 8
        self.max_hp = 9 
        self.hp = self.max_hp
        self.get_design_address()
    
    def on_summon(self):
        super().on_summon()
        for card in self.owner.field:
            if card is None: continue
            card.attackable = True
    