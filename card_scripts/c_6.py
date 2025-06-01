from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Unicorn"
        self.lv = 6
        self.attribute = "c"
        self.atk = 6
        self.max_hp = 7
        self.hp = self.max_hp
        self.get_design_address()

    def on_summon(self):
        super().on_summon()
        for card in self.owner.field + self.owner.opponent.field:
            if card is None: continue
            if card.hp < card.max_hp:
                card.animation = "destruction"
    