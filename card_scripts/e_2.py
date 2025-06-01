from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Artemis"
        self.lv = 2
        self.attribute = "e"
        self.atk = 2
        self.max_hp = 3
        self.hp = self.max_hp
        self.get_design_address()
    
    def attack(self, target):
        if self.attackable:
            super().attack(target)
            if isinstance(target, Card) and (target.attribute == "c"):
                target.animation = "destruction"

    def on_summon(self):
        super().on_summon()
        for card in self.owner.opponent.field:
            if card is None: continue
            if card.attribute == "c":
                self.deal_damage(0, card)
                card.animation = "destruction"


