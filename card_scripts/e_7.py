from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Nyalathotep"
        self.lv = 7
        self.attribute = "e"
        self.atk = 1
        self.max_hp = 1
        self.hp = self.max_hp
        self.get_design_address()

    def trade_owner(self, target):
        if isinstance(target, Card):
            new_owner = target.owner
            target.owner = self.owner
            target.discard()
            self.owner = new_owner
            self.discard()

    def attack(self, target):
        super().attack(target)
        self.trade_owner(target)
    
    def attacked(self, target):
        super().attacked(target)
        self.trade_owner(target)
        





