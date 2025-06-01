import random 
from card import Card
from utils import len_with_out_none, get_no_used_card_lst, import_real_card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Norun"
        self.lv = 8
        self.attribute = "e"
        self.atk = 8
        self.max_hp = 9
        self.hp = self.max_hp
        self.get_design_address()
    
    # Verdandi
    def attacked(self, target):
        super().attack(target)
        if (self.owner.deck) and (len_with_out_none(self.owner.field) < self.owner.max_field):
            target_idx = random.randint(0, len(self.owner.deck) - 1)
            card = self.owner.deck.pop(target_idx)
            card.summon()

    # Urd
    def on_summon(self):
        super().on_summon()
        card = random.choice(self.owner.graveyard)
        card.reborn()

    # Skuld
    def destruction(self):
        if self.hp > 0:
            pass
        else:
            no_used_card_lst = get_no_used_card_lst(self.owner, self.owner.opponent)
            if no_used_card_lst:
                attribute, lv = random.choice(no_used_card_lst)
                card = import_real_card(attribute, lv, owner=self.owner)
                card.summon()
        super().destruction()

