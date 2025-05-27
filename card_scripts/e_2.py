from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Artemis"
        self.lv = 2
        self.attribute = "e"
        self.atk = 3
        self.max_hp = 2
        self.hp = self.max_hp
        self.get_design_address()
    
    def attack(self, target):
        if self.attackable:
            super().attack(target)
            if isinstance(target, Card) and (target.attribute == "c"):
                target.hp = 0
    

