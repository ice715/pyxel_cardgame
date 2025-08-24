import pyxel

class Background:
    def __init__(self):
        pyxel.init(width=320, height=240, title="test")
        self.t = 0  # アニメーション用の時間カウンタ
        pyxel.run(self.update, self.draw)

    def update(self):
        self.t += 1  # フレームごとにカウンタを増やす

    def draw(self):
        pyxel.cls(0)

        # 天界（左半分）
        for y in range(240):
            color = 7 if y < 100 else 6  # 空の色
            pyxel.line(0, y, 160, y, color)
        
        # 天界の光の球（上下にふわふわ動く）
        light_y = 50 + 5 * pyxel.sin(self.t * 0.05)  # sin波で動かす
        pyxel.circ(100, int(light_y), 20, 10)

        # 冥界（右半分）
        for y in range(240):
            color = 13 if y < 100 else 2  # 暗い空の色
            pyxel.line(160, y, 320, y, color)
        
        # 冥界の黒炎（ゆらゆら揺れる）
        flame_height = 30 + 5 * pyxel.sin(self.t * 0.1)  # sin波でサイズ変化
        pyxel.rect(220, 180, 20, int(flame_height), 0)

        # 境界エネルギー（明滅する円）
        for i in range(10):
            color = 8 if (self.t // 5) % 2 == 0 else 0  # 点滅
            pyxel.circ(160, 120, 30 - i, color)

        pyxel.text(130, 5, "天界 vs 冥界", 7)

Background()