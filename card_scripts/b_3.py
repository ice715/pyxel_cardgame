from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Amodeus"
        self.attribute = "b"
        self.lv = 3 
        self.atk = 4 
        self.max_hp = 3
        self.hp = self.max_hp
        self.get_design_address()
    
    def on_summon(self):
        super().on_summon()
        for card in self.owner.field:
            card.atk = max(card.atk - 1, 0)
            card.max_hp = max(card.max_hp - 1, 1)
            card.hp =  max(card.hp - 1, 0)

