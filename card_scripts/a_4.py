from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Kamael"
        self.lv = 4
        self.attribute = "a"
        self.atk = 4
        self.max_hp = 5
        self.hp = self.max_hp
        self.get_design_address()
    
    def on_summon(self):
        super().on_summon()
        for card in self.owner.field:
            if card is None: continue
            card.atk += 1
    