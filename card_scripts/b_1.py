from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Adramelech"
        self.attribute = "b"
        self.lv = 1
        self.atk = 1
        self.max_hp = 2
        self.hp = self.max_hp

        self.get_design_address()
    
    def attack(self, target):
        if self.attackable:
            self.deal_damage(self.atk, self.owner.opponent)
        super().attack(target)
        