from card import Card

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Hydra"
        self.lv = 9
        self.attribute = "c"
        self.atk = 2
        self.max_hp = 9
        self.hp = self.max_hp
        self.max_attack = 9
        self.attack_cnt = 0
        self.get_design_address()
    
    def attack(self, target):
        if self.attackable:
            super().attack(target)
            if self.attack_cnt <= self.max_attack:
                self.attackable = True
    
    def on_summon(self):
        super().on_summon()
        self.attack_cnt = 0
    
    def turn_end(self):
        super().turn_end()
        self.attack_cnt = 0
    
    def discard(self):
        super().discard()
        self.attack_cnt = 0
    
    def destruction(self):
        super().destruction()
        self.attack_cnt = 0
        
