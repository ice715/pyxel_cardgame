from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Behemoth"
        self.lv = 7
        self.attribute = "c"
        self.atk = 8
        self.max_hp = 7
        self.hp = self.max_hp
        self.get_design_address()

    def attack(self, target):
        if self.attackable:
            for card in self.owner.opponent.field:
                if card is None: continue
                self.deal_damage(self.atk, card)
        super().attack(target)

    def destruction(self):
        if self.hp <= 0:
            self.owner.hp += self.atk
        super().destruction()