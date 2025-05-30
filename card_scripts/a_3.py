import random
from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Gabriel"
        self.lv = 3
        self.attribute = "a"
        self.atk = 2
        self.max_hp = 3
        self.hp = self.max_hp
        self.get_design_address()
    
    def on_summon(self):
        super().on_summon()
        if self.owner.graveyard:
            card = random.choice(self.owner.graveyard)
            card.reborn()
    