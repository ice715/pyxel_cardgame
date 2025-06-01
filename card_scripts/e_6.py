from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Alice"
        self.lv = 6
        self.attribute = "e"
        self.atk = 6
        self.max_hp = 7
        self.hp = self.max_hp
        self.get_design_address()
    
    def on_summon(self):
        super().on_summon()
        for card in self.owner.field:
            if (card is None) or (card is self): continue
            card.attack *= 2
            card.hp *= 2
        for card in self.owner.opponent.field:
            if card is None: continue
            card.attack = int(card.attack / 2)
            card.hp = int(card.hp / 2)

