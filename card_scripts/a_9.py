import random
from card import Card
from utils import len_with_out_none, import_real_card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Lucifer"
        self.lv = 9
        self.attribute = "a"
        self.atk = 10 
        self.max_hp = 9 
        self.hp = self.max_hp
        self.get_design_address()
    
    def on_fusion(self):
        super().on_fusion()

        residual_size = self.owner.max_field_size - len_with_out_none(self.owner.field) 
        angel_cards_in_graveyard = [card for card in self.owner.graveyard if card.attribute == "a"]
        while (residual_size > 0) and angel_cards_in_graveyard:
            card = random.choice(angel_cards_in_graveyard)
            card.reborn()
        for card in self.owner.field:
            if card is None: continue
            if card.attribute == "a":
                lv = card.lv
                new_card = import_real_card('a', lv, self.owner)
                card.animation_queue.append(("metamorphose", (new_card,)))
                

