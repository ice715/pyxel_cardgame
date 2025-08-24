import colorsys
import math

import cv2
from PIL import Image
import numpy as np

# Pyxelの16色パレット（RGB）
PYXEL_PALETTE = {
    0:(0, 0, 0), 1:(43, 51, 95), 2:(126, 32, 114), 3:(25, 149, 156),
    4:(139, 72, 82), 5:(57, 92, 152), 6:(169, 193, 255), 7:(238, 238, 238),
    8:(212, 24, 108), 9:(211, 132, 65), 10:(233, 195, 91), 11:(112, 198, 169),
    12:(118, 150, 222), 13:(163, 163, 163), 14:(255, 151, 152), 15:(237, 199, 176)
}

# RGBをHSVに変換

def rgb_to_hsv(rgb):
    """RGBタプル (R, G, B) をHSVに変換する"""
    r, g, b = rgb  # RGB値を取得
    r, g, b = r / 255.0, g / 255.0, b / 255.0  # 0〜1の範囲に正規化
    h, s, v = colorsys.rgb_to_hsv(r, g, b)  # HSVに変換
    return int(h * 360), int(s * 100), int(v * 100)  # Hを0-360、S/Vを0-100の範囲に変換

# HSVの距離を計算

def hsv_distance(hsv1, hsv2):
    """HSV空間での2点間の距離を計算する"""
    h1, s1, v1 = hsv1
    h2, s2, v2 = hsv2
    
    # Hの差を360度の円環で最短距離に調整
    dh = min(abs(h1 - h2), 360 - abs(h1 - h2)) / 180.0  # 正規化 (0〜2にする)
    ds = (s1 - s2) / 100.0  # 0〜1に正規化
    dv = (v1 - v2) / 100.0  # 0〜1に正規化

    # ユークリッド距離を計算
    return math.sqrt(dh**2 + ds**2 + dv**2)

def rgb_distance(rgb1, rgb2):
    diff = (np.array(rgb1) - np.array(rgb2))
    # ユークリッド距離を計算
    return math.sqrt(diff[0]**2 + diff[1]**2 + diff[2]**2)


# PyxelパレットをHSVに変換
PYXEL_PALETTE_HSV = [rgb_to_hsv(rgb) for rgb in PYXEL_PALETTE.values()]

def convert_to_pyxel_palette(image_path, output_path, im_size=None):
    img = Image.open(image_path).convert("RGB")
    img_array = np.array(img)
    
    if im_size is not None:
        height, width = img_array.shape[:2]
        cx = width // 2
        cy = height // 2
        rate = im_size[1] / im_size[0]

        if rate > 1:
            new_width = int(height / rate)
            img_array = img_array[:,cx-new_width//2:cx+new_width//2]
        else:
            new_height = int(width * rate)
            img_array = img_array[cy-new_height//2:cy+new_height//2,:]
    new_img_array = np.zeros_like(img_array)

    for y in range(img_array.shape[0]):
        for x in range(img_array.shape[1]):
            original_rgb = tuple(img_array[y, x])
            closest_color = min(PYXEL_PALETTE.values(), key=lambda c: rgb_distance(original_rgb, c))
            new_img_array[y, x] = closest_color

    if im_size is not None:
        new_img_array = cv2.resize(new_img_array, im_size, interpolation=cv2.INTER_NEAREST)
        # img_array = cv2.resize(img_array, im_size, interpolation=cv2.INTER_LINEAR)


    new_img = Image.fromarray(new_img_array.astype(np.uint8), "RGB")
    new_img.save(output_path)

# 使用例
# convert_to_pyxel_palette("card_src/test.webp", "output3.png", im_size=(32, 48))
# convert_to_pyxel_palette("card_src/test.webp", "output2.png", im_size=(64, 96))
# convert_to_pyxel_palette("output2.png", "output3.png", im_size=(32, 48))

im = cv2.imread("output2.png")
h, w = im.shape[:2]

im = im[h//4-5:3*h//4-5, w//4:3*w//4]
print(im.shape)
cv2.imwrite("output4.png", im)
