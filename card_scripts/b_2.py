from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Naamah"
        self.attribute = "b"
        self.lv = 2
        self.atk = 3
        self.max_hp = 2
        self.hp = self.max_hp
        self.get_design_address()
    
    def attacked(self, target):
        super().attacked(target)
        self.function_queue.append((self.owner.fusion, (self, target)))