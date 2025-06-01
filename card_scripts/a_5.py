import random
from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Zerachiel"
        self.lv = 5
        self.attribute = "a"
        self.atk = 5 
        self.max_hp = 6
        self.hp = self.max_hp
        self.get_design_address()
    
    def on_summon(self):
        super().on_summon()
        min_lv_in_hand = min([card.lv for card in self.owner.hand if card is not None], default=0)
        if min_lv_in_hand > 0:
            card = random.choice([card for card in self.owner.hand if (card is not None) & card.lv == min_lv_in_hand])
            card.animation = "vanish"
