import copy
import random
from importlib import import_module

from card import Card
from utils import get_user_card_set

class Real_card(Card):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Viṣṇu"
        self.lv = 9
        self.attribute = "e"
        self.atk = 10
        self.max_hp = 9
        self.hp = self.max_hp
        self.get_design_address()

        self.original_class = Real_card  # 元のクラスを保持
        self.original_state = copy.deepcopy(self.__dict__)  # 元の状態を保持

    def on_summon(self):
        opponent_card_lst = sorted(get_user_card_set(self.owner.opponent))
        opponent_max_lv = max([lv for attribute, lv in opponent_card_lst])
        candidate_cards = [param for param in opponent_card_lst if param[1] == opponent_max_lv]
        param = random.choice(candidate_cards)
        target_attribute, target_lv = param

        # 相手のカードクラスを取得
        target_card_module = import_module(f"card_scripts.{target_attribute}_{target_lv}")
        target_card_cls = getattr(target_card_module, "Real_card")
        target_card = target_card_cls(self.owner)  # 対象カードのインスタンスを生成
        self.copied_class = target_card_cls

        # 動的にクラスを生成（クラス名は変更しない）
        self.__class__ = type(
            self.copied_class.__name__,  # 元のクラス名をそのまま使用
            (self.copied_class,),        # 継承元のクラス
            {}                           # 追加の属性やメソッドはなし
        )

        # 対象カードのインスタンス変数をコピー
        self.__dict__ = copy.deepcopy(target_card.__dict__)
        self.name = self.name + "_Visnu"
        super().on_summon()
    
    def destruction(self):
        super().destruction()
        self.__class__ = self.original_class  # クラスを元に戻す
        self.__dict__ = copy.deepcopy(self.original_state) 
    