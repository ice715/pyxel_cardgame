from importlib import import_module
import itertools
import random

from cfg import MAX_LV
# クラインの四元群の積を定義
klein_group = {
    ('e', 'e'): 'e', ('e', 'a'): 'a', ('e', 'b'): 'b', ('e', 'c'): 'c',
    ('a', 'e'): 'a', ('a', 'a'): 'e', ('a', 'b'): 'c', ('a', 'c'): 'b',
    ('b', 'e'): 'b', ('b', 'a'): 'c', ('b', 'b'): 'e', ('b', 'c'): 'a',
    ('c', 'e'): 'c', ('c', 'a'): 'b', ('c', 'b'): 'a', ('c', 'c'): 'e'
}

all_card_lst = list(itertools.product(["e", "a", "b", "c"], range(1, MAX_LV + 1)))

def klein_map(x, y):
    return klein_group[(x, y)]

def add_or_replace_none(lst, element):
    try:
        index = lst.index(None)
        lst[index] = element
    except ValueError:
        lst.append(element)
    print('add_or_replace', lst)
        
def len_with_out_none(lst):
    return len([i for i in lst if i is not None])

def get_fusion_card(card1, card2, owner=None):
    total_lv = (card1.lv + card2.lv)
    target_lv = total_lv % MAX_LV
    bonus = total_lv // MAX_LV
    if target_lv == 0:
        target_lv = MAX_LV
        bonus -= 1
    target_attr = klein_map(card1.attribute, card2.attribute)
    new_card = param2card(lv=target_lv, attribute=target_attr, owner=owner, bonus=bonus)
    return new_card

def param2card(lv, attribute, owner=None, bonus=0):
    # card_info = card_data[(attribute, lv)]
    real_card = import_real_card(attribute, lv, owner)
    apply_bonus(real_card, bonus)
    return real_card

def apply_bonus(card, bonus):
    if bonus == 0:
        return
    rate = 2
    card.name += f"+{bonus}"
    card.lv += MAX_LV * bonus
    card.max_hp += rate * bonus
    card.hp += rate * bonus
    card.atk += rate * bonus

def get_init_deck_debug(owner):
    ret = [
        import_real_card("e", 1, owner),
        import_real_card("a", 1, owner),
        import_real_card("b", 1, owner),
        import_real_card("c", 1, owner),
    ]
    return ret

def get_init_deck(owner):
    ret = [
        import_real_card("e", 1, owner),
        import_real_card("a", 1, owner),
        import_real_card("b", 1, owner),
        import_real_card("c", 1, owner),
    ]
    return ret

def import_real_card(attribute, lv, owner):
    card_module = import_module(f"card_scripts.{attribute}_{lv}")
    real_card_cls = getattr(card_module, "Real_card")
    return real_card_cls(owner)

def judge_counter_attribute(card1, card2):
    if card1.attribute == "e":
        return card2.attribute == "e"
    elif card1.attribute == "a":
        return card2.attribute == "b"
    elif card1.attribute == "b":
        return card2.attribute == "a"
    elif card1.attribute == "c":
        return card2.attribute != "e"

def get_no_used_card_lst(player1, player2):
    use_card_lst = get_used_card_lst(player1, player2)
    all_cards = set(all_card_lst)
    not_use_card_lst = sorted(all_cards - set(use_card_lst))
    return not_use_card_lst

def get_used_card_lst(player1, player2):
    player1_cards = get_user_card_set(player1)
    player2_cards = get_user_card_set(player2)
    use_card_lst = sorted(player1_cards | player2_cards)
    return use_card_lst

def get_user_card_set(player):
    user_card_set = set([extract_param(card) for card in (player.deck + player.field + player.hand + player.graveyard) if card is not None])
    return user_card_set

def extract_param(card):
    return card.attribute, card.lv

