from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Isis"
        self.lv = 4
        self.attribute = "e"
        self.atk = 4
        self.max_hp = 5
        self.hp = self.max_hp
        self.get_design_address()
    
    def on_fusion(self):
        super().on_fusion()
        self.owner.n_turn_draw += 1

    def on_summon(self):
        super().on_summon()
        for _ in range(self.lv):
            self.owner.one_card_deck2hand()

