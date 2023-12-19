import math
import os
import random
import sys
import time
from typing import Any
import pygame as pg

WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]


class Koukaton:
    def __init__(self):
        self.hp = 100
        self.speed = 1.0
        
    def setHp(self, hp):
        self.hp = hp
    def getHp(self):
        return self.hp
    
    def setSpeed(self, speed):
        self.speed = speed
    def getSpeed(self):
        return self.speed


class start:
    """
    勝利条件に関するクラス
    """
    def __init__(self, koukaton):
        self.koukaton = koukaton
        self.timer = 60  # 初期時間
        self.reset_timer = 10  # リセットまでの時間について
        self.round = 5  # ラウンド回数について
        self.reset()

    def reset(self):
        """
        勝利条件をリセットする
        """
        self.timer = 60
        self.koukaton.hp = 100
        self.allow_input = True
        self.round -= 1
        if self.round <= 0:
            self.allow_input = False
            
    def update(self, dt):
        """
        勝利条件の更新
        """
        # 設定した時間かこうかとんのhpが0になったときに勝利
        self.timer == dt
        if self.koukaton.hp <= 0:
            self.allow_input = False
            if self.reset_timer <= 0:
                self.reset()
            else:
                self.reset_timer -= dt       


def main():
    pg.display.set_caption("大戦争スマッシュこうかとんファイターズ")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"{MAIN_DIR}/fig/pg_bg.jpg")

    tmr = 0
    clock = pg.time.Clock()
    pg.init()
    koukaton = Koukaton() # クラスからオブジェクト生成
    vict_condition = start(koukaton)
    hyper_font = pg.font.Font(None, 50)  # 残り時間用のフォント
    hyper_color = (0, 0, 255)  # 残り時間の表示色
    fonto = pg.font.Font(None, 200)  # ゲームオーバーの文字を生成
    txt = fonto.render("Game Over", True, (255, 0, 0))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])
        #メイン処理

        # pg.display.update()
        tmr += 1
        clock.tick(50)

        dt = 15 - tmr/50 # ゲームの経過時間を計算

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # キー入力の処理
        keys = pg.key.get_pressed() # キーボードの状態をゲットする
        if vict_condition.allow_input: # 勝利条件が満たされているか
            if keys[pg.K_SPACE]: # スペースキーが押された場合hp減少
                koukaton.hp -= 10
        
        if dt >= 0:
            hyper_text = hyper_font.render(f"Time: {int(dt)}", True, hyper_color)
            hyper_pos = (WIDTH - hyper_text.get_width() - 10, HEIGHT - hyper_text.get_height() - 10)
            screen.blit(hyper_text, hyper_pos)  # 残り時間を表示
        elif dt <= 0:
            txt_rect = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(txt, txt_rect)  # Game Overを画面中央に表示
            pg.display.update()
            pg.time.delay(2000)
            return
            
            
        
        # 勝利条件の更新
        vict_condition.update(dt)

        # 画面の描画
        pg.display.flip()
            

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

    
