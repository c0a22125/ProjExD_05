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

def draw_start_screen(screen, font, text, color):
        text_render = font.render(text, True, color)
        text_rect = text_render.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_render, text_rect)

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



class Item:
    """
    アイテムに関するクラス
    """
    def __init__(self, color, x, y, radius=15, lifespan=500):
        self.color = color  # アイテムの色
        self.x = x  # アイテムのX座標
        self.y = y  # アイテムのY座標
        self.radius = radius  # アイテムの半径
        self.stop_y = random.randint(self.radius, HEIGHT - self.radius)  # アイテムの停止位置（ランダム）
        self.lifespan = lifespan  # アイテムの寿命（フレーム数）
        self.age = 0  # アイテムの年齢（フレーム数）
        self.has_stopped = False  # アイテムが停止したかどうか
        self.visible = True  # アイテムが表示されているかどうか

    def draw(self, screen):
        if self.visible:
            pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)  # アイテムを画面に描画

    def update(self):
        if self.y < self.stop_y:
            self.y += 3  # アイテムが停止位置に達するまで下に移動
        else:
            if not self.has_stopped:
                self.has_stopped = True  # アイテムが停止位置に達したことを記録
                self.age = 0  # 停止した時点で年齢をリセット
            else:
                self.age += 1  # アイテムの年齢を増やす

    def is_expired(self):
        return self.age > self.lifespan  # アイテムの寿命が尽きたかどうかを判断


def main():
    pg.display.set_caption("大戦争スマッシュこうかとんファイターズ")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"{MAIN_DIR}/fig/pg_bg.jpg")

    items = []  # アイテムのリスト
    last_item_spawn = 0  # 最後にアイテムが生成された時間を記録
    item_spawn_interval = 1500  # アイテムを生成する頻度

    tmr = 0
    clock = pg.time.Clock()
    pg.init()
    koukaton = Koukaton() # クラスからオブジェクト生成
    vict_condition = start(koukaton)
    hyper_font = pg.font.Font(None, 50)  # 残り時間用のフォント
    hyper_color = (0, 0, 255)  # 残り時間の表示色
    fonto = pg.font.Font(None, 200)  # ゲームオーバーの文字を生成
    txt = fonto.render("Time UP", True, (255, 0, 0))
    start_screen_font = pg.font.Font(None, 200)
    start_screen_color = (200, 50, 100)  # 紫色の文字
    lnvalid_screen_color = (255, 0, 0)  # 赤色の文字)
    
    # スタート画面についての部分
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])

        keys = pg.key.get_pressed()

        if keys[pg.K_1]: # 「１」を押すとメインコード部分が読み込み開始
            draw_start_screen(screen, start_screen_font, "Game start", start_screen_color)
            pg.display.flip()
            pg.time.delay(2000)  # 表示を少し待つ
            break
        else: # 「１」が押されるまでの画面表示
            draw_start_screen(screen, start_screen_font, "Are you ready?", lnvalid_screen_color)
            pg.display.flip()
    tmr = 0
    clock.tick(50)
    # ここまでがスタート画面です。

    # メインコード部分
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])
        #メイン処理

        
        # アイテムの生成
        if tmr - last_item_spawn > item_spawn_interval:
            last_item_spawn = tmr
            color = random.choice([(0, 255, 0), (0, 0, 255)])  # アイテムの色を緑または青に設定
            x = random.randint(0, WIDTH)  # X座標をランダムに設定
            items.append(Item(color, x, 0))  # アイテムを生成してリストに追加

        # アイテムの更新
        for item in items[:]:
            item.update()
            item.draw(screen)
            if item.is_expired():
                items.remove(item)  # 寿命が尽きたアイテムを削除

        pg.display.update()
        tmr += 1
        clock.tick(50)

        dt = 10 - tmr/50 # ゲームの経過時間を計算

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()


        # キー入力の処理 HPが減るかの確認用
        keys = pg.key.get_pressed() # キーボードの状態をゲットする
        if vict_condition.allow_input: # 勝利条件が満たされているか
            if keys[pg.K_SPACE]: # スペースキーが押された場合hp減少
                koukaton.setHp(koukaton.getHp() - 10)   
                print(koukaton.getHp())
        
        if dt >= 0: # 時間が0になるまでの時間を右下に表示
            hyper_text = hyper_font.render(f"Time: {int(dt)}", True, hyper_color)
            hyper_pos = (WIDTH - hyper_text.get_width() - 10, HEIGHT - hyper_text.get_height() - 10)
            screen.blit(hyper_text, hyper_pos)  # 残り時間を表示
        elif dt <= 0: # 時間が0になった時に「Time UP」と表示
            txt_rect = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(txt, txt_rect)  # Time UPを画面中央に表示
            pg.display.update()
            pg.time.delay(2000)
            return
        if koukaton.getHp() <= 0:
            txt_rect = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            draw_start_screen(screen, start_screen_font, "Finish!!!", lnvalid_screen_color)  # Finissh!!!を画面中央に表示
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

    
