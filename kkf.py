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

        # 点滅処理（消滅の3秒前から開始）
        if self.age > self.lifespan - 150:  # 3秒は150フレーム
            self.visible = not self.visible  # 1フレームごとに表示/非表示を切り替え

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

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

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
            

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

    
