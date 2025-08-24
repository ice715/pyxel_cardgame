# card_library.py
import pyxel

import copy
from cfg import HEIGHT, WIDTH, CARD_HEIGHT, CARD_WIDTH, CARD_COLOR,ATTRIBUTES
from utils import add_or_replace_none, len_with_out_none, judge_counter_attribute

class Card:
    def __init__(self, owner):
        self.name = "empty"
        self.atk = 0
        self.max_hp = 1
        self.hp = self.max_hp
        self.lv = 0
        self.attribute = None
        self.owner = owner
        self.attackable = False
        
        # animation
        self.animation = None  # アニメーションの状態を管理する属性
        self.animation_progress = 0.0  # アニメーションの進行度を管理する属性
        self.animation_speed = 4  # アニメーションの速度
        self.alpha = 1.0
        self.design_address = None
        
        # attack animation
        self.attack_animation = []
        self.attack_animation_progress = []
        self.attack_damages = []
        self.attack_effects = []
        self.text_color = pyxel.COLOR_BLACK
    
        # effect queue
        self.function_queue = []
        self.dst_metamorphose = None

    def get_design_address(self):
        r = ATTRIBUTES.index(self.attribute)
        if self.lv > 8:
            self.design_address = ((2*r + self.lv - 9)*CARD_WIDTH, 4*CARD_HEIGHT)
        else:
            self.design_address = ((self.lv-1)*CARD_WIDTH, r*CARD_HEIGHT)
    
    def deal_damage(self, damage, target):
        self.attack_animation.append(target)
        self.attack_animation_progress.append(0.0)
        self.attack_damages.append(damage)
        self.attack_effects.append('effect')
    
    def attack(self, target):
        if self.attackable:
            self.attackable = False
            self.attack_animation.append(target)
            self.attack_animation_progress.append(0.0)
            self.attack_damages.append(self.atk)
            self.attack_effects.append('attack')
    
    def counter_attack(self, target):
        self.attack_animation.append(target)
        self.attack_animation_progress.append(0.0)
        self.attack_damages.append(self.atk)
        self.attack_effects.append('counter_attack')

    def attacked(self, target):
        if judge_counter_attribute(self, target):
            self.counter_attack(target)

    def destruction(self):
        self.owner.graveyard.append(self)
        idx = self.owner.field.index(self)
        self.owner.field[idx] = None
        self.hp = self.max_hp
        self.attackable = False

    def discard(self):
        self.owner.graveyard.append(self)
        idx = self.owner.hand.index(self)
        self.owner.hand[idx] = None
        self.hp = self.max_hp
        self.attackable = False

    def vanish(self):
        if self in self.owner.field:
            idx = self.owner.field.index(self)
            self.owner.field[idx] = None
        elif self in self.owner.hand:
            idx = self.owner.hand.index(self)
            self.owner.hand[idx] = None
        del self

    def metamorphose(self, new_card):
        self.animation = 'metamorphose'  # カードの上から着色されるアニメーションを設定
        self.animation_progress = 0  # アニメーションの進行度を初期化
        self.dst_metamorphose = new_card
        
    def summon_from_hand(self):
        idx = self.owner.hand.index(self)
        self.owner.hand[idx] = None
        self.summon()
        self.owner.n_summon -= 1

    def summon(self):
        add_or_replace_none(self.owner.field, self)
        self.animation = "summon"  # カードの上から着色されるアニメーションを設定
        self.animation_progress = 0  # アニメーションの進行度を初期化

    def on_summon(self):
        pass

    def on_reborn(self):
        self.on_summon()

    def on_fusion(self):
        self.on_summon()

    def turn_start(self):
        if self in self.owner.field:
            self.attackable = True
    
    def turn_end(self):
        pass

    def reborn(self):
        if (self in self.owner.graveyard) and (len_with_out_none(self.owner.field) < self.owner.max_field_size):
            add_or_replace_none(self.owner.field, self)
            self.animation = "reborn"
            self.animation_progress = 0

    def copy_class(self, target_card):
        # 動的にクラスを生成（クラス名は変更しない）
        self.__class__ = type(
            target_card.__class__.__name__,  # 元のクラス名をそのまま使用
            (target_card.__class__,),        # 継承元のクラス
            {'original_class': self.__class__, 'original_state': self.__dict__}   # 追加の属性やメソッドはなし
        )
        # 対象カードのインスタンス変数をコピー
        # print(target_card.__dict__)
        self.__dict__ = target_card.__dict__

    def reset_class(self):
        self.__class__ = type(
            self.original_class.__name__,  # 元のクラス名をそのまま使用
            (self.original_class,),        # 継承元のクラス
            {}                             # 追加の属性やメソッドはなし
        )
        self.__dict__ = self.original_state
        print(self.__dict__)
        
    def draw(self, edge_color=7, selected=False, attacker=False, counter=False):
        if self in self.owner.field:
            place = self.owner.field
            if self.owner.is_real:
                xo = 50
                yo = HEIGHT - 110
            else:
                xo = 50
                yo = HEIGHT - 190
        elif self in self.owner.hand:
            place = self.owner.hand
            xo = 50
            yo = HEIGHT - 50
        
        idx = place.index(self)    
        
        card_w = CARD_WIDTH
        card_h = CARD_HEIGHT

        # update x, y
        self.x = xo + idx * (CARD_WIDTH + 8) + CARD_WIDTH//2
        self.y = yo + CARD_HEIGHT//2

        if self.attack_animation:
        # 弾丸の描画
            # 攻撃アニメーションの更新と描画
            new_attack_animation = []
            new_attack_animation_progress = []
            new_attack_damages = []
            new_attack_effects = []

            for attack_target, animation_progress, damage, effect in zip(self.attack_animation, 
                                                                         self.attack_animation_progress,
                                                                         self.attack_damages,
                                                                         self.attack_effects):
                bullet_x = self.x + (attack_target.x - self.x) * animation_progress
                bullet_y = self.y + (attack_target.y - self.y) * animation_progress
                bullet_color1 = pyxel.COLOR_DARK_BLUE if effect == 'effect' else pyxel.COLOR_RED 
                bullet_color2 = pyxel.COLOR_LIGHT_BLUE if effect == 'effect' else pyxel.COLOR_PEACH
                bullet_size = min(max(4, damage), 10)
                pyxel.circ(bullet_x, bullet_y, bullet_size, bullet_color1)
                pyxel.circ(bullet_x, bullet_y, bullet_size - 2, bullet_color2)

                # アニメーション進行
                animation_progress += 0.10

                # アニメーションが完了していない場合のみリストに追加
                if animation_progress < 1:
                    new_attack_animation.append(attack_target)
                    new_attack_animation_progress.append(animation_progress)
                    new_attack_damages.append(damage)
                    new_attack_effects.append(effect)
                else:
                    attack_target.hp -= damage

                if isinstance(attack_target, Card) and (effect == 'attack'):
                    attack_target.attacked(self)

            # 更新されたリストを反映
            self.attack_animation = new_attack_animation
            self.attack_animation_progress = new_attack_animation_progress
            self.attack_damages = new_attack_damages
            self.attack_effects = new_attack_effects

        if self.animation == "hand2field":
            self.animation_progress += self.animation_speed
            if self.animation_progress >= CARD_HEIGHT:
                self.animation_progress = CARD_HEIGHT
                self.summon_from_hand()
                return self.animation is None
            yo = yo + self.animation_progress
            card_h = card_h - self.animation_progress

        elif self.animation in ["summon", "reborn"]:
            self.animation_progress += self.animation_speed
            if self.animation_progress >= CARD_HEIGHT:
                self.animation_progress = CARD_HEIGHT
                if self.animation == "summon":
                    self.on_summon()
                elif self.animation == "reborn":
                    self.on_reborn()
                self.animation = None  # アニメーション終了
            card_h = self.animation_progress
        elif self.animation == "draw":
            self.animation_progress += self.animation_speed
            if self.animation_progress >= CARD_WIDTH:
                self.animation_progress = CARD_WIDTH
                self.animation = None  # アニメーション終了
            card_w = self.animation_progress

        elif self.animation in ["destruction", "discard", 'vanish']:
            pyxel.dither(1.0)
            if self.alpha >= 0:
                self.alpha -= 0.05
                pyxel.dither(self.alpha)
            else:
                self.alpha = 1.0
                if self.animation == "destruction":
                    self.destruction()
                elif self.animation == "discard":
                    self.discard()
                elif self.animation == "vanish":
                    self.vanish()
    
                self.animation = None  # アニメーション終了
                return self.animation is None

        elif self.animation == "fusion":
            pyxel.dither(1.0)
            if self.alpha < 1.0:
                self.alpha += 0.05
                pyxel.dither(self.alpha)
            else:
                self.alpha = 1.0
                self.on_fusion()
                self.animation = None # アニメーション終了

        elif self.animation == "metamorphose":
            self.animation_progress += self.animation_speed
            if self.animation_progress >= CARD_HEIGHT:
                self.animation_progress = CARD_HEIGHT
                self.animation = None  # アニメーション終了
                if self in self.owner.field:
                    self.owner.field[self.owner.field.index(self)].copy_class(self.dst_metamorphose)
                elif self in self.owner.hand:
                    self.owner.hand[self.owner.hand.index(self)].copy_class(self.dst_metamorphose)
                return self.animation is None
            card_h = self.animation_progress

        bg_color = pyxel.COLOR_BLACK
        pyxel.rectb(xo + idx * (CARD_WIDTH + 8) + 1, yo + 1, card_w, card_h, bg_color)
        if self.animation == "metamorphose":
            pyxel.blt(xo + idx * (CARD_WIDTH + 8), yo, 0, self.design_address[0], self.design_address[1], card_w, CARD_HEIGHT)
            pyxel.blt(xo + idx * (CARD_WIDTH + 8), yo, 0, self.dst_metamorphose.design_address[0], self.dst_metamorphose.design_address[1], card_w, card_h)
        else:
            pyxel.blt(xo + idx * (CARD_WIDTH + 8), yo, 0, self.design_address[0], self.design_address[1], card_w, card_h)
        frame_color = pyxel.COLOR_GRAY
        if self.owner.is_real:
            if (self in self.owner.field) and self.attackable:
                frame_color = pyxel.COLOR_LIME
            if self in self.owner.hand and (self.owner.n_summon > 0):
                frame_color = pyxel.COLOR_LIME
        pyxel.rectb(xo + idx * (CARD_WIDTH + 8), yo, card_w, card_h, frame_color)

        if self.animation is None:
            if self.function_queue:
                effect, args = self.function_queue.pop(0)
                effect(*args)
            else:
                pyxel.dither(1.0)
                self.animation_progress = 0
                # pyxel.text(xo + 5 + idx * (CARD_WIDTH + 8), yo + 12, self.name, 0)
                pyxel.text(xo + 22 + idx * (CARD_WIDTH + 8), yo + 4, f"{self.lv:>2}", pyxel.COLOR_ORANGE)
                pyxel.text(xo + 24 + idx * (CARD_WIDTH + 8), yo + 4, f"{self.lv:>2}", pyxel.COLOR_ORANGE)
                pyxel.text(xo + 23 + idx * (CARD_WIDTH + 8), yo + 3, f"{self.lv:>2}", pyxel.COLOR_ORANGE)
                pyxel.text(xo + 23 + idx * (CARD_WIDTH + 8), yo + 5, f"{self.lv:>2}", pyxel.COLOR_ORANGE)
                pyxel.text(xo + 23 + idx * (CARD_WIDTH + 8), yo + 4, f"{self.lv:>2}", pyxel.COLOR_YELLOW)

                pyxel.text(xo - 1 + idx * (CARD_WIDTH + 8), yo + 40, f"{self.atk:>2}", pyxel.COLOR_RED)
                pyxel.text(xo + 1 + idx * (CARD_WIDTH + 8), yo + 40, f"{self.atk:>2}", pyxel.COLOR_RED)
                pyxel.text(xo + idx * (CARD_WIDTH + 8), yo + 39, f"{self.atk:>2}", pyxel.COLOR_RED)
                pyxel.text(xo + idx * (CARD_WIDTH + 8), yo + 41, f"{self.atk:>2}", pyxel.COLOR_RED)
                pyxel.text(xo + idx * (CARD_WIDTH + 8), yo + 40, f"{self.atk:>2}", pyxel.COLOR_ORANGE)

                if self.hp < self.max_hp:
                    hp_color = pyxel.COLOR_RED
                    hp_bg_color = pyxel.COLOR_PEACH
                else:
                    hp_color = pyxel.COLOR_LIME
                    hp_bg_color = pyxel.COLOR_GREEN
                pyxel.text(xo + 22+ idx * (CARD_WIDTH + 8), yo + 40, f"{self.hp:>2}", hp_bg_color)
                pyxel.text(xo + 24+ idx * (CARD_WIDTH + 8), yo + 40, f"{self.hp:>2}", hp_bg_color)
                pyxel.text(xo + 23+ idx * (CARD_WIDTH + 8), yo + 39, f"{self.hp:>2}", hp_bg_color)
                pyxel.text(xo + 23+ idx * (CARD_WIDTH + 8), yo + 41, f"{self.hp:>2}", hp_bg_color)
                pyxel.text(xo + 23+ idx * (CARD_WIDTH + 8), yo + 40, f"{self.hp:>2}", hp_color)

        if selected:
            margin = 2
            pyxel.rectb(xo + idx * (CARD_WIDTH + 8) - margin, yo - margin, card_w + 2*margin, card_h + 2*margin, edge_color)
            if attacker and self.attackable and self.owner.is_real: # and (len_with_out_none(self.owner.opponent.field) == 0):
                pyxel.tri(xo + idx * (CARD_WIDTH + 8) + card_w//2, yo - 10, xo + idx * (CARD_WIDTH + 8) + card_w//2 - 4, yo - 2, xo + idx * (CARD_WIDTH + 8) + card_w//2 + 4, yo - 2, pyxel.COLOR_RED)
        if counter:
            if self.owner.is_real:
                pass
                # pyxel.tri(xo + idx * (CARD_WIDTH + 8) + card_w//2, yo - 10, xo + idx * (CARD_WIDTH + 8) + card_w//2 - 4, yo - 2, xo + idx * (CARD_WIDTH + 8) + card_w//2 + 4, yo - 2, pyxel.COLOR_PURPLE)
            else:
                pyxel.tri(xo + idx * (CARD_WIDTH + 8) + card_w//2, yo + CARD_HEIGHT + 10, xo + idx * (CARD_WIDTH + 8) + card_w//2 - 4, yo + CARD_HEIGHT + 2, xo + idx * (CARD_WIDTH + 8) + card_w//2 + 4, yo + CARD_HEIGHT + 2, pyxel.COLOR_PURPLE)
        pyxel.dither(1.0)
        return self.animation is None

