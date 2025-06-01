import random
from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "pegasus"
        self.lv = 8
        self.attribute = "c"
        self.atk = 8
        self.max_hp = 9
        self.hp = self.max_hp
        self.get_design_address()

    def on_summon(self):
        super().on_summon()
        # search
        search_candidate_idx_lst = [idx for idx, card in enumerate(self.owner.deck) if card.attribute == "e"]
        if search_candidate_idx_lst:
            search_idx = random.choice(search_candidate_idx_lst)
            search_card = self.owner.deck.pop(search_idx)
            self.owner.deck.insert(0, search_card)  # put the searched card on top of the deck
            self.owner.one_card_deck2hand()
        self.owner.n_summon += 1
    