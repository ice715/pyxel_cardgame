# cardgame.py

import random
import pyxel
from player import Player, Opponent
from cfg import WIDTH, HEIGHT, DEBUG
from utils import len_with_out_none, judge_counter_attribute

class Game:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="Turn-Based Card Game")
        self.reset_game()
        pyxel.load("assets/design.pyxres")
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.player = Player(debug=DEBUG)
        self.opponent = Opponent()
        self.turn_player = random.choice([self.player, self.opponent])
        
        self.player.opponent = self.opponent
        self.opponent.opponent = self.player

        self.selecting_space = self.player.hand
        self.selecting_space_idx = 0

        self.selected_card_idx = 0
        self.selected_card = None

        self.selected_attacker = None
        self.game_over = False

        self.cpu_action_delay = 10
        self.cpu_action_timer = 10

        self.draw_status = False
        
        self.turn_player.turn_start()
        if self.turn_player is self.opponent:
            self.turn_player.play_turn()
    
    def update(self):
        if self.player.hp <= 0 or self.opponent.hp <= 0:
            self.game_over = True

        if self.game_over:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.reset_game()
            return
        
        for card in self.player.field + self.opponent.field:
            if card is None:
                continue
            if (card.hp <= 0) and (card.animation in ["destruction", None]) and (not card.attack_animation):
                card.animation = "destruction"

        if self.turn_player is self.opponent:
            if self.cpu_action_timer > 0:
                self.cpu_action_timer -= 1
            else:
                if self.opponent.execute_action():
                    self.end_turn()
                    self.turn_player = self.player
                    self.start_turn()
                self.cpu_action_timer = self.cpu_action_delay

        self.space_lst = [self.player.hand, self.player.field, self.opponent.field]
        # effective_space_idx_lst = [i for i, v in enumerate(self.space_lst) if len_with_out_none(v)]
        effective_space_lst = [sp for sp in self.space_lst  if len_with_out_none(sp) > 0]
        if pyxel.btnp(pyxel.KEY_UP):
            self.selecting_space_idx = (self.selecting_space_idx + 1) % max(len(effective_space_lst), 1)
            # self.selecting_space = self.space_lst[effective_space_idx_lst[self.selecting_space_idx]]
            if effective_space_lst:
                self.selecting_space = effective_space_lst[self.selecting_space_idx]
                self.selected_card_idx = 0

        if pyxel.btnp(pyxel.KEY_DOWN):
            self.selecting_space_idx = (self.selecting_space_idx - 1) % max(len(effective_space_lst), 1)
            # self.selecting_space = self.space_lst[effective_space_idx_lst[self.selecting_space_idx]]

            if effective_space_lst:
                self.selecting_space = effective_space_lst[self.selecting_space_idx]
                self.selected_card_idx = 0

        effective_idx_lst = [i for i, v in enumerate(self.selecting_space) if v is not None]
        if pyxel.btnp(pyxel.KEY_LEFT):
            if not effective_idx_lst:
                pass
            elif self.selected_card is None:
                self.selected_card_idx = effective_idx_lst[0]
            else:
                self.selected_card_idx = (self.selected_card_idx - 1) % max(len(effective_idx_lst), 1)

        if pyxel.btnp(pyxel.KEY_RIGHT):
            if not effective_idx_lst:
                pass
            elif self.selected_card is None:
                self.selected_card_idx = effective_idx_lst[0]
            else:
                self.selected_card_idx = (self.selected_card_idx + 1) % max(len(effective_idx_lst), 1)

        if self.selected_card_idx < len(effective_idx_lst):
            self.selected_card = self.selecting_space[effective_idx_lst[self.selected_card_idx]]
        else:
            self.selected_card = None

        if (self.turn_player is self.player) & pyxel.btnp(pyxel.KEY_SPACE):
            if not self.draw_status:
                print("drawing a card now.")
                pass
            
            elif self.selected_card in self.player.hand:
                self.player.play_card(self.selected_card_idx)
                print(f"Playing card: {self.selected_card.name}")
                if self.selected_card in self.player.field:
                    print('in field')
                if self.selected_card in self.player.hand:
                    print('in hand')
                print('field', self.player.field)
                print('hand', self.player.hand)
            
            elif self.selected_attacker is not None:
                print(f"Attacking with: {self.selected_attacker.name}")
                if (len_with_out_none(self.opponent.field) == 0) & (self.selected_attacker==self.selected_card):
                    # self.player.direct_attack(self.selected_card)
                    self.selected_attacker.attack(self.opponent)
                    self.selected_attacker = None
                elif self.selected_card in self.opponent.field:
                    # self.player.attack(self.selected_attacker, self.selected_card)
                    self.selected_attacker.attack(self.selected_card)
                    self.selected_card = self.selected_attacker
                    self.selected_attacker = None
                elif (self.selected_card in self.player.field) and (self.selected_attacker is not self.selected_card):
                    fusion_card = self.player.fusion(self.selected_attacker, self.selected_card)
                    self.selected_attacker = None
                    if fusion_card is not None:
                        self.selected_card = fusion_card
                    
            elif self.selected_card in self.player.field:
                print(f"Selecting attacker: {self.selected_card.name}")
                self.selected_attacker = self.selected_card

        if (self.turn_player is self.player) & pyxel.btnp(pyxel.KEY_SHIFT):
            if not self.draw_status:
                pass
            elif self.selected_attacker is not None:
                if self.selected_card is self.selected_attacker:
                    self.selected_attacker = None

        if pyxel.btnp(pyxel.KEY_RETURN):
            self.end_turn()

    def start_turn(self):
        self.turn_player.turn_start()

    def end_turn(self):
        self.selected_attacker = None
        self.turn_player.turn_end()
        self.turn_player = self.opponent
        self.opponent.play_turn()

    def draw(self):
        pyxel.cls(3)
        if self.game_over:
            winner = "Player Wins!" if self.opponent.hp <= 0 else "Opponent Wins!"
            pyxel.text(WIDTH // 2 - 30, HEIGHT // 2, winner, 7)
            pyxel.text(WIDTH // 2 - 40, HEIGHT // 2 + 20, "Press ENTER to Restart", 7)
            return

        # ターンの表示
        turn_text = "Player's Turn" if self.turn_player is self.player else "Opponent's Turn"
        pyxel.text(WIDTH // 2 - 40, 10, turn_text, 7)

        # 召喚回数, 合体回数
        summon_text = f"# summon: {self.player.n_summon:02d}"
        pyxel.text(10, 20, summon_text, 7)
        fusion_text=f"# fusion: {self.player.n_fusion:02d}"
        pyxel.text(10, 30, fusion_text, 7)

        deck_text=f"# deck: {len(self.player.deck):02d}"
        pyxel.text(10, 40, deck_text, 7)
        graveyard_text=f"# graveyard: {len(self.player.graveyard):02d}"
        pyxel.text(10, 50, graveyard_text, 7)
        
        summon_text = f"# summon: {self.opponent.n_summon:02d}"
        pyxel.text(250, 20, summon_text, 7)
        fusion_text=f"# fusion: {self.opponent.n_fusion:02d}"
        pyxel.text(250, 30, fusion_text, 7)

        deck_text=f"# deck: {len(self.player.deck):02d}"
        pyxel.text(250, 40, deck_text, 7)
        graveyard_text=f"# graveyard: {len(self.player.graveyard):02d}"
        pyxel.text(250, 50, graveyard_text, 7)
        graveyard_text=f"# hand: {len(self.player.hand):02d}"
        pyxel.text(250, 60, graveyard_text, 7)
        
        pyxel.text(10, 10, f"Player HP: {self.player.hp}", 7)
        pyxel.text(250, 10, f"Opponent HP: {self.opponent.hp}", 7)
        
        # card draw
        self.draw_status = True
        for i, card in enumerate(self.player.hand):
            if card is None: continue

            if card == self.selected_card:
                if self.player.n_summon > 0:
                    color = pyxel.COLOR_ORANGE
                else:
                    color = pyxel.COLOR_GRAY
            else:
                color = pyxel.COLOR_WHITE

            selected = self.selected_card == card
            self.draw_status *= card.draw(color, selected=selected)

        for i, card in enumerate(self.player.field):
            if card is None: continue

            if card == self.selected_attacker:
                color = pyxel.COLOR_LIME

            elif card == self.selected_card:
                if (self.player.n_fusion > 0) & (self.selected_attacker is not None):
                    color = pyxel.COLOR_PURPLE
                else:
                    color = pyxel.COLOR_ORANGE
            elif card.attackable:
                color = pyxel.COLOR_LIME
            else:
                color = pyxel.COLOR_WHITE

            selected = self.selected_card == card
            attacker = self.selected_attacker == card
            self.draw_status *= card.draw(color, selected=selected, attacker=attacker)

        for i, card in enumerate(self.opponent.field):
            if card is None: continue
            if card == self.selected_card:
                if (self.selected_attacker is not None) and (self.selected_attacker.attackable):
                    color = pyxel.COLOR_RED
                else:
                    color = pyxel.COLOR_GRAY
            else:
                color = pyxel.COLOR_WHITE
            
            selected = self.selected_card == card
            
            counter = False
            if self.selected_attacker is not None:
                counter = judge_counter_attribute(card, self.selected_attacker)
            self.draw_status *= card.draw(color, selected=selected, counter=counter)

if __name__ == "__main__":
    Game()
