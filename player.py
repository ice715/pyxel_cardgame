import random 

from cfg import HEIGHT, WIDTH
from utils import add_or_replace_none, get_fusion_card, get_init_deck, get_init_deck_debug, len_with_out_none

class Player:
    def __init__(self, debug=False):
        self.hp = 20
        self.n_turn_draw = 3
        self.max_n_summon = 1
        self.n_summon = self.max_n_summon
        self.max_n_fusion = 1
        self.n_fusion = self.max_n_fusion

        self.x = WIDTH//2
        self.y = HEIGHT

        self.is_real = True

        if debug:
            self.deck = get_init_deck_debug(owner=self)  # 初期デッキ
        else:
            self.deck = get_init_deck(owner=self)  # 初期デッキ
        random.shuffle(self.deck)
        self.hand = []

        self.max_field_size = 5
        self.field = []
        self.graveyard = []
        self.opponent = None

    def play_card(self, card_index):
        if self.n_summon <= 0:
            pass
        elif len_with_out_none(self.field) >= self.max_field_size:
            pass
        elif not self.is_real:
            self.hand[card_index].summon_from_hand()
        else:
            self.hand[card_index].animation = "hand2field"
            self.hand[card_index].animation_progress = 0

    def fusion(self, card1, card2):
        if self.n_fusion <= 0:
            return None
        else:
            new_card = get_fusion_card(card1, card2, owner=self)
            card1.animation = "destruction"
            card2.animation = "destruction"
            add_or_replace_none(self.field, new_card)
            new_card.animation = "fusion"
            new_card.alpha = 0
            self.n_fusion -= 1
            return new_card

    def one_card_deck2hand(self):
        if not self.deck:
            self.deck = self.graveyard
            random.shuffle(self.deck)
            self.graveyard = []   
        if self.deck:
            pop_card = self.deck.pop(0)
            pop_card.animation = "draw"
            pop_card.animation_progress = 0  # アニメーションの進行度を初期化
            add_or_replace_none(self.hand, pop_card)

    def reset_hand(self):
        self.hand = []
        for _ in range(self.n_turn_draw):
            self.one_card_deck2hand()

    def turn_start(self):
        self.n_summon = self.max_n_summon
        self.n_fusion = self.max_n_fusion
        for card in (self.field + self.hand + self.graveyard):
            if card is None: continue
            card.turn_start()
        self.reset_hand()

    def turn_end(self):
        self.selected_attacker = None
        for card in (self.hand + self.field + self.graveyard):
            if card is None: continue
            card.turn_end()
        
        for card in self.hand:
            if card is None: continue
            card.animation = "discard"

class Opponent(Player):
    def __init__(self):
        super().__init__()
        self.actions = []

        self.is_real = False
        self.x = WIDTH//2
        self.y = 0

    def play_turn(self):
        self.actions = []
        # カードをプレイ
        effective_hand_idx_lst = [i for i, card in enumerate(self.hand) if card is not None]
        if effective_hand_idx_lst:
            self.actions.append(('play_card', effective_hand_idx_lst[0]))

        # 攻撃
        effective_field_lst = [card for i, card in enumerate(self.field) if card is not None]
        for card in effective_field_lst:
            if card.attackable:
                self.actions.append(('attack', card))
    
    def execute_action(self):
        if not self.actions:
            return True

        action = self.actions.pop(0)
        if action[0] == 'play_card':
            self.play_card(action[1])
            
        elif action[0] == 'attack':
            opp_field_lst = [opp_card for opp_card in self.opponent.field if opp_card is not None]
            
            if opp_field_lst:
                action[1].attack(opp_field_lst[0])
            
            elif action[0] == 'direct_attack':
                action[1].attack(self.opponent)

        return False
