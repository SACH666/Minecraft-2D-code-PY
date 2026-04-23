# -*- coding: utf-8 -*-
"""
2D Minecraft - 完整版
包含单机模式、联机功能、合成系统、生命值系统、地底滤镜效果
"""

import pygame
import os
import sys
import random
import json
import math
import time
import threading
import socket
import pickle
import argparse
import base64
from enum import Enum
from io import BytesIO

# ==================== 游戏配置 ====================

# 获取游戏根目录
GAME_ROOT = os.path.dirname(os.path.abspath(__file__))
SAVES_PATH = os.path.join(GAME_ROOT, 'saves')
SKINS_PATH = os.path.join(GAME_ROOT, 'skins')
FONTS_PATH = os.path.join(GAME_ROOT, 'fonts')
TEXTURES_PATH = os.path.join(GAME_ROOT, 'textures')

# 确保必要目录存在
for path in [SAVES_PATH, SKINS_PATH, FONTS_PATH, TEXTURES_PATH]:
    if not os.path.exists(path):
        os.makedirs(path)

# ==================== 内置纹理数据 ====================

# Base64编码的纹理数据
TEXTURE_DATA = {
    "grass_block.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAeFBMVEV5VTqWbEq5hVyHh4dwsEZoqD5iojhsrEJhoTdpqT9npz1goDZXly1QkCZzs0l2tkyKuVp+vlRqqkCDslOBsFFmpjyQv2CSwWKTwmN/v1WXxmdvr0VkpDqcy2xrq0GNvF11tUttrUN0tEpfnzVxsUd0WERsbGxZPSmGrpghAAAAjElEQVR42gXBB0LCAAAEwd2LGkAFG3ZqIPf/HzLDebPebv+m8XXztlounk8cx5eP994/TN+f68W42nPo7n/Zu55/vn779Fg6t5e2U0+lBTEV2s5YoIptoUAIMEBCgggkClZBEUSKAgUstAAkCJIQm1QHEDQ4K5VCRQMAJCBcUZoSRRpKEwRFogwoKL0BxA0LD3lN79UAAAAASUVORK5CYII=",
    
    "stone.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAAAAAA6mKC9AAAAXklEQVR42gXBMQEAMAwEocqNgNuR8JYLb9uUruCRgLv0dFddBR6bsaF6Ucm2xTNAXddebGur4NVdV1R424xtoMewjW3zTuouUT2wgc2eyhR3XW9TVFR7CsC2PaBsxAdyLn2NNWHIVAAAAABJRU5ErkJggg==",
    
    "dirt.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAFVBMVEV5VTq5hVyHh4eWbEpsbGx0WERZPSk6VlZqAAAAa0lEQVR42gXBwQnDQAxFwSd+0FnLgs8+5SyjsA2kgZQgY9j+S8gMM61oM9R6W85NeBDs4BPLSpbk9bBeary02zGC02JIMIpVFCm5kkbtDUPIYt5HnaQuffNxPCuAgfiVH1bk7T5EkTPPovwPGbIOYwnMHcMAAAAASUVORK5CYII=",
    
    "oak_log.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAElBMVEV0WjaYeEmRcUJfSitMPSY4Kxi/mP6UAAAAaElEQVR42gXBwQ3DIBREwSd2/90SKWAl8B0lDRAqcPpvJjM4lWpHuFevtkV9qttb3LJUezBV6nLInu7TYe2xEof15M1Q8I+3xgh8WZp5oKnkPLiprro2L8bdi8W142Egh9s+kLOnOfoDKZ4L2kN8RTwAAAAASUVORK5CYII=",
    
    "azalea_leaves.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAD1BMVEUAAABwki1sgDFQaSw6TCZikRf/AAAAAXRSTlMAQObYZgAAAHBJREFUeNoNxsEVhCAMBcAvpgACWwCQLSAhFoCS/mvSy7yB7lk1MNHorjpywnKP0n+EYrLYLwIfGad24BMBHqgrOl/nFyXj/zasQ8RqOPyuxUYeEFNux5dGW5A8gXzrZFlIfSxjCcxSAv40uGUCPfICoioQjMR2fYEAAAAASUVORK5CYII=",
    
    "sand.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAElBMVEXaz6Pt68vn5Lvj27DVxJbRuoo9qeK3AAAAZUlEQVR42gXBMQrCQABE0U9m0gtiH28wkNiP2bUXzP3P4ntscjI0qD2u7bGQ6wS76PCxD0NvQ6LC7OlBOf3u/NqY2nMxjT6jKVuZqzlYZZFLTNJ9tnQMPzNF8pJEke5JfpDsMskfw+0REW3/INgAAAAASUVORK5CYII=",
    
    "cobblestone.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAElBMVEW1tbWmpqaIh4hubW1hYWFSUlLm8qFQAAAAcUlEQVR42gVAARGDMAz8MAMjh4CSLwIWIgDSIGAD/1p2iPk5pTfFOW3QLR3nGrrGQxSLTL1wp2TJ3PF6W/yaOjSV9eEB2y3a4omQPSerG4f6biMXkP0a8X2DMdpytQkuIWuY49CuziJmclhoIcsjUvgH41gVHD61kt4AAAAASUVORK5CYII=",
    
    "bedrock.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAAAAAA6mKC9AAAAbUlEQVR42gXBgQAAMBDEsLG8QmEKcFDVXfIGYDNBfGytRe2Qx8EBoeaebZ4pAL4jAGG18VBROIXj1VzN1eKeigoHMt9K0NWqnnCITKC9LVYc1eCdCq7c6p7AhAWAby1P4HD1NkFwJfg4uBruwH1D0lUfTgxevgAAAABJRU5ErkJggg==",
    
    "coal_ore.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAHlBMVEV/f3+Pj490dHRoaGhcXFxJSz85PDY2NjYuLi4lJSVYKuP9AAAAdklEQVR42gXBgQHAIAzDMMdkhf7/8CSSBMWjAIBIWzinCJ5jd27lXYAqb+73FlTcq/btVgVIkCTaHoPBqjhvCli78wqdj4TIzncfoiLEvltNoIVDbBG1OwdoLUirCt3v7ib9Zj2H2NmqvVsFVLgPCiSASiQB4Qdt9QKv63TjNgAAAABJRU5ErkJggg==",
    
    "iron_ore.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAG1BMVEV/f3+Pj4+IdFWvjnfYr5PiwKp3Z09oaGh0dHR2kUs9AAAAdElEQVR42gXBgQHAMAjDMBtYk/8vnoQALU3bKtAElDfzKHR2SlpmAZg9aZJCW6o2mdmdpIAwe/fd0lkpqHsnRaElqUoTAM1sUt7sKwXf7p24p0LQ+0xR2gKgCLwRoemsfbN3O8XZInXvWwWcVwBVAFBoQSn8xv0DBu+myPQAAAAASUVORK5CYII=",
    
    "gold_ore.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAHlBMVEV/f390dHRoaGiccCDrnQ5cXFz87kv//7WioqKPj48wUnvMAAAAfklEQVR42gXBgQHAQAgCsQN9C/sv3IS2lYQsAQBiwID9EMiu31h6bwZo8Zsd8WZHCPxmb9zuBijeu28lJyqCZm8nEgCSrWyCpB2oZ5tJCwaB9kJa3nsuuEll682sLcB2i2f3uzFoZsUoe5eIzt53jZiNVFD2CpC0W4AGiRYEP65HA2+xOYABAAAAAElFTkSuQmCC",
    
    "diamond_ore.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAHlBMVEV/f3+Pj4+NrbEjlpge0NaioqLV//Z359FnZ2d0dHTXUAaKAAAAeElEQVR42gXBgQHAIAzDMLvAmvz/8CQEaWlaVKBEFZoUaHIlabMHUBmzZ2RsKdDEoVgAab4N/baptH577xnuAcDEeTOJg++RvSPNtwUszBC695zxPQjlNs6YtAUA1WaPAjXB7rf3HovOnpR37owA7ajg0BYAoAKA/g9mA6MdO18tAAAAAElFTkSuQmCC",
    
    "emerald_ore.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAJFBMVEV/f390dHRSa1AX3WIAexjZ/+tB84QXxUQ3Wz4cmCloaGiPj48mkEo8AAAAfElEQVR42gXBgQHAIAzDMKcUBvX//05ClYRMAgBUoUrVhEDtlUBqLwBgNRS62iQEsC6oBkD0nFfJZCJh7tn9LoEqSNU9/b5bSe0FtRff0wRYHVitglSNwhiQ4Zw7SQAA6bP7gZCkivTX78sEpfYiuU8TIWG1jIIKgCaoBH4ExwQBmQbUuQAAAABJRU5ErkJggg==",
    
    "lapis_ore.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAKlBMVEV/f3+Pj4+ioqJEb9wWRI1plfQQNL0QNJwgWYsYVb0QRKxcXFxoaGh0dHQtQBNZAAAAh0lEQVR42gXBgQEDIQwDsXMC9CH2/utWQiAS4gRJgGccCTxDIPe7yzOJzgKESi+rBaWEQDITMaMACM994O/EEWFO716itwTkdVVpbCoSqHcJv7lrMROowvjd7uVnY+yX+PRW+gNYvx+oSmg3kCr97NXtOi0k0vvS+1SqgITbq6giCQCoCgCQ/gdhBTDSbWBDAAAAAElFTkSuQmCC",
    
    "redstone_ore.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAKlBMVEV/f390dHRoaGiWBgbKBwf3HBz9Xl5pXFyXAwPGBAT/AAD/iYm/k5OTjIyWS9PFAAAAe0lEQVR42gXBgWHDIBAEMN1jTJNw+69bSdtKZBJABJiJkJnMOUkAZNZaM4kkIs96vu/nT06g6ef7+97y7FTQe28jipwzmYScc5D9rtKuZz3vDmujrfv+9mVEMhO59yYwc86BVknWfvY6PLsTrb6/20SblERvQdsCEi3hH9DmA9/D3DCFAAAAAElFTkSuQmCC",
    
    "crafting_table.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAANlBMVEX////Y2Ni1tbXCnWK4lF+vj1WfhE2WdEF+YjdnUCxzOSBLKxhBIw44IRYoHgsbFg0ZFAwRDggy6vjwAAAAjklEQVR42gXBW1bDAAxDwSvZKSfAB/vfJtDmaXVGP/8Jn7dIPUHfJnLvBbVZMoZkZrN3IYamCZKxCi6as27AnHy91qHRrEdkDCtD4zgEwh80TQVLZskmTHPwGMYcABfG83vFdvkBxkTEgpAwNEuC1FRU+0JzTxDmpO4cH02QiRHRAo2UkQBJQMeIpNKKIG8DCkhY9AxuRwAAAABJRU5ErkJggg==",
    
    "apple.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAIVBMVEUAAAD/lp3/Xmn/HCvdFyV+Nw60Ex51KAKcEBdUJAlUCQ5dkieqAAAAAXRSTlMAQObYZgAAAFhJREFUeNp9z0EOgEAIQ1GQ2jLc/8BmxhCNUbv7L2yw7+nR+/g9yNSQrqRzJCh1x+buW1BqWEOwAYEAEKgFIgESvAFnM1jWgkndppwJZoNVMvPsFklV708fJ30CoAEZcEMAAAAASUVORK5CYII=",
    
    "bread.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAFVBMVEVHcEz/xn3/1IX/0YL/xn3/xn3/xn3///8kNiFgAAAAAXRSTlMAQObYZgAAAFdJREFUeNqNj0EKgDAMBLMfgSp4/4MqHioKIrLsdMlOIIQ0ECBAWmSBAumRBQqkRxYokB5ZoEB6ZIEC6ZEFCqRHFiiQHlmgQHpkgQLpkQUKpEcWKJAX8QBZzAgNoKLYhgAAAABJRU5ErkJggg==",
    
    "cooked_porkchop.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAGFBMVEVHcEz/d0b/dEb/dEb/dEb/dEb/dEb/dEb///8T9KZnAAAAAnRSTlMAAHaTzTgAAABySURBVHicY2RgYBRgYmBABQwMr18wMDK+AEx/+cLAyPgVMH3rFgMD4zcG0PSbNwwMjN8ZQNNv3zIwMH5nAE2/fcvAwPidATT99i0DA+N3BtD027cMDIzfGUDTb98yMDB+ZwBNv33LwMD4nQHgPwYA51gRDUQnKJkAAAAASUVORK5CYII=",
    
    "cooked_beef.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAFVBMVEVHcEz/d0b/dEb/dEb/dEb/dEb/dEb///+TvIlRAAAAAXRSTlMAQObYZgAAAF5JREFUeNqNj0EKgDAMBLMfgSp4/4MqHioKIjJ0s0kLQwJpIEBmZIICmZEJCmRGJiiQGZmgQGZkggKZkQkKZEYmKJAZmaBAZmSCApmRCQpkRiYokBmZoEBmZIICeWEPa8cIDWqpHN8AAAAASUVORK5CYII=",
    
    "cooked_chicken.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAIVBMVEVHcEz/d0b/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb///8pJYwCAAAACnRSTlMAgEB/n7/f/98QAM3rEgAAAHNJREFUeNqNj0EKgDAMBLMfgSp4/4MqHioKIjJ0s0kLQwJpIEBmZIICmZEJCmRGJiiQGZmgQGZkggKZkQkKZEYmKJAZmaBAZmSCApmRCQpkRiYokBmZoEBmZIICmZEJCmRGJiiQGZmgQF7YA1u1CA2vUAt1AAAAAElFTkSuQmCC",
    
    "cooked_fish.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAHlBMVEVHcEz/d0b/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb///8WlG7vAAAACnRSTlMAgEB/n7/f/98QAM3rEgAAAHNJREFUeNqNj0EKgDAMBLMfgSp4/4MqHioKIjJ0s0kLQwJpIEBmZIICmZEJCmRGJiiQGZmgQGZkggKZkQkKZEYmKJAZmaBAZmSCApmRCQpkRiYokBmZoEBmZIICmZEJCmRGJiiQGZmgQF7YA1u1CA2vUAt1AAAAAElFTkSuQmCC",
    
    "cake.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAALVBMVEVHcEz/c0b/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb///9RRQ8RAAAADnRSTlMAgEB/n7/f7/8QECAwn3nJvQAAAHdJREFUeNqNj0EKgDAMBLMfgSp4/4MqHioKIjJ0s0kLQwJpIEBmZIICmZEJCmRGJiiQGZmgQGZkggKZkQkKZEYmKJAZmaBAZmSCApmRCQpkRiYokBmZoEBmZIICmZEJCmRGJiiQGZmgQGZkggJ5YQ9w1QgNqXwJfQAAAABJRU5ErkJggg==",
    
    "stick.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAFVBMVEVHcEz/d0b/dEb/dEb/dEb/dEb/dEb///+TvIlRAAAAAXRSTlMAQObYZgAAAF5JREFUeNqNj0EKgDAMBLMfgSp4/4MqHioKIjJ0s0kLQwJpIEBmZIICmZEJCmRGJiiQGZmgQGZkggKZkQkKZEYmKJAZmaBAZmSCApmRCQpkRiYokBmZoEBmZIICeWEPa8cIDWqpHN8AAAAASUVORK5CYII=",
    
    "wooden_pickaxe.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAIVBMVEVHcEz/d0b/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb///8pJYwCAAAACnRSTlMAgEB/n7/f/98QAM3rEgAAAHNJREFUeNqNj0EKgDAMBLMfgSp4/4MqHioKIjJ0s0kLQwJpIEBmZIICmZEJCmRGJiiQGZmgQGZkggKZkQkKZEYmKJAZmaBAZmSCApmRCQpkRiYokBmZoEBmZIICmZEJCmRGJiiQGZmgQF7YA1u1CA2vUAt1AAAAAElFTkSuQmCC",
    
    "stone_pickaxe.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAHlBMVEVHcEz/d0b/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb///8WlG7vAAAACnRSTlMAgEB/n7/f/98QAM3rEgAAAHNJREFUeNqNj0EKgDAMBLMfgSp4/4MqHioKIjJ0s0kLQwJpIEBmZIICmZEJCmRGJiiQGZmgQGZkggKZkQkKZEYmKJAZmaBAZmSCApmRCQpkRiYokBmZoEBmZIICmZEJCmRGJiiQGZmgQF7YA1u1CA2vUAt1AAAAAElFTkSuQmCC",
    
    "iron_pickaxe.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAALVBMVEVHcEz/c0b/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb///9RRQ8RAAAADnRSTlMAgEB/n7/f7/8QECAwn3nJvQAAAHdJREFUeNqNj0EKgDAMBLMfgSp4/4MqHioKIjJ0s0kLQwJpIEBmZIICmZEJCmRGJiiQGZmgQGZkggKZkQkKZEYmKJAZmaBAZmSCApmRCQpkRiYokBmZoEBmZIICmZEJCmRGJiiQGZmgQGZkggJ5YQ9w1QgNqXwJfQAAAABJRU5ErkJggg==",
    
    "gold_pickaxe.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAALVBMVEVHcEz/c0b/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb///9RRQ8RAAAADnRSTlMAgEB/n7/f7/8QECAwn3nJvQAAAHdJREFUeNqNj0EKgDAMBLMfgSp4/4MqHioKIjJ0s0kLQwJpIEBmZIICmZEJCmRGJiiQGZmgQGZkggKZkQkKZEYmKJAZmaBAZmSCApmRCQpkRiYokBmZoEBmZIICmZEJCmRGJiiQGZmgQGZkggJ5YQ9w1QgNqXwJfQAAAABJRU5ErkJggg==",
    
    "diamond_pickaxe.png": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAHlBMVEVHcEz/c0b/dEb/dEb/dEb/dEb/dEb/dEb/dEb/dEb///8WlG7vAAAACnRSTlMAgEB/n7/f/98QAM3rEgAAAHNJREFUeNqNj0EKgDAMBLMfgSp4/4MqHioKIjJ0s0kLQwJpIEBmZIICmZEJCmRGJiiQGZmgQGZkggKZkQkKZEYmKJAZmaBAZmSCApmRCQpkRiYokBmZoEBmZIICmZEJCmRGJiiQGZmgQF7YA1u1CA2vUAt1AAAAAElFTkSuQmCC"
}

# 游戏模式
class GameMode(Enum):
    SURVIVAL = 1      # 生存模式
    CREATIVE = 2      # 创造模式
    CLASSIC = 3       # 老版本生存模式

# 游戏配置
class Config:
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    CHUNK_SIZE = 16
    RENDER_DISTANCE = 8
    TILE_SIZE = 32
    GRAVITY = 0.5
    JUMP_FORCE = -12
    PLAYER_SPEED = 5
    INVENTORY_SLOTS = 9
    WORLD_HEIGHT = 256
    CLOUD_LEVEL = 180
    CLOUD_COUNT = 20
    
    # 昼夜循环速度（帧数）
    DAY_LENGTH = 36000  # 10分钟一个昼夜循环
    
    # 视频设置
    SHOW_CLOUDS = True
    AMBIENT_OCCLUSION = True  # 环境光遮蔽（地底变暗效果）
    DARK_FILTER_STRENGTH = 1.0  # 暗色滤镜强度 (0-1)
    
    # 网络配置
    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 5555
    
    # 颜色定义
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    BLUE = (0, 100, 255)
    BROWN = (139, 69, 19)
    GREEN = (34, 139, 34)
    SKY_BLUE = (135, 206, 235)
    NIGHT_SKY = (10, 10, 30)
    CLOUD_WHITE = (240, 240, 240)
    ORANGE = (255, 165, 0)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    PURPLE = (128, 0, 128)
    CYAN = (0, 255, 255)
    PLAYER_COLORS = [
        (255, 0, 0),    # 红
        (0, 255, 0),    # 绿
        (0, 0, 255),    # 蓝
        (255, 255, 0),  # 黄
        (255, 0, 255),  # 紫
        (0, 255, 255),  # 青
        (255, 128, 0),  # 橙
        (128, 0, 255),  # 紫罗兰
    ]

# 方块类型
class BlockType(Enum):
    AIR = 0
    GRASS = 1
    DIRT = 2
    STONE = 3
    WOOD = 4
    LEAVES = 5
    SAND = 6
    WATER = 7
    COBBLESTONE = 8
    BEDROCK = 9
    COAL_ORE = 10
    IRON_ORE = 11
    GOLD_ORE = 12
    DIAMOND_ORE = 13
    EMERALD_ORE = 14
    LAPIS_ORE = 15
    REDSTONE_ORE = 16
    GRAVEL = 17
    CLAY = 18
    SNOW = 19
    ICE = 20
    CLOUD = 21
    CRAFTING_TABLE = 22  # 工作台
    FURNACE = 23         # 熔炉
    CHEST = 24           # 箱子
    WHEAT = 25           # 小麦
    APPLE = 26           # 苹果
    BREAD = 27           # 面包
    COOKED_PORKCHOP = 28 # 熟猪排
    COOKED_BEEF = 29     # 熟牛排
    COOKED_CHICKEN = 30  # 熟鸡肉
    COOKED_FISH = 31     # 熟鱼
    CAKE = 32            # 蛋糕
    STICK = 33           # 木棍
    WOODEN_PICKAXE = 34  # 木镐
    STONE_PICKAXE = 35   # 石镐
    IRON_PICKAXE = 36    # 铁镐
    GOLD_PICKAXE = 37    # 金镐
    DIAMOND_PICKAXE = 38 # 钻石镐

# 方块属性
BLOCK_PROPERTIES = {
    BlockType.AIR: {"name": "空气", "breakable": False, "color": None, "hardness": 0, "drop": None, "placeable": False},
    BlockType.GRASS: {"name": "草", "breakable": True, "color": (34, 139, 34), "hardness": 1, "drop": BlockType.DIRT, "placeable": True},
    BlockType.DIRT: {"name": "泥土", "breakable": True, "color": (139, 69, 19), "hardness": 1, "drop": BlockType.DIRT, "placeable": True},
    BlockType.STONE: {"name": "石头", "breakable": True, "color": (128, 128, 128), "hardness": 3, "drop": BlockType.COBBLESTONE, "placeable": True},
    BlockType.WOOD: {"name": "木头", "breakable": True, "color": (160, 82, 45), "hardness": 2, "drop": BlockType.WOOD, "placeable": True},
    BlockType.LEAVES: {"name": "树叶", "breakable": True, "color": (34, 139, 34), "hardness": 0.5, "drop": None, "placeable": True},
    BlockType.SAND: {"name": "沙子", "breakable": True, "color": (255, 255, 0), "hardness": 0.5, "drop": BlockType.SAND, "placeable": True},
    BlockType.WATER: {"name": "水", "breakable": False, "color": (0, 0, 255, 128), "hardness": 0, "drop": None, "placeable": False},
    BlockType.COBBLESTONE: {"name": "圆石", "breakable": True, "color": (100, 100, 100), "hardness": 3, "drop": BlockType.COBBLESTONE, "placeable": True},
    BlockType.BEDROCK: {"name": "基岩", "breakable": False, "color": (30, 30, 30), "hardness": -1, "drop": None, "placeable": False},
    BlockType.COAL_ORE: {"name": "煤矿", "breakable": True, "color": (30, 30, 30), "hardness": 3, "drop": BlockType.COAL_ORE, "placeable": True},
    BlockType.IRON_ORE: {"name": "铁矿", "breakable": True, "color": (192, 192, 192), "hardness": 3, "drop": BlockType.IRON_ORE, "placeable": True},
    BlockType.GOLD_ORE: {"name": "金矿", "breakable": True, "color": (255, 215, 0), "hardness": 3, "drop": BlockType.GOLD_ORE, "placeable": True},
    BlockType.DIAMOND_ORE: {"name": "钻石矿", "breakable": True, "color": (0, 255, 255), "hardness": 5, "drop": BlockType.DIAMOND_ORE, "placeable": True},
    BlockType.EMERALD_ORE: {"name": "绿宝石矿", "breakable": True, "color": (0, 255, 0), "hardness": 4, "drop": BlockType.EMERALD_ORE, "placeable": True},
    BlockType.LAPIS_ORE: {"name": "青金石矿", "breakable": True, "color": (0, 0, 255), "hardness": 3, "drop": BlockType.LAPIS_ORE, "placeable": True},
    BlockType.REDSTONE_ORE: {"name": "红石矿", "breakable": True, "color": (255, 0, 0), "hardness": 3, "drop": BlockType.REDSTONE_ORE, "placeable": True},
    BlockType.GRAVEL: {"name": "砾石", "breakable": True, "color": (128, 128, 128), "hardness": 1, "drop": BlockType.GRAVEL, "placeable": True},
    BlockType.CLAY: {"name": "粘土", "breakable": True, "color": (160, 160, 180), "hardness": 1, "drop": BlockType.CLAY, "placeable": True},
    BlockType.SNOW: {"name": "雪", "breakable": True, "color": (255, 255, 255), "hardness": 0.2, "drop": BlockType.SNOW, "placeable": True},
    BlockType.ICE: {"name": "冰", "breakable": True, "color": (200, 230, 255), "hardness": 0.5, "drop": BlockType.ICE, "placeable": True},
    BlockType.CLOUD: {"name": "云", "breakable": False, "color": (255, 255, 255, 200), "hardness": 0, "drop": None, "placeable": False},
    BlockType.CRAFTING_TABLE: {"name": "工作台", "breakable": True, "color": (139, 69, 19), "hardness": 2, "drop": BlockType.CRAFTING_TABLE, "placeable": True},
    BlockType.FURNACE: {"name": "熔炉", "breakable": True, "color": (100, 100, 100), "hardness": 3, "drop": BlockType.FURNACE, "placeable": True},
    BlockType.CHEST: {"name": "箱子", "breakable": True, "color": (160, 82, 45), "hardness": 2, "drop": BlockType.CHEST, "placeable": True},
    BlockType.WHEAT: {"name": "小麦", "breakable": False, "color": (255, 255, 0), "hardness": 0, "drop": BlockType.WHEAT, "placeable": False},
    BlockType.APPLE: {"name": "苹果", "breakable": False, "color": (255, 0, 0), "hardness": 0, "drop": BlockType.APPLE, "food": 4, "placeable": False},
    BlockType.BREAD: {"name": "面包", "breakable": False, "color": (255, 215, 0), "hardness": 0, "drop": BlockType.BREAD, "food": 5, "placeable": False},
    BlockType.COOKED_PORKCHOP: {"name": "熟猪排", "breakable": False, "color": (255, 192, 203), "hardness": 0, "drop": BlockType.COOKED_PORKCHOP, "food": 8, "placeable": False},
    BlockType.COOKED_BEEF: {"name": "熟牛排", "breakable": False, "color": (165, 42, 42), "hardness": 0, "drop": BlockType.COOKED_BEEF, "food": 8, "placeable": False},
    BlockType.COOKED_CHICKEN: {"name": "熟鸡肉", "breakable": False, "color": (255, 255, 224), "hardness": 0, "drop": BlockType.COOKED_CHICKEN, "food": 6, "placeable": False},
    BlockType.COOKED_FISH: {"name": "熟鱼", "breakable": False, "color": (255, 228, 196), "hardness": 0, "drop": BlockType.COOKED_FISH, "food": 5, "placeable": False},
    BlockType.CAKE: {"name": "蛋糕", "breakable": False, "color": (255, 192, 203), "hardness": 0, "drop": BlockType.CAKE, "food": 2, "placeable": False},
    BlockType.STICK: {"name": "木棍", "breakable": False, "color": (160, 82, 45), "hardness": 0, "drop": BlockType.STICK, "placeable": False},
    BlockType.WOODEN_PICKAXE: {"name": "木镐", "breakable": False, "color": (160, 82, 45), "hardness": 0, "drop": BlockType.WOODEN_PICKAXE, "placeable": False},
    BlockType.STONE_PICKAXE: {"name": "石镐", "breakable": False, "color": (128, 128, 128), "hardness": 0, "drop": BlockType.STONE_PICKAXE, "placeable": False},
    BlockType.IRON_PICKAXE: {"name": "铁镐", "breakable": False, "color": (192, 192, 192), "hardness": 0, "drop": BlockType.IRON_PICKAXE, "placeable": False},
    BlockType.GOLD_PICKAXE: {"name": "金镐", "breakable": False, "color": (255, 215, 0), "hardness": 0, "drop": BlockType.GOLD_PICKAXE, "placeable": False},
    BlockType.DIAMOND_PICKAXE: {"name": "钻石镐", "breakable": False, "color": (0, 255, 255), "hardness": 0, "drop": BlockType.DIAMOND_PICKAXE, "placeable": False},
}


# ==================== 暗色滤镜类 ====================

class DarkFilter:
    """从dark.png图片读取颜色渐变，应用到地底滤镜"""
    
    def __init__(self):
        self.filter_texture = None
        self.filter_width = 0
        self.filter_height = 0
        self.color_gradient = []  # 存储每行的颜色值
        self.load_filter()
    
    def load_filter(self):
        """加载dark.png图片并提取颜色渐变"""
        dark_png_path = os.path.join(GAME_ROOT, 'dark.png')
        
        if os.path.exists(dark_png_path):
            try:
                # 加载图片
                img = pygame.image.load(dark_png_path).convert_alpha()
                self.filter_width = img.get_width()
                self.filter_height = img.get_height()
                
                # 提取每行的颜色（从上到下）
                for y in range(self.filter_height):
                    # 获取该行最左边的像素颜色
                    color = img.get_at((0, y))
                    self.color_gradient.append(color)
                
                print(f"加载滤镜图片: {dark_png_path}")
                print(f"  尺寸: {self.filter_width}x{self.filter_height}")
                print(f"  顶部颜色: {self.color_gradient[0] if self.color_gradient else 'None'}")
                print(f"  底部颜色: {self.color_gradient[-1] if self.color_gradient else 'None'}")
                
            except Exception as e:
                print(f"加载滤镜图片失败: {e}")
                self.create_default_gradient()
        else:
            print(f"未找到滤镜图片: {dark_png_path}")
            self.create_default_gradient()
    
    def create_default_gradient(self):
        """创建默认的渐变滤镜（白到黑）"""
        self.filter_height = Config.WORLD_HEIGHT * Config.TILE_SIZE
        self.filter_width = Config.SCREEN_WIDTH
        
        # 创建默认渐变（上白下黑）
        for y in range(self.filter_height):
            factor = y / self.filter_height
            alpha = int(255 * (1 - factor * Config.DARK_FILTER_STRENGTH))
            self.color_gradient.append((255, 255, 255, alpha))
        
        print("创建默认渐变滤镜")
    
    def apply_to_surface(self, surface, camera_y):
        """将滤镜应用到表面（基于相机Y坐标）"""
        if not self.color_gradient:
            return
        
        # 创建临时滤镜表面
        filter_surf = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.SRCALPHA)
        
        for y in range(Config.SCREEN_HEIGHT):
            # 计算深度因子
            world_y = camera_y + y
            if world_y > Config.CLOUD_LEVEL * Config.TILE_SIZE:
                depth = world_y - Config.CLOUD_LEVEL * Config.TILE_SIZE
                max_depth = (Config.WORLD_HEIGHT - Config.CLOUD_LEVEL) * Config.TILE_SIZE
                depth_factor = min(1.0, depth / max_depth)
                
                # 从颜色渐变中获取颜色
                filter_idx = int(depth_factor * (self.filter_height - 1))
                filter_idx = min(filter_idx, self.filter_height - 1)
                
                if filter_idx < len(self.color_gradient):
                    color = self.color_gradient[filter_idx]
                    # 应用滤镜强度
                    if Config.DARK_FILTER_STRENGTH < 1.0:
                        alpha = int(color[3] * Config.DARK_FILTER_STRENGTH)
                        color = (color[0], color[1], color[2], alpha)
                    
                    pygame.draw.line(filter_surf, color, (0, y), (Config.SCREEN_WIDTH, y), 1)
        
        # 混合滤镜
        surface.blit(filter_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


# ==================== 区块类 ====================

class Chunk:
    def __init__(self, chunk_x):
        self.chunk_x = chunk_x
        self.blocks = {}
        self.generated = False
        self.trees = []
        self.caves = []
        
    def get_block(self, x, y):
        local_x = x % Config.CHUNK_SIZE
        key = (local_x, y)
        return self.blocks.get(key, BlockType.AIR)
    
    def set_block(self, x, y, block_type):
        local_x = x % Config.CHUNK_SIZE
        key = (local_x, y)
        if block_type == BlockType.AIR:
            self.blocks.pop(key, None)
        else:
            self.blocks[key] = block_type
    
    def generate(self, seed):
        if self.generated:
            return
        
        random.seed(seed + self.chunk_x)
        
        for local_x in range(Config.CHUNK_SIZE):
            world_x = self.chunk_x * Config.CHUNK_SIZE + local_x
            
            height_noise = math.sin(world_x * 0.01) * 10 + math.sin(world_x * 0.05) * 5
            ground_height = int(Config.CLOUD_LEVEL - 50 + height_noise)
            
            for y in range(ground_height, Config.WORLD_HEIGHT):
                if y == ground_height:
                    self.set_block(world_x, y, BlockType.GRASS)
                elif y < ground_height + 4:
                    self.set_block(world_x, y, BlockType.DIRT)
                elif y < Config.WORLD_HEIGHT - 1:
                    block = BlockType.STONE
                    depth = Config.WORLD_HEIGHT - y
                    
                    if depth > 10 and random.random() < 0.02:
                        block = BlockType.COAL_ORE
                    elif depth > 20 and random.random() < 0.015:
                        block = BlockType.IRON_ORE
                    elif depth > 30 and random.random() < 0.008:
                        block = BlockType.GOLD_ORE
                    elif depth > 40 and random.random() < 0.005:
                        block = BlockType.DIAMOND_ORE
                    elif depth > 30 and random.random() < 0.003:
                        block = BlockType.EMERALD_ORE
                    
                    self.set_block(world_x, y, block)
                else:
                    self.set_block(world_x, y, BlockType.BEDROCK)
            
            if random.random() < 0.1 and world_x % 8 != 0:
                if self.get_block(world_x, ground_height) == BlockType.GRASS:
                    self.generate_tree(world_x, ground_height - 1)
        
        self.generated = True
    
    def generate_tree(self, x, y):
        if y < 5:
            return
        
        tree_height = random.randint(4, 6)
        
        for i in range(tree_height):
            if y - i >= 0:
                self.set_block(x, y - i, BlockType.WOOD)
        
        leaf_start = y - tree_height + 1
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                leaf_x = x + dx
                leaf_y = leaf_start + dy
                if (abs(dx) + abs(dy) <= 3 and 
                    leaf_y > 0 and 
                    self.get_block(leaf_x, leaf_y) == BlockType.AIR):
                    self.set_block(leaf_x, leaf_y, BlockType.LEAVES)
    
    def to_dict(self):
        return {
            'chunk_x': self.chunk_x,
            'blocks': [(key[0], key[1], block.value) for key, block in self.blocks.items()],
            'generated': self.generated,
            'trees': self.trees,
            'caves': self.caves
        }
    
    @staticmethod
    def from_dict(data):
        chunk = Chunk(data['chunk_x'])
        chunk.generated = data['generated']
        chunk.trees = data['trees']
        chunk.caves = data['caves']
        for local_x, y, block_value in data['blocks']:
            chunk.blocks[(local_x, y)] = BlockType(block_value)
        return chunk


# ==================== 世界类 ====================

class World:
    def __init__(self, seed=None):
        self.seed = seed if seed is not None else random.randint(-10000, 10000)
        self.chunks = {}
        self.player_spawn = (0, Config.CLOUD_LEVEL - 50)
        
    def get_chunk(self, chunk_x):
        if chunk_x not in self.chunks:
            if len(self.chunks) > Config.RENDER_DISTANCE * 2 + 5:
                to_remove = []
                for cx in self.chunks:
                    if abs(cx - chunk_x) > Config.RENDER_DISTANCE + 2:
                        to_remove.append(cx)
                for cx in to_remove:
                    del self.chunks[cx]
            
            self.chunks[chunk_x] = Chunk(chunk_x)
            self.chunks[chunk_x].generate(self.seed)
        return self.chunks[chunk_x]
    
    def get_block(self, x, y):
        if y < 0 or y >= Config.WORLD_HEIGHT:
            return BlockType.AIR
        
        chunk_x = x // Config.CHUNK_SIZE
        chunk = self.get_chunk(chunk_x)
        return chunk.get_block(x, y)
    
    def set_block(self, x, y, block_type):
        if y < 0 or y >= Config.WORLD_HEIGHT:
            return
        
        chunk_x = x // Config.CHUNK_SIZE
        chunk = self.get_chunk(chunk_x)
        chunk.set_block(x, y, block_type)
    
    def save(self, filename):
        save_data = {"seed": self.seed, "player_spawn": self.player_spawn, "chunks": {}}
        for chunk_x, chunk in self.chunks.items():
            if chunk.blocks:
                save_data["chunks"][str(chunk_x)] = chunk.to_dict()
        
        filepath = os.path.join(SAVES_PATH, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False)
        return filepath
    
    def load(self, filename):
        filepath = os.path.join(SAVES_PATH, filename)
        if not os.path.exists(filepath):
            return False
        
        with open(filepath, 'r', encoding='utf-8') as f:
            save_data = json.load(f)
        
        self.seed = save_data["seed"]
        self.player_spawn = tuple(save_data["player_spawn"])
        self.chunks = {}
        
        for chunk_x_str, chunk_data in save_data["chunks"].items():
            chunk_x = int(chunk_x_str)
            self.chunks[chunk_x] = Chunk.from_dict(chunk_data)
        return True
    
    def to_dict(self):
        return {
            'seed': self.seed,
            'player_spawn': self.player_spawn,
            'chunks': {str(k): v.to_dict() for k, v in self.chunks.items()}
        }
    
    @staticmethod
    def from_dict(data):
        world = World(data['seed'])
        world.player_spawn = tuple(data['player_spawn'])
        for chunk_x_str, chunk_data in data['chunks'].items():
            chunk_x = int(chunk_x_str)
            world.chunks[chunk_x] = Chunk.from_dict(chunk_data)
        return world


# ==================== 云层类 ====================

class Cloud:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = random.uniform(0.2, 0.5)
        self.parts = []
        
        for i in range(random.randint(3, 6)):
            part_x = random.randint(-width//2, width//2)
            part_y = random.randint(-height//4, height//4)
            part_w = random.randint(width//3, width//2)
            part_h = random.randint(height//3, height//2)
            self.parts.append((part_x, part_y, part_w, part_h))
    
    def update(self):
        self.x += self.speed
        if self.x > Config.SCREEN_WIDTH + 200:
            self.x = -200
    
    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x * 0.3
        for part_x, part_y, w, h in self.parts:
            rect = pygame.Rect(screen_x + part_x, self.y + part_y, w, h)
            pygame.draw.ellipse(screen, Config.CLOUD_WHITE, rect)


# ==================== 物品类 ====================

class Item:
    def __init__(self, block_type, count=1):
        self.block_type = block_type
        self.count = count
        self.name = BLOCK_PROPERTIES[block_type]["name"]
    
    def add(self, count=1):
        self.count += count
    
    def remove(self, count=1):
        if self.count >= count:
            self.count -= count
            return True
        return False


# ==================== 背包类 ====================

class Inventory:
    def __init__(self, size=36):
        self.size = size
        self.slots = [None] * size
        self.selected_hotbar = 0
        
    def add_item(self, block_type, count=1):
        for i in range(self.size):
            if self.slots[i] and self.slots[i].block_type == block_type:
                self.slots[i].add(count)
                return True
        
        for i in range(self.size):
            if self.slots[i] is None:
                self.slots[i] = Item(block_type, count)
                return True
        return False
    
    def remove_item(self, block_type, count=1):
        for i in range(self.size):
            if self.slots[i] and self.slots[i].block_type == block_type:
                if self.slots[i].count >= count:
                    self.slots[i].remove(count)
                    if self.slots[i].count <= 0:
                        self.slots[i] = None
                    return True
        return False
    
    def get_selected_item(self):
        if self.selected_hotbar < len(self.slots):
            return self.slots[self.selected_hotbar]
        return None
    
    def get_selected_block(self):
        item = self.get_selected_item()
        if item and item.block_type != BlockType.AIR:
            return item.block_type
        return BlockType.AIR
    
    def has_item(self, block_type):
        for slot in self.slots:
            if slot and slot.block_type == block_type and slot.count > 0:
                return True
        return False
    
    def get_item_count(self, block_type):
        count = 0
        for slot in self.slots:
            if slot and slot.block_type == block_type:
                count += slot.count
        return count
    
    def select_hotbar(self, index):
        if 0 <= index <= 8:
            self.selected_hotbar = index
    
    def scroll_hotbar(self, direction):
        self.selected_hotbar = (self.selected_hotbar + direction) % 9
    
    def get_hotbar_items(self):
        items = []
        for i in range(9):
            if i < len(self.slots):
                items.append(self.slots[i])
            else:
                items.append(None)
        return items


# ==================== 中文支持类 ====================

class ChineseFont:
    def __init__(self):
        self.font = None
        self.small_font = None
        self.big_font = None
        self.load_font()
    
    def load_font(self):
        font_names = [
            'simhei.ttf',
            'msyh.ttc',
            'simsun.ttc',
            'C:/Windows/Fonts/simhei.ttf',
            'C:/Windows/Fonts/msyh.ttc',
        ]
        
        for font_name in font_names:
            try:
                if os.path.exists(font_name):
                    self.font = pygame.font.Font(font_name, 36)
                    self.small_font = pygame.font.Font(font_name, 24)
                    self.big_font = pygame.font.Font(font_name, 48)
                    print(f"加载字体: {font_name}")
                    return
            except:
                continue
        
        print("未找到中文字体，使用默认字体")
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 48)
    
    def render(self, text, antialias, color, size='normal'):
        if size == 'normal':
            return self.font.render(text, antialias, color)
        elif size == 'small':
            return self.small_font.render(text, antialias, color)
        elif size == 'big':
            return self.big_font.render(text, antialias, color)


# ==================== 玩家类 ====================

class Player:
    def __init__(self, x, y, player_id=None, name="Player", skin_file=None):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.width = Config.TILE_SIZE * 0.8
        self.height = Config.TILE_SIZE * 1.5
        self.on_ground = False
        self.selected_slot = 0
        self.health = 100
        self.hunger = 100
        self.player_id = player_id
        self.name = name
        
        # 游戏模式相关
        self.game_mode = GameMode.SURVIVAL
        self.can_fly = False
        self.flying = False
        self.infinite_items = False
        self.block_break_progress = 0
        self.breaking_block = None
        
        # 背包
        self.inventory = Inventory()
        
        # 初始化生存模式背包
        self.init_survival_inventory()
        
        # 皮肤相关
        self.skin = None
        self.skin_file = skin_file
        self.load_skin()
    
    def init_survival_inventory(self):
        """初始化生存模式背包"""
        self.inventory.add_item(BlockType.GRASS, 64)
        self.inventory.add_item(BlockType.DIRT, 64)
        self.inventory.add_item(BlockType.STONE, 64)
        self.inventory.add_item(BlockType.WOOD, 64)
        self.inventory.add_item(BlockType.COBBLESTONE, 64)
        self.inventory.add_item(BlockType.SAND, 64)
        self.inventory.add_item(BlockType.COAL_ORE, 32)
        self.inventory.add_item(BlockType.IRON_ORE, 32)
        self.inventory.add_item(BlockType.APPLE, 10)
    
    def set_game_mode(self, mode):
        """设置游戏模式"""
        self.game_mode = mode
        if mode == GameMode.CREATIVE:
            self.can_fly = True
            self.infinite_items = True
        elif mode == GameMode.SURVIVAL:
            self.can_fly = False
            self.infinite_items = False
            self.flying = False
        elif mode == GameMode.CLASSIC:
            self.can_fly = False
            self.infinite_items = False
            self.flying = False
    
    def load_skin(self):
        """加载玩家皮肤"""
        if self.skin_file and os.path.exists(self.skin_file):
            try:
                skin_texture = pygame.image.load(self.skin_file).convert_alpha()
                self.skin = pygame.transform.scale(skin_texture, (int(self.width), int(self.height)))
                print(f"加载皮肤: {self.skin_file}")
            except Exception as e:
                print(f"皮肤加载失败: {e}")
                self.skin = None
        else:
            self.skin = None
    
    def set_skin(self, skin_file):
        """设置新皮肤"""
        self.skin_file = skin_file
        self.load_skin()
    
    def update(self, world):
        # 重力（除非在创造模式飞行）
        if not (self.game_mode == GameMode.CREATIVE and self.flying):
            self.vy += Config.GRAVITY
        
        new_x = self.x + self.vx
        new_y = self.y + self.vy
        
        # X轴碰撞
        if not self.check_collision(world, new_x, self.y):
            self.x = new_x
        else:
            self.vx = 0
        
        # Y轴碰撞    
        if not self.check_collision(world, self.x, new_y):
            self.y = new_y
            self.on_ground = False
        else:
            if self.vy > 0:
                self.on_ground = True
            self.vy = 0
        
        # 掉出世界
        if self.y > Config.WORLD_HEIGHT * Config.TILE_SIZE:
            self.respawn(world)
        
        # 更新生命值和饱食度（生存模式）
        if self.game_mode == GameMode.SURVIVAL:
            self.update_hunger_health()
    
    def update_hunger_health(self):
        """更新饱食度和生命值"""
        if random.random() < 0.0005:
            if self.hunger > 0:
                self.hunger = max(0, self.hunger - 1)
        
        if self.vx != 0 or self.vy != 0:
            if random.random() < 0.001:
                if self.hunger > 0:
                    self.hunger = max(0, self.hunger - 1)
        
        if self.hunger <= 0:
            if random.random() < 0.001:
                self.health = max(0, self.health - 1)
        
        self.health = min(100, self.health)
        self.hunger = min(100, self.hunger)
        
        if self.health <= 0:
            return False
        return True
    
    def eat_food(self, block_type):
        """吃东西恢复饱食度"""
        if block_type in BLOCK_PROPERTIES and 'food' in BLOCK_PROPERTIES[block_type]:
            food_value = BLOCK_PROPERTIES[block_type]['food']
            self.hunger = min(100, self.hunger + food_value)
            return True
        return False
    
    def heal(self, amount):
        """恢复生命值"""
        self.health = min(100, self.health + amount)
    
    def check_collision(self, world, x, y):
        left = int(x // Config.TILE_SIZE)
        right = int((x + self.width) // Config.TILE_SIZE)
        top = int(y // Config.TILE_SIZE)
        bottom = int((y + self.height) // Config.TILE_SIZE)
        
        for tile_y in range(top, bottom + 1):
            for tile_x in range(left, right + 1):
                block = world.get_block(tile_x, tile_y)
                if block != BlockType.AIR and BLOCK_PROPERTIES[block]["breakable"]:
                    return True
        return False
    
    def jump(self):
        if self.game_mode == GameMode.CREATIVE and self.flying:
            self.vy = -Config.PLAYER_SPEED * 1.5
        elif self.on_ground:
            self.vy = Config.JUMP_FORCE
            self.on_ground = False
    
    def descend(self):
        """下降（用于创造模式飞行）"""
        if self.game_mode == GameMode.CREATIVE and self.flying:
            self.vy = Config.PLAYER_SPEED * 1.5
    
    def respawn(self, world):
        self.x = world.player_spawn[0] * Config.TILE_SIZE
        self.y = world.player_spawn[1] * Config.TILE_SIZE
        self.vx = 0
        self.vy = 0
        self.health = 100
        self.hunger = 100
    
    def get_selected_block(self):
        """获取当前选中的方块类型"""
        if self.game_mode == GameMode.CREATIVE and self.infinite_items:
            item = self.inventory.get_selected_item()
            if item:
                return item.block_type
            for i in range(self.inventory.size):
                if self.inventory.slots[i]:
                    return self.inventory.slots[i].block_type
            return BlockType.AIR
        else:
            return self.inventory.get_selected_block()
    
    def add_block(self, block_type, count=1):
        """添加方块到背包"""
        if self.game_mode == GameMode.CREATIVE:
            return True
        return self.inventory.add_item(block_type, count)
    
    def remove_block(self, block_type, count=1):
        """从背包移除方块"""
        if self.game_mode == GameMode.CREATIVE:
            return True
        return self.inventory.remove_item(block_type, count)
    
    def start_breaking(self, x, y):
        """开始破坏方块"""
        self.breaking_block = (x, y)
        self.block_break_progress = 0
    
    def stop_breaking(self):
        """停止破坏方块"""
        self.breaking_block = None
        self.block_break_progress = 0
    
    def update_breaking(self, world):
        """更新方块破坏进度"""
        if self.breaking_block:
            x, y = self.breaking_block
            block = world.get_block(x, y)
            
            if block == BlockType.AIR or not BLOCK_PROPERTIES[block]["breakable"]:
                self.stop_breaking()
                return
            
            hardness = BLOCK_PROPERTIES[block]["hardness"]
            
            if self.game_mode == GameMode.CREATIVE:
                return True
            elif self.game_mode == GameMode.CLASSIC:
                return True
            else:
                self.block_break_progress += 1
                if self.block_break_progress >= hardness * 20:
                    return True
            
        return False
    
    def get_break_progress(self):
        """获取破坏进度"""
        if self.breaking_block:
            return self.block_break_progress
        return 0
    
    def draw(self, screen, camera_x, camera_y, is_local=False):
        """绘制玩家"""
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        if screen_x + self.width > 0 and screen_x < Config.SCREEN_WIDTH and \
           screen_y + self.height > 0 and screen_y < Config.SCREEN_HEIGHT:
            
            if self.skin:
                screen.blit(self.skin, (screen_x, screen_y))
            else:
                if is_local:
                    color = Config.BLUE
                else:
                    color = Config.PLAYER_COLORS[self.player_id % len(Config.PLAYER_COLORS)] if self.player_id else Config.GRAY
                
                player_rect = pygame.Rect(int(screen_x), int(screen_y), int(self.width), int(self.height))
                pygame.draw.rect(screen, color, player_rect)
                pygame.draw.rect(screen, Config.BLACK, player_rect, 2)
            
            # 绘制玩家名称
            font = pygame.font.Font(None, 20)
            name_text = font.render(self.name, True, Config.WHITE)
            name_rect = name_text.get_rect(center=(screen_x + self.width//2, screen_y - 10))
            
            bg_rect = name_rect.inflate(4, 2)
            pygame.draw.rect(screen, (0, 0, 0, 128), bg_rect)
            screen.blit(name_text, name_rect)


# ==================== 网络玩家类 ====================

class NetworkPlayer:
    def __init__(self, player_id, x=0, y=0, name="Player", skin_file=None):
        self.player_id = player_id
        self.x = x
        self.y = y
        self.name = name
        self.width = Config.TILE_SIZE * 0.8
        self.height = Config.TILE_SIZE * 1.5
        self.last_update = time.time()
        self.color = Config.PLAYER_COLORS[player_id % len(Config.PLAYER_COLORS)]
        
        self.skin = None
        if skin_file and os.path.exists(skin_file):
            try:
                skin_texture = pygame.image.load(skin_file).convert_alpha()
                self.skin = pygame.transform.scale(skin_texture, (int(self.width), int(self.height)))
            except:
                self.skin = None
    
    def update_position(self, x, y):
        self.x = x
        self.y = y
        self.last_update = time.time()
    
    def draw(self, screen, camera_x, camera_y):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        if screen_x + self.width > 0 and screen_x < Config.SCREEN_WIDTH and \
           screen_y + self.height > 0 and screen_y < Config.SCREEN_HEIGHT:
            
            if self.skin:
                screen.blit(self.skin, (screen_x, screen_y))
            else:
                player_rect = pygame.Rect(int(screen_x), int(screen_y), int(self.width), int(self.height))
                pygame.draw.rect(screen, self.color, player_rect)
                pygame.draw.rect(screen, Config.BLACK, player_rect, 2)
            
            font = pygame.font.Font(None, 20)
            name_text = font.render(self.name, True, Config.WHITE)
            name_rect = name_text.get_rect(center=(screen_x + self.width//2, screen_y - 10))
            bg_rect = name_rect.inflate(4, 2)
            pygame.draw.rect(screen, (0, 0, 0, 128), bg_rect)
            screen.blit(name_text, name_rect)


# ==================== 合成系统 ====================

class Recipe:
    """合成配方类"""
    def __init__(self, result, pattern, count=1):
        self.result = result
        self.pattern = pattern
        self.count = count
    
    def matches(self, grid):
        if len(grid) != 3 or len(grid[0]) != 3:
            return False
        
        for i in range(3):
            for j in range(3):
                if self.pattern[i][j] != grid[i][j]:
                    return False
        return True


class CraftingManager:
    """合成管理器"""
    def __init__(self):
        self.recipes = []
        self.init_recipes()
    
    def init_recipes(self):
        # 木棍
        self.recipes.append(Recipe(
            BlockType.STICK,
            [
                [BlockType.WOOD, None, None],
                [BlockType.WOOD, None, None],
                [None, None, None]
            ],
            4
        ))
        
        # 工作台
        self.recipes.append(Recipe(
            BlockType.CRAFTING_TABLE,
            [
                [BlockType.WOOD, BlockType.WOOD, None],
                [BlockType.WOOD, BlockType.WOOD, None],
                [None, None, None]
            ]
        ))
        
        # 木镐
        self.recipes.append(Recipe(
            BlockType.WOODEN_PICKAXE,
            [
                [BlockType.WOOD, BlockType.WOOD, BlockType.WOOD],
                [None, BlockType.STICK, None],
                [None, BlockType.STICK, None]
            ]
        ))
        
        # 石镐
        self.recipes.append(Recipe(
            BlockType.STONE_PICKAXE,
            [
                [BlockType.COBBLESTONE, BlockType.COBBLESTONE, BlockType.COBBLESTONE],
                [None, BlockType.STICK, None],
                [None, BlockType.STICK, None]
            ]
        ))
        
        # 铁镐
        self.recipes.append(Recipe(
            BlockType.IRON_PICKAXE,
            [
                [BlockType.IRON_ORE, BlockType.IRON_ORE, BlockType.IRON_ORE],
                [None, BlockType.STICK, None],
                [None, BlockType.STICK, None]
            ]
        ))
        
        # 金镐
        self.recipes.append(Recipe(
            BlockType.GOLD_PICKAXE,
            [
                [BlockType.GOLD_ORE, BlockType.GOLD_ORE, BlockType.GOLD_ORE],
                [None, BlockType.STICK, None],
                [None, BlockType.STICK, None]
            ]
        ))
        
        # 钻石镐
        self.recipes.append(Recipe(
            BlockType.DIAMOND_PICKAXE,
            [
                [BlockType.DIAMOND_ORE, BlockType.DIAMOND_ORE, BlockType.DIAMOND_ORE],
                [None, BlockType.STICK, None],
                [None, BlockType.STICK, None]
            ]
        ))
        
        # 面包
        self.recipes.append(Recipe(
            BlockType.BREAD,
            [
                [BlockType.WHEAT, BlockType.WHEAT, BlockType.WHEAT],
                [None, None, None],
                [None, None, None]
            ]
        ))
    
    def craft(self, grid, inventory):
        for recipe in self.recipes:
            if recipe.matches(grid):
                materials_ok = True
                material_counts = {}
                
                for i in range(3):
                    for j in range(3):
                        material = grid[i][j]
                        if material:
                            if material not in material_counts:
                                material_counts[material] = 0
                            material_counts[material] += 1
                
                for material, count_needed in material_counts.items():
                    if inventory.get_item_count(material) < count_needed:
                        materials_ok = False
                        break
                
                if materials_ok:
                    for i in range(3):
                        for j in range(3):
                            material = grid[i][j]
                            if material:
                                inventory.remove_item(material)
                    
                    inventory.add_item(recipe.result, recipe.count)
                    return recipe.result, recipe.count
        
        return None, 0


# ==================== 游戏主类 ====================

class Game:
    def __init__(self, online_mode=False, is_server=False, host=None, port=None):
        pygame.init()
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption("2D Minecraft")
        self.clock = pygame.time.Clock()
        
        self.chinese_font = ChineseFont()
        
        # 暗色滤镜
        self.dark_filter = DarkFilter()
        
        # 合成管理器
        self.crafting_manager = CraftingManager()
        self.show_crafting = False
        self.crafting_grid = [[None for _ in range(3)] for _ in range(3)]
        self.crafting_result = None
        
        # 2x2合成
        self.show_crafting_2x2 = False
        self.crafting_grid_2x2 = [[None for _ in range(2)] for _ in range(2)]
        self.crafting_result_2x2 = None
        
        # 网络相关
        self.online_mode = online_mode
        self.is_server = is_server
        self.server = None
        self.client = None
        self.network_players = {}
        self.last_position_send = 0
        self.position_send_interval = 50
        
        # 初始化世界
        self.world = World()
        
        # 皮肤相关
        self.available_skins = self.get_available_skins()
        self.selected_skin = 0
        self.show_skin_menu = False
        
        # 创建玩家
        default_skin = os.path.join(SKINS_PATH, 'default.png')
        if os.path.exists(default_skin):
            self.player = Player(
                self.world.player_spawn[0] * Config.TILE_SIZE,
                self.world.player_spawn[1] * Config.TILE_SIZE,
                name="Player",
                skin_file=default_skin
            )
        else:
            self.player = Player(
                self.world.player_spawn[0] * Config.TILE_SIZE,
                self.world.player_spawn[1] * Config.TILE_SIZE,
                name="Player"
            )
        
        # 相机
        self.camera_x = 0
        self.camera_y = 0
        
        # 云层
        self.clouds = []
        for i in range(Config.CLOUD_COUNT):
            x = random.randint(-200, Config.SCREEN_WIDTH + 200)
            y = Config.CLOUD_LEVEL * Config.TILE_SIZE - random.randint(0, 100)
            width = random.randint(80, 200)
            height = random.randint(30, 60)
            self.clouds.append(Cloud(x, y, width, height))
        
        # 游戏状态
        self.running = True
        self.paused = False
        self.show_debug = True
        self.breaking = False
        self.placing = False
        self.break_timer = 0
        self.place_timer = 0
        self.break_cooldown = 10
        self.place_cooldown = 5
        
        # 背包相关
        self.show_inventory = False
        self.inventory_selected_slot = 0
        self.dragging_item = None
        self.drag_from_slot = None
        
        # 时间系统
        self.time_of_day = 0.5
        self.day_length = Config.DAY_LENGTH
        self.time_counter = 0
        
        # 纹理缓存
        self.texture_cache = {}
        self.load_textures_from_data()
        
        # 存档列表
        self.saves = self.get_saves()
        self.show_save_menu = False
        self.save_name = ""
        self.menu_option = 0
        
        # 网络菜单
        self.show_network_menu = False
        self.network_host = Config.DEFAULT_HOST
        self.network_port = str(Config.DEFAULT_PORT)
        self.network_input = "host"
        self.network_status = ""
        self.chat_messages = []
        self.chat_input = ""
        self.show_chat = False
        
        # 键位设置
        self.key_jump = pygame.K_SPACE
        self.key_jump_alt = pygame.K_w
        self.key_left = pygame.K_a
        self.key_right = pygame.K_d
        
        # 显示选中的物品
        self.selected_item_display = ""
        self.selected_item_timer = 0
        
        # ESC菜单按钮
        self.menu_buttons = []
        self.menu_button_rects = []
        self.create_menu_buttons()
        
        # 启动网络服务
        if online_mode:
            self.start_network(host, port)
    
    def load_textures_from_data(self):
        """从Base64数据加载纹理"""
        print("开始加载内置纹理...")
        
        # 方块纹理映射
        texture_to_block = {
            "grass_block.png": BlockType.GRASS,
            "dirt.png": BlockType.DIRT,
            "stone.png": BlockType.STONE,
            "oak_log.png": BlockType.WOOD,
            "azalea_leaves.png": BlockType.LEAVES,
            "sand.png": BlockType.SAND,
            "cobblestone.png": BlockType.COBBLESTONE,
            "bedrock.png": BlockType.BEDROCK,
            "coal_ore.png": BlockType.COAL_ORE,
            "iron_ore.png": BlockType.IRON_ORE,
            "gold_ore.png": BlockType.GOLD_ORE,
            "diamond_ore.png": BlockType.DIAMOND_ORE,
            "emerald_ore.png": BlockType.EMERALD_ORE,
            "lapis_ore.png": BlockType.LAPIS_ORE,
            "redstone_ore.png": BlockType.REDSTONE_ORE,
            "crafting_table.png": BlockType.CRAFTING_TABLE,
            "apple.png": BlockType.APPLE,
            "bread.png": BlockType.BREAD,
            "cooked_porkchop.png": BlockType.COOKED_PORKCHOP,
            "cooked_beef.png": BlockType.COOKED_BEEF,
            "cooked_chicken.png": BlockType.COOKED_CHICKEN,
            "cooked_fish.png": BlockType.COOKED_FISH,
            "cake.png": BlockType.CAKE,
            "stick.png": BlockType.STICK,
            "wooden_pickaxe.png": BlockType.WOODEN_PICKAXE,
            "stone_pickaxe.png": BlockType.STONE_PICKAXE,
            "iron_pickaxe.png": BlockType.IRON_PICKAXE,
            "gold_pickaxe.png": BlockType.GOLD_PICKAXE,
            "diamond_pickaxe.png": BlockType.DIAMOND_PICKAXE,
        }
        
        for block_type in BlockType:
            if block_type == BlockType.AIR or block_type == BlockType.CLOUD or block_type == BlockType.WATER:
                self.texture_cache[block_type] = None
                continue
            
            texture_file = None
            for filename, bt in texture_to_block.items():
                if bt == block_type:
                    texture_file = filename
                    break
            
            if texture_file and texture_file in TEXTURE_DATA:
                try:
                    img_data = base64.b64decode(TEXTURE_DATA[texture_file])
                    img_io = BytesIO(img_data)
                    texture = pygame.image.load(img_io).convert_alpha()
                    
                    surf = pygame.transform.scale(texture, (Config.TILE_SIZE, Config.TILE_SIZE))
                    
                    
                    self.texture_cache[block_type] = surf
                    print(f"  ✓ 成功加载 {texture_file}")
                    continue
                except Exception as e:
                    print(f"  ✗ 加载内置纹理失败 {texture_file}: {e}")
            
            # 如果纹理加载失败，使用颜色方块
            print(f"  使用颜色方块代替 {block_type.name}")
            props = BLOCK_PROPERTIES[block_type]
            surf = pygame.Surface((Config.TILE_SIZE, Config.TILE_SIZE))
            
            if props["color"]:
                if len(props["color"]) == 4:
                    surf = pygame.Surface((Config.TILE_SIZE, Config.TILE_SIZE), pygame.SRCALPHA)
                    surf.fill(props["color"])
                else:
                    surf.fill(props["color"])
            
            # 添加简单纹理细节
            if block_type == BlockType.GRASS:
                pygame.draw.rect(surf, (0, 100, 0), (0, 0, Config.TILE_SIZE, 4))
            elif block_type == BlockType.STONE:
                for i in range(10):
                    x = random.randint(0, Config.TILE_SIZE-1)
                    y = random.randint(0, Config.TILE_SIZE-1)
                    surf.set_at((x, y), (100, 100, 100))
            elif block_type == BlockType.WOOD:
                pygame.draw.line(surf, (100, 50, 25), (Config.TILE_SIZE//2, 0), (Config.TILE_SIZE//2, Config.TILE_SIZE), 2)
            elif block_type == BlockType.LEAVES:
                for i in range(20):
                    x = random.randint(2, Config.TILE_SIZE-3)
                    y = random.randint(2, Config.TILE_SIZE-3)
                    pygame.draw.circle(surf, (50, 255, 50), (x, y), 2)
            elif block_type in [BlockType.COAL_ORE, BlockType.IRON_ORE, BlockType.GOLD_ORE, BlockType.DIAMOND_ORE, BlockType.EMERALD_ORE, BlockType.LAPIS_ORE, BlockType.REDSTONE_ORE]:
                base_color = (100, 100, 100)
                surf.fill(base_color)
                for i in range(5):
                    x = random.randint(4, Config.TILE_SIZE-5)
                    y = random.randint(4, Config.TILE_SIZE-5)
                    if block_type == BlockType.COAL_ORE:
                        color = (30, 30, 30)
                    elif block_type == BlockType.IRON_ORE:
                        color = (200, 200, 200)
                    elif block_type == BlockType.GOLD_ORE:
                        color = (255, 215, 0)
                    elif block_type == BlockType.DIAMOND_ORE:
                        color = (0, 255, 255)
                    elif block_type == BlockType.EMERALD_ORE:
                        color = (0, 255, 0)
                    elif block_type == BlockType.LAPIS_ORE:
                        color = (0, 0, 255)
                    elif block_type == BlockType.REDSTONE_ORE:
                        color = (255, 0, 0)
                    pygame.draw.circle(surf, color, (x, y), 3)
            
            pygame.draw.rect(surf, (0, 0, 0), surf.get_rect(), 1)
            self.texture_cache[block_type] = surf
        
        print("纹理加载完成")
    
    def create_menu_buttons(self):
        button_width = 200
        button_height = 50
        center_x = Config.SCREEN_WIDTH // 2 - button_width // 2
        
        self.menu_buttons = [
            {"text": "单人游戏", "action": "single"},
            {"text": "联机游戏", "action": "online"},
            {"text": "皮肤管理", "action": "skins"},
            {"text": "存档管理", "action": "saves"},
            {"text": "退出游戏", "action": "quit"}
        ]
        
        self.menu_button_rects = []
        for i, button in enumerate(self.menu_buttons):
            rect = pygame.Rect(center_x, 150 + i * 70, button_width, button_height)
            self.menu_button_rects.append(rect)
    
    def get_available_skins(self):
        skins = []
        if os.path.exists(SKINS_PATH):
            for file in os.listdir(SKINS_PATH):
                if file.endswith(('.png', '.jpg', '.jpeg')):
                    skins.append(file)
        return skins
    
    def get_saves(self):
        saves = []
        if os.path.exists(SAVES_PATH):
            for file in os.listdir(SAVES_PATH):
                if file.endswith('.json'):
                    saves.append(file[:-5])
        return saves
    
    def start_network(self, host=None, port=None):
        pass
    
    def on_network_move(self, message):
        pass
    
    def on_network_block_break(self, message):
        pass
    
    def on_network_block_place(self, message):
        pass
    
    def on_network_chat(self, message):
        pass
    
    def on_network_player_list(self, message):
        pass
    
    def on_network_leave(self, message):
        pass
    
    def on_network_world_data(self, world_data):
        pass
    
    def send_position(self):
        pass
    
    def eat_item(self, block_type):
        if self.player.game_mode == GameMode.SURVIVAL:
            if self.player.inventory.has_item(block_type):
                self.player.inventory.remove_item(block_type)
                food_value = BLOCK_PROPERTIES[block_type]["food"]
                self.player.hunger = min(100, self.player.hunger + food_value)
                self.show_message(f"吃了 {BLOCK_PROPERTIES[block_type]['name']} +{food_value} 饱食度", Config.GREEN)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.show_crafting:
                        self.show_crafting = False
                    elif self.show_crafting_2x2:
                        self.show_crafting_2x2 = False
                        self.clear_crafting_grid_2x2()
                    elif self.show_inventory:
                        self.show_inventory = False
                    elif self.show_skin_menu:
                        self.show_skin_menu = False
                    elif self.show_network_menu:
                        self.show_network_menu = False
                    elif self.show_save_menu:
                        self.show_save_menu = False
                    elif self.show_chat:
                        self.show_chat = False
                    else:
                        self.paused = not self.paused
                
                # 按Tab切换游戏模式
                elif event.key == pygame.K_TAB and not self.paused and not self.show_chat and not self.show_inventory:
                    if self.player.game_mode == GameMode.SURVIVAL:
                        self.player.set_game_mode(GameMode.CREATIVE)
                        self.show_message("切换到创造模式", Config.GREEN)
                    elif self.player.game_mode == GameMode.CREATIVE:
                        self.player.set_game_mode(GameMode.CLASSIC)
                        self.show_message("切换到老版本生存模式", Config.YELLOW)
                    elif self.player.game_mode == GameMode.CLASSIC:
                        self.player.set_game_mode(GameMode.SURVIVAL)
                        self.show_message("切换到生存模式", Config.RED)
                
                # 按E打开背包
                elif event.key == pygame.K_e and not self.paused and not self.show_chat:
                    self.show_inventory = not self.show_inventory
                    if not self.show_inventory:
                        self.dragging_item = None
                        self.drag_from_slot = None
                
                # 按C打开2x2合成
                elif event.key == pygame.K_c and not self.paused and not self.show_chat:
                    self.show_crafting_2x2 = not self.show_crafting_2x2
                    if not self.show_crafting_2x2:
                        self.clear_crafting_grid_2x2()
                
                # 跳跃键
                elif (event.key == self.key_jump or event.key == self.key_jump_alt) and not self.paused and not self.show_chat and not self.show_inventory:
                    self.player.jump()
                
                elif event.key == pygame.K_f:
                    self.show_debug = not self.show_debug
                
                elif event.key == pygame.K_s and self.paused:
                    self.show_save_menu = True
                    self.save_name = f"world_{len(self.saves) + 1}"
                
                elif event.key == pygame.K_l and self.paused:
                    self.show_save_menu = True
                    self.save_name = ""
                
                elif event.key == pygame.K_n and not self.online_mode:
                    self.show_network_menu = True
                    self.network_input = "host"
                
                elif event.key == pygame.K_t and self.online_mode:
                    self.show_chat = True
                    self.chat_input = ""
                
                elif event.key == pygame.K_RETURN:
                    if self.show_skin_menu:
                        self.handle_skin_menu_confirm()
                    elif self.show_network_menu:
                        self.handle_network_menu_confirm()
                    elif self.show_save_menu:
                        self.handle_save_menu_confirm()
                    elif self.show_chat and self.chat_input.strip():
                        if self.online_mode and self.client:
                            self.client.send_chat(self.chat_input)
                        self.show_chat = False
                        self.chat_input = ""
                    elif self.show_crafting_2x2:
                        self.craft_item_2x2()
                
                elif event.key == pygame.K_TAB and self.show_save_menu:
                    self.menu_option = (self.menu_option + 1) % 2
                
                elif event.key == pygame.K_UP and self.show_skin_menu and self.available_skins:
                    self.selected_skin = (self.selected_skin - 1) % len(self.available_skins)
                
                elif event.key == pygame.K_DOWN and self.show_skin_menu and self.available_skins:
                    self.selected_skin = (self.selected_skin + 1) % len(self.available_skins)
                
                elif event.key == pygame.K_BACKSPACE:
                    if self.show_network_menu:
                        if self.network_input == "host":
                            self.network_host = self.network_host[:-1]
                        elif self.network_input == "port":
                            self.network_port = self.network_port[:-1]
                    elif self.show_save_menu:
                        self.save_name = self.save_name[:-1]
                    elif self.show_chat:
                        self.chat_input = self.chat_input[:-1]
                
                elif self.show_network_menu and event.unicode.isprintable():
                    if self.network_input == "host":
                        self.network_host += event.unicode
                    elif self.network_input == "port" and event.unicode.isdigit():
                        self.network_port += event.unicode
                
                elif self.show_save_menu and event.unicode.isprintable():
                    self.save_name += event.unicode
                
                elif self.show_chat and event.unicode.isprintable():
                    self.chat_input += event.unicode
                
                # 数字键选择背包
                elif event.key >= pygame.K_1 and event.key <= pygame.K_9 and not self.paused and not self.show_chat and not self.show_inventory:
                    self.player.inventory.select_hotbar(event.key - pygame.K_1)
                    self.update_selected_item_display()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.paused:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(self.menu_button_rects):
                        if rect.collidepoint(mouse_pos):
                            self.handle_menu_button(i)
                            break
                elif not self.paused and not self.show_chat:
                    if self.show_inventory:
                        self.handle_inventory_click(event.pos, event.button)
                    elif self.show_crafting:
                        self.handle_crafting_click(event.pos, event.button)
                    elif self.show_crafting_2x2:
                        self.handle_crafting_2x2_click(event.pos, event.button)
                    else:
                        if event.button == 1:
                            self.breaking = True
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            world_x = int((mouse_x + self.camera_x) // Config.TILE_SIZE)
                            world_y = int((mouse_y + self.camera_y) // Config.TILE_SIZE)
                            self.player.start_breaking(world_x, world_y)
                        elif event.button == 3:
                            self.placing = True
            
            elif event.type == pygame.MOUSEWHEEL and not self.paused and not self.show_chat:
                if self.show_inventory:
                    self.inventory_selected_slot = (self.inventory_selected_slot + event.y) % 36
                else:
                    self.player.inventory.scroll_hotbar(-event.y)
                    self.update_selected_item_display()
            
            elif event.type == pygame.MOUSEBUTTONUP and not self.paused:
                if not self.show_inventory and not self.show_crafting and not self.show_crafting_2x2:
                    if event.button == 1:
                        self.breaking = False
                        self.player.stop_breaking()
                        self.break_timer = 0
                    elif event.button == 3:
                        self.placing = False
                        self.place_timer = 0
        
        if not self.paused and not self.show_chat and not self.show_inventory and not self.show_crafting and not self.show_crafting_2x2:
            keys = pygame.key.get_pressed()
            self.player.vx = 0
            if keys[self.key_left] or keys[self.key_right]:
                if keys[self.key_left]:
                    self.player.vx = -Config.PLAYER_SPEED
                if keys[self.key_right]:
                    self.player.vx = Config.PLAYER_SPEED
        
        if self.selected_item_timer > 0:
            self.selected_item_timer -= 1
    
    def handle_menu_button(self, button_index):
        if button_index >= len(self.menu_buttons):
            return
        
        action = self.menu_buttons[button_index]["action"]
        
        if action == "single":
            self.paused = False
        elif action == "online":
            self.paused = False
            self.show_network_menu = True
        elif action == "skins":
            self.paused = False
            self.show_skin_menu = True
        elif action == "saves":
            self.paused = False
            self.show_save_menu = True
            self.save_name = f"world_{len(self.saves) + 1}"
        elif action == "quit":
            self.running = False
    
    def handle_inventory_click(self, pos, button):
        slot_width = 40
        slot_height = 40
        start_x = (Config.SCREEN_WIDTH - 9 * slot_width) // 2
        start_y = Config.SCREEN_HEIGHT // 2 - 4 * slot_height
        
        for i in range(36):
            row = i // 9
            col = i % 9
            x = start_x + col * slot_width
            y = start_y + row * slot_height
            rect = pygame.Rect(x, y, slot_width, slot_height)
            
            if rect.collidepoint(pos):
                if button == 1:
                    if self.dragging_item:
                        if self.player.inventory.slots[i]:
                            self.player.inventory.slots[i], self.dragging_item = self.dragging_item, self.player.inventory.slots[i]
                        else:
                            self.player.inventory.slots[i] = self.dragging_item
                            self.dragging_item = None
                            self.drag_from_slot = None
                    else:
                        if self.player.inventory.slots[i]:
                            self.dragging_item = self.player.inventory.slots[i]
                            self.player.inventory.slots[i] = None
                            self.drag_from_slot = i
                elif button == 3:
                    if self.player.inventory.slots[i] and self.player.inventory.slots[i].count > 1:
                        if not self.dragging_item:
                            item = self.player.inventory.slots[i]
                            half = item.count // 2
                            self.dragging_item = Item(item.block_type, half)
                            item.remove(half)
                            self.drag_from_slot = i
                break
    
    def handle_crafting_click(self, pos, button):
        slot_size = 40
        start_x = Config.SCREEN_WIDTH // 2 - 150
        start_y = Config.SCREEN_HEIGHT // 2 - 100
        
        for row in range(3):
            for col in range(3):
                x = start_x + col * slot_size
                y = start_y + row * slot_size
                rect = pygame.Rect(x, y, slot_size, slot_size)
                
                if rect.collidepoint(pos):
                    if button == 1:
                        if self.dragging_item:
                            if not self.crafting_grid[row][col]:
                                self.crafting_grid[row][col] = self.dragging_item.block_type
                                self.dragging_item = None
                        else:
                            if self.crafting_grid[row][col]:
                                block_type = self.crafting_grid[row][col]
                                self.dragging_item = Item(block_type, 1)
                                self.crafting_grid[row][col] = None
                    elif button == 3:
                        self.crafting_grid[row][col] = None
                    
                    self.update_crafting_result()
                    return
        
        result_x = start_x + 4 * slot_size
        result_y = start_y + slot_size
        result_rect = pygame.Rect(result_x, result_y, slot_size, slot_size)
        
        if result_rect.collidepoint(pos) and self.crafting_result and button == 1:
            result_type, count = self.crafting_result
            if self.player.add_block(result_type, count):
                self.clear_crafting_grid()
                self.crafting_result = None
                self.show_message(f"合成 {BLOCK_PROPERTIES[result_type]['name']} x{count}", Config.GREEN)
    
    def handle_crafting_2x2_click(self, pos, button):
        slot_size = 40
        start_x = Config.SCREEN_WIDTH // 2 - 100
        start_y = Config.SCREEN_HEIGHT // 2 - 100
        
        for row in range(2):
            for col in range(2):
                x = start_x + col * slot_size
                y = start_y + row * slot_size
                rect = pygame.Rect(x, y, slot_size, slot_size)
                
                if rect.collidepoint(pos):
                    if button == 1:
                        if self.dragging_item:
                            if not self.crafting_grid_2x2[row][col]:
                                self.crafting_grid_2x2[row][col] = self.dragging_item.block_type
                                self.dragging_item = None
                        else:
                            if self.crafting_grid_2x2[row][col]:
                                block_type = self.crafting_grid_2x2[row][col]
                                self.dragging_item = Item(block_type, 1)
                                self.crafting_grid_2x2[row][col] = None
                    elif button == 3:
                        self.crafting_grid_2x2[row][col] = None
                    
                    self.update_crafting_result_2x2()
                    return
        
        result_x = start_x + 3 * slot_size
        result_y = start_y + slot_size
        result_rect = pygame.Rect(result_x, result_y, slot_size, slot_size)
        
        if result_rect.collidepoint(pos) and self.crafting_result_2x2 and button == 1:
            result_type, count = self.crafting_result_2x2
            if self.player.add_block(result_type, count):
                self.clear_crafting_grid_2x2()
                self.crafting_result_2x2 = None
                self.show_message(f"合成 {BLOCK_PROPERTIES[result_type]['name']} x{count}", Config.GREEN)
    
    def update_crafting_result(self):
        self.crafting_result = self.crafting_manager.craft(self.crafting_grid, self.player.inventory)
    
    def update_crafting_result_2x2(self):
        grid_3x3 = [[None for _ in range(3)] for _ in range(3)]
        for i in range(2):
            for j in range(2):
                grid_3x3[i][j] = self.crafting_grid_2x2[i][j]
        self.crafting_result_2x2 = self.crafting_manager.craft(grid_3x3, self.player.inventory)
    
    def clear_crafting_grid(self):
        for row in range(3):
            for col in range(3):
                if self.crafting_grid[row][col]:
                    self.player.add_block(self.crafting_grid[row][col])
                    self.crafting_grid[row][col] = None
        self.crafting_result = None
    
    def clear_crafting_grid_2x2(self):
        for row in range(2):
            for col in range(2):
                if self.crafting_grid_2x2[row][col]:
                    self.player.add_block(self.crafting_grid_2x2[row][col])
                    self.crafting_grid_2x2[row][col] = None
        self.crafting_result_2x2 = None
    
    def craft_item(self):
        if self.crafting_result:
            result_type, count = self.crafting_result
            if self.player.add_block(result_type, count):
                self.clear_crafting_grid()
                self.crafting_result = None
                self.show_message(f"合成 {BLOCK_PROPERTIES[result_type]['name']} x{count}", Config.GREEN)
    
    def craft_item_2x2(self):
        if self.crafting_result_2x2:
            result_type, count = self.crafting_result_2x2
            if self.player.add_block(result_type, count):
                self.clear_crafting_grid_2x2()
                self.crafting_result_2x2 = None
                self.show_message(f"合成 {BLOCK_PROPERTIES[result_type]['name']} x{count}", Config.GREEN)
    
    def update_selected_item_display(self):
        selected_block = self.player.get_selected_block()
        if selected_block != BlockType.AIR:
            block_name = BLOCK_PROPERTIES[selected_block]["name"]
            self.selected_item_display = f"选中: {block_name}"
        else:
            self.selected_item_display = "选中: 空"
        self.selected_item_timer = 120
    
    def show_message(self, text, color):
        self.selected_item_display = text
        self.selected_item_timer = 120
        self.message_color = color
    
    def handle_skin_menu_confirm(self):
        if self.available_skins:
            skin_file = os.path.join(SKINS_PATH, self.available_skins[self.selected_skin])
            self.player.set_skin(skin_file)
            self.show_skin_menu = False
    
    def handle_network_menu_confirm(self):
        try:
            port = int(self.network_port)
            if self.network_input == "host":
                self.show_network_menu = False
                self.is_server = True
                self.online_mode = True
                self.start_network(self.network_host, port)
            else:
                self.is_server = False
                self.online_mode = True
                self.start_network(self.network_host, port)
        except ValueError:
            self.network_status = "端口格式错误"
    
    def handle_save_menu_confirm(self):
        if self.save_name:
            if self.menu_option == 0:
                filename = self.save_name + '.json'
                self.world.save(filename)
                self.saves = self.get_saves()
                self.show_save_menu = False
            elif self.menu_option == 1 and self.saves:
                filename = self.saves[0] + '.json'
                self.world.load(filename)
                self.player.respawn(self.world)
                self.show_save_menu = False
    
    def update_camera(self):
        self.camera_x = self.player.x - Config.SCREEN_WIDTH // 2
        self.camera_y = self.player.y - Config.SCREEN_HEIGHT // 2
        self.camera_y = max(0, min(self.camera_y, 
                                  Config.WORLD_HEIGHT * Config.TILE_SIZE - Config.SCREEN_HEIGHT))
    
    def handle_block_interaction(self):
        if self.show_inventory or self.show_chat or self.paused or self.show_crafting or self.show_crafting_2x2:
            return
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        world_x = int((mouse_x + self.camera_x) // Config.TILE_SIZE)
        world_y = int((mouse_y + self.camera_y) // Config.TILE_SIZE)
        
        player_tile_x = int(self.player.x // Config.TILE_SIZE)
        player_tile_y = int(self.player.y // Config.TILE_SIZE)
        distance = abs(world_x - player_tile_x) + abs(world_y - player_tile_y)
        
        if distance > 6:
            return
        
        if self.breaking:
            block = self.world.get_block(world_x, world_y)
            if block != BlockType.AIR and BLOCK_PROPERTIES[block]["breakable"]:
                should_break = self.player.update_breaking(self.world)
                if should_break:
                    self.world.set_block(world_x, world_y, BlockType.AIR)
                    
                    if self.player.game_mode != GameMode.CREATIVE:
                        drop = BLOCK_PROPERTIES[block]["drop"]
                        if drop:
                            self.player.add_block(drop)
                        
                        if block == BlockType.LEAVES and random.random() < 0.25:
                            self.player.add_block(BlockType.APPLE)
                            self.show_message("获得苹果", Config.GREEN)
                    
                    if self.online_mode and self.client:
                        self.client.send_block_break(world_x, world_y)
                    
                    self.player.stop_breaking()
        
        elif self.placing and self.place_timer <= 0:
            if self.world.get_block(world_x, world_y) == BlockType.AIR:
                selected = self.player.get_selected_block()
                if selected != BlockType.AIR:
                    can_place = BLOCK_PROPERTIES[selected].get("placeable", True)
                    
                    if can_place:
                        if self.player.game_mode == GameMode.CREATIVE or self.player.remove_block(selected):
                            self.world.set_block(world_x, world_y, selected)
                            
                            if self.online_mode and self.client:
                                self.client.send_block_place(world_x, world_y, selected)
                            
                            self.place_timer = self.place_cooldown
                    else:
                        if "food" in BLOCK_PROPERTIES[selected]:
                            self.eat_item(selected)
        
        if self.place_timer > 0:
            self.place_timer -= 1
    
    def update_time(self):
        self.time_counter += 1
        if self.time_counter >= self.day_length:
            self.time_counter = 0
        self.time_of_day = 0.5 + 0.5 * math.sin(self.time_counter / self.day_length * 2 * math.pi)
    
    def get_sky_color(self):
        if self.time_of_day > 0.8:
            factor = (self.time_of_day - 0.8) * 5
            return (
                int(135 * (1 - factor) + 10 * factor),
                int(206 * (1 - factor) + 10 * factor),
                int(235 * (1 - factor) + 30 * factor)
            )
        elif self.time_of_day < 0.2:
            factor = self.time_of_day * 5
            return (
                int(10 * (1 - factor) + 135 * factor),
                int(10 * (1 - factor) + 206 * factor),
                int(30 * (1 - factor) + 235 * factor)
            )
        else:
            return Config.SKY_BLUE
    
    def draw(self):
        sky_color = self.get_sky_color()
        self.screen.fill(sky_color)
        
        if Config.SHOW_CLOUDS:
            for cloud in self.clouds:
                cloud.update()
                cloud.draw(self.screen, self.camera_x)
        
        start_x = int(self.camera_x // Config.TILE_SIZE)
        end_x = int((self.camera_x + Config.SCREEN_WIDTH) // Config.TILE_SIZE) + 1
        start_y = max(0, int(self.camera_y // Config.TILE_SIZE))
        end_y = min(Config.WORLD_HEIGHT, int((self.camera_y + Config.SCREEN_HEIGHT) // Config.TILE_SIZE) + 1)
        
        blocks_drawn = 0
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                block = self.world.get_block(x, y)
                if block != BlockType.AIR:
                    texture = self.texture_cache.get(block)
                    if texture:
                        screen_x = x * Config.TILE_SIZE - self.camera_x
                        screen_y = y * Config.TILE_SIZE - self.camera_y
                        
                        # 应用暗色滤镜（基于深度）
                        if y > Config.CLOUD_LEVEL and Config.AMBIENT_OCCLUSION:
                            # 计算深度因子
                            depth = y - Config.CLOUD_LEVEL
                            max_depth = Config.WORLD_HEIGHT - Config.CLOUD_LEVEL
                            depth_factor = min(1.0, depth / max_depth)
                            
                            # 获取滤镜颜色
                            filter_idx = int(depth_factor * (self.dark_filter.filter_height - 1))
                            filter_idx = min(filter_idx, self.dark_filter.filter_height - 1)
                            
                            if filter_idx < len(self.dark_filter.color_gradient):
                                filter_color = self.dark_filter.color_gradient[filter_idx]
                                # 应用滤镜到纹理
                                dark_surf = texture.copy()
                                dark_surf.fill((filter_color[0], filter_color[1], filter_color[2]), 
                                             special_flags=pygame.BLEND_RGB_MULT)
                                # 应用透明度
                                if filter_color[3] < 255:
                                    dark_surf.set_alpha(filter_color[3])
                                self.screen.blit(dark_surf, (screen_x, screen_y))
                            else:
                                self.screen.blit(texture, (screen_x, screen_y))
                        else:
                            self.screen.blit(texture, (screen_x, screen_y))
                        blocks_drawn += 1
        
        for player in self.network_players.values():
            player.draw(self.screen, self.camera_x, self.camera_y)
        
        self.player.draw(self.screen, self.camera_x, self.camera_y, is_local=True)
        
        # 绘制破坏进度条
        if self.player.breaking_block:
            x, y = self.player.breaking_block
            screen_x = x * Config.TILE_SIZE - self.camera_x
            screen_y = y * Config.TILE_SIZE - self.camera_y
            
            progress = self.player.block_break_progress
            hardness = BLOCK_PROPERTIES[self.world.get_block(x, y)]["hardness"]
            max_progress = hardness * 20
            
            if max_progress > 0:
                bar_width = Config.TILE_SIZE
                bar_height = 4
                bar_x = screen_x
                bar_y = screen_y - bar_height - 2
                
                pygame.draw.rect(self.screen, Config.BLACK, (bar_x, bar_y, bar_width, bar_height))
                pygame.draw.rect(self.screen, Config.RED, (bar_x, bar_y, int(bar_width * progress / max_progress), bar_height))
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.line(self.screen, Config.WHITE, (mouse_x - 10, mouse_y), (mouse_x + 10, mouse_y), 2)
        pygame.draw.line(self.screen, Config.WHITE, (mouse_x, mouse_y - 10), (mouse_x, mouse_y + 10), 2)
        
        if not self.paused and not self.show_chat and not self.show_inventory and not self.show_crafting and not self.show_crafting_2x2:
            tile_x = int((mouse_x + self.camera_x) // Config.TILE_SIZE)
            tile_y = int((mouse_y + self.camera_y) // Config.TILE_SIZE)
            if 0 <= tile_y < Config.WORLD_HEIGHT:
                highlight_rect = pygame.Rect(
                    tile_x * Config.TILE_SIZE - self.camera_x,
                    tile_y * Config.TILE_SIZE - self.camera_y,
                    Config.TILE_SIZE,
                    Config.TILE_SIZE
                )
                pygame.draw.rect(self.screen, Config.WHITE, highlight_rect, 3)
        
        self.draw_hud()
        
        if self.show_debug:
            self.draw_debug(blocks_drawn)
        
        if self.online_mode and self.network_status:
            status_text = self.chinese_font.render(self.network_status, True, Config.GREEN, 'small')
            self.screen.blit(status_text, (10, 100))
        
        if self.chat_messages:
            y = Config.SCREEN_HEIGHT - 150
            for msg in self.chat_messages[-5:]:
                msg_text = self.chinese_font.render(msg, True, Config.WHITE, 'small')
                bg_rect = pygame.Rect(10, y - 2, msg_text.get_width() + 4, msg_text.get_height() + 4)
                pygame.draw.rect(self.screen, (0, 0, 0, 128), bg_rect)
                self.screen.blit(msg_text, (12, y))
                y += 22
        
        if self.show_chat:
            chat_bg = pygame.Rect(10, Config.SCREEN_HEIGHT - 50, Config.SCREEN_WIDTH - 20, 40)
            pygame.draw.rect(self.screen, (0, 0, 0, 200), chat_bg)
            pygame.draw.rect(self.screen, Config.WHITE, chat_bg, 2)
            
            chat_text = self.chinese_font.render("> " + self.chat_input + "_", True, Config.WHITE)
            self.screen.blit(chat_text, (20, Config.SCREEN_HEIGHT - 42))
        
        if self.selected_item_timer > 0 and self.selected_item_display:
            color = getattr(self, 'message_color', Config.YELLOW)
            item_text = self.chinese_font.render(self.selected_item_display, True, color, 'small')
            text_rect = item_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT - 100))
            bg_rect = text_rect.inflate(10, 5)
            pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect)
            pygame.draw.rect(self.screen, color, bg_rect, 2)
            self.screen.blit(item_text, text_rect)
        
        if self.show_inventory:
            self.draw_inventory()
        
        if self.show_crafting:
            self.draw_crafting()
        
        if self.show_crafting_2x2:
            self.draw_crafting_2x2()
        
        if self.paused:
            self.draw_pause_menu()
        elif self.show_save_menu:
            self.draw_save_menu()
        elif self.show_network_menu:
            self.draw_network_menu()
        elif self.show_skin_menu:
            self.draw_skin_menu()
        
        pygame.display.flip()
    
    def draw_hud(self):
        bar_width = 9 * (Config.TILE_SIZE + 4) + 4
        bar_x = (Config.SCREEN_WIDTH - bar_width) // 2
        bar_y = Config.SCREEN_HEIGHT - Config.TILE_SIZE - 20
        
        s = pygame.Surface((bar_width + 4, Config.TILE_SIZE + 24))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self.screen.blit(s, (bar_x - 2, bar_y - 2))
        
        hotbar_items = self.player.inventory.get_hotbar_items()
        
        for i in range(9):
            slot_x = bar_x + i * (Config.TILE_SIZE + 4)
            slot_rect = pygame.Rect(slot_x, bar_y, Config.TILE_SIZE, Config.TILE_SIZE)
            
            color = Config.WHITE if i == self.player.inventory.selected_hotbar else Config.GRAY
            pygame.draw.rect(self.screen, color, slot_rect, 2)
            
            if hotbar_items[i]:
                block = hotbar_items[i].block_type
                texture = self.texture_cache.get(block)
                if texture:
                    self.screen.blit(texture, (slot_x, bar_y))
                
                count = hotbar_items[i].count
                if count > 1:
                    text = self.chinese_font.render(str(count), True, Config.WHITE, 'small')
                    self.screen.blit(text, (slot_x + 2, bar_y + 2))
            
            text = self.chinese_font.render(str(i + 1), True, Config.WHITE, 'small')
            self.screen.blit(text, (slot_x + 2, bar_y + Config.TILE_SIZE - 20))
        
        # 游戏模式显示
        mode_text = ""
        mode_color = Config.WHITE
        if self.player.game_mode == GameMode.SURVIVAL:
            mode_text = "生存模式"
            mode_color = Config.RED
        elif self.player.game_mode == GameMode.CREATIVE:
            mode_text = "创造模式"
            mode_color = Config.GREEN
        elif self.player.game_mode == GameMode.CLASSIC:
            mode_text = "老版本生存"
            mode_color = Config.YELLOW
        
        mode_display = self.chinese_font.render(mode_text, True, mode_color, 'small')
        self.screen.blit(mode_display, (10, 60))
        
        # 生命值和饥饿值
        if self.player.game_mode != GameMode.CREATIVE:
            health_text = self.chinese_font.render(f"❤ {self.player.health}", True, Config.RED, 'small')
            self.screen.blit(health_text, (10, 10))
            
            hunger_text = self.chinese_font.render(f"🍗 {self.player.hunger}", True, Config.ORANGE, 'small')
            self.screen.blit(hunger_text, (10, 35))
        
        coord_text = self.chinese_font.render(
            f"X: {int(self.player.x//Config.TILE_SIZE)} Y: {int(self.player.y//Config.TILE_SIZE)}", 
            True, Config.WHITE, 'small')
        self.screen.blit(coord_text, (Config.SCREEN_WIDTH - 150, 10))
        
        if self.online_mode:
            online_text = self.chinese_font.render(f"在线: {len(self.network_players) + 1}", True, Config.GREEN, 'small')
            self.screen.blit(online_text, (Config.SCREEN_WIDTH - 150, 35))
        
        hint_text = self.chinese_font.render("按 E 打开背包  C 合成", True, Config.GRAY, 'small')
        self.screen.blit(hint_text, (Config.SCREEN_WIDTH - 200, Config.SCREEN_HEIGHT - 30))
    
    def draw_inventory(self):
        s = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        s.set_alpha(180)
        s.fill((30, 30, 30))
        self.screen.blit(s, (0, 0))
        
        title = self.chinese_font.render("背包", True, Config.WHITE, 'big')
        title_rect = title.get_rect(center=(Config.SCREEN_WIDTH//2, 80))
        self.screen.blit(title, title_rect)
        
        slot_width = 40
        slot_height = 40
        start_x = (Config.SCREEN_WIDTH - 9 * slot_width) // 2
        start_y = Config.SCREEN_HEIGHT // 2 - 4 * slot_height
        
        for i in range(36):
            row = i // 9
            col = i % 9
            x = start_x + col * slot_width
            y = start_y + row * slot_height
            
            slot_rect = pygame.Rect(x, y, slot_width, slot_height)
            pygame.draw.rect(self.screen, Config.DARK_GRAY, slot_rect)
            pygame.draw.rect(self.screen, Config.GRAY, slot_rect, 2)
            
            if i < len(self.player.inventory.slots) and self.player.inventory.slots[i]:
                item = self.player.inventory.slots[i]
                texture = self.texture_cache.get(item.block_type)
                if texture:
                    item_surf = pygame.transform.scale(texture, (slot_width - 4, slot_height - 4))
                    self.screen.blit(item_surf, (x + 2, y + 2))
                
                if item.count > 1:
                    count_text = self.chinese_font.render(str(item.count), True, Config.WHITE, 'small')
                    self.screen.blit(count_text, (x + 2, y + 2))
        
        if self.dragging_item:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            texture = self.texture_cache.get(self.dragging_item.block_type)
            if texture:
                item_surf = pygame.transform.scale(texture, (slot_width, slot_height))
                self.screen.blit(item_surf, (mouse_x - slot_width//2, mouse_y - slot_height//2))
                
                if self.dragging_item.count > 1:
                    count_text = self.chinese_font.render(str(self.dragging_item.count), True, Config.WHITE, 'small')
                    self.screen.blit(count_text, (mouse_x - slot_width//2 + 2, mouse_y - slot_height//2 + 2))
        
        hint = self.chinese_font.render("左键拿起/放置  右键分半   ESC关闭", True, Config.GRAY, 'small')
        hint_rect = hint.get_rect(center=(Config.SCREEN_WIDTH//2, Config.SCREEN_HEIGHT - 50))
        self.screen.blit(hint, hint_rect)
    
    def draw_crafting(self):
        s = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        s.set_alpha(200)
        s.fill((30, 30, 30))
        self.screen.blit(s, (0, 0))
        
        title = self.chinese_font.render("3x3 合成", True, Config.WHITE, 'big')
        title_rect = title.get_rect(center=(Config.SCREEN_WIDTH//2, 80))
        self.screen.blit(title, title_rect)
        
        slot_size = 40
        start_x = Config.SCREEN_WIDTH // 2 - 150
        start_y = Config.SCREEN_HEIGHT // 2 - 100
        
        for row in range(3):
            for col in range(3):
                x = start_x + col * slot_size
                y = start_y + row * slot_size
                rect = pygame.Rect(x, y, slot_size, slot_size)
                
                pygame.draw.rect(self.screen, Config.DARK_GRAY, rect)
                pygame.draw.rect(self.screen, Config.GRAY, rect, 2)
                
                if self.crafting_grid[row][col]:
                    texture = self.texture_cache.get(self.crafting_grid[row][col])
                    if texture:
                        item_surf = pygame.transform.scale(texture, (slot_size - 4, slot_size - 4))
                        self.screen.blit(item_surf, (x + 2, y + 2))
        
        arrow_x = start_x + 3 * slot_size + 10
        arrow_y = start_y + slot_size
        pygame.draw.polygon(self.screen, Config.WHITE, [
            (arrow_x, arrow_y + 10),
            (arrow_x + 30, arrow_y),
            (arrow_x + 30, arrow_y + 20)
        ])
        
        result_x = start_x + 4 * slot_size
        result_y = start_y + slot_size
        result_rect = pygame.Rect(result_x, result_y, slot_size, slot_size)
        
        pygame.draw.rect(self.screen, Config.DARK_GRAY, result_rect)
        pygame.draw.rect(self.screen, Config.YELLOW if self.crafting_result else Config.GRAY, result_rect, 3)
        
        if self.crafting_result:
            result_type, count = self.crafting_result
            texture = self.texture_cache.get(result_type)
            if texture:
                item_surf = pygame.transform.scale(texture, (slot_size - 4, slot_size - 4))
                self.screen.blit(item_surf, (result_x + 2, result_y + 2))
            
            if count > 1:
                count_text = self.chinese_font.render(str(count), True, Config.WHITE, 'small')
                self.screen.blit(count_text, (result_x + 2, result_y + 2))
        
        if self.dragging_item:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            texture = self.texture_cache.get(self.dragging_item.block_type)
            if texture:
                item_surf = pygame.transform.scale(texture, (slot_size, slot_size))
                self.screen.blit(item_surf, (mouse_x - slot_size//2, mouse_y - slot_size//2))
        
        hint = self.chinese_font.render("左键放置/拿起  右键清除  回车合成  ESC关闭", True, Config.GRAY, 'small')
        hint_rect = hint.get_rect(center=(Config.SCREEN_WIDTH//2, Config.SCREEN_HEIGHT - 50))
        self.screen.blit(hint, hint_rect)
    
    def draw_crafting_2x2(self):
        s = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        s.set_alpha(200)
        s.fill((30, 30, 30))
        self.screen.blit(s, (0, 0))
        
        title = self.chinese_font.render("2x2 合成", True, Config.WHITE, 'big')
        title_rect = title.get_rect(center=(Config.SCREEN_WIDTH//2, 80))
        self.screen.blit(title, title_rect)
        
        slot_size = 40
        start_x = Config.SCREEN_WIDTH // 2 - 100
        start_y = Config.SCREEN_HEIGHT // 2 - 100
        
        for row in range(2):
            for col in range(2):
                x = start_x + col * slot_size
                y = start_y + row * slot_size
                rect = pygame.Rect(x, y, slot_size, slot_size)
                
                pygame.draw.rect(self.screen, Config.DARK_GRAY, rect)
                pygame.draw.rect(self.screen, Config.GRAY, rect, 2)
                
                if self.crafting_grid_2x2[row][col]:
                    texture = self.texture_cache.get(self.crafting_grid_2x2[row][col])
                    if texture:
                        item_surf = pygame.transform.scale(texture, (slot_size - 4, slot_size - 4))
                        self.screen.blit(item_surf, (x + 2, y + 2))
        
        arrow_x = start_x + 2 * slot_size + 10
        arrow_y = start_y + slot_size
        pygame.draw.polygon(self.screen, Config.WHITE, [
            (arrow_x, arrow_y + 10),
            (arrow_x + 30, arrow_y),
            (arrow_x + 30, arrow_y + 20)
        ])
        
        result_x = start_x + 3 * slot_size
        result_y = start_y + slot_size
        result_rect = pygame.Rect(result_x, result_y, slot_size, slot_size)
        
        pygame.draw.rect(self.screen, Config.DARK_GRAY, result_rect)
        pygame.draw.rect(self.screen, Config.YELLOW if self.crafting_result_2x2 else Config.GRAY, result_rect, 3)
        
        if self.crafting_result_2x2:
            result_type, count = self.crafting_result_2x2
            texture = self.texture_cache.get(result_type)
            if texture:
                item_surf = pygame.transform.scale(texture, (slot_size - 4, slot_size - 4))
                self.screen.blit(item_surf, (result_x + 2, result_y + 2))
            
            if count > 1:
                count_text = self.chinese_font.render(str(count), True, Config.WHITE, 'small')
                self.screen.blit(count_text, (result_x + 2, result_y + 2))
        
        if self.dragging_item:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            texture = self.texture_cache.get(self.dragging_item.block_type)
            if texture:
                item_surf = pygame.transform.scale(texture, (slot_size, slot_size))
                self.screen.blit(item_surf, (mouse_x - slot_size//2, mouse_y - slot_size//2))
        
        hint = self.chinese_font.render("左键放置/拿起  右键清除  回车合成  ESC关闭", True, Config.GRAY, 'small')
        hint_rect = hint.get_rect(center=(Config.SCREEN_WIDTH//2, Config.SCREEN_HEIGHT - 50))
        self.screen.blit(hint, hint_rect)
    
    def draw_debug(self, blocks_drawn):
        debug_info = [
            f"FPS: {int(self.clock.get_fps())}",
            f"位置: ({int(self.player.x)}, {int(self.player.y)})",
            f"速度: ({self.player.vx:.1f}, {self.player.vy:.1f})",
            f"地面: {self.player.on_ground}",
            f"时间: {self.time_of_day:.2f}",
            f"区块: {len(self.world.chunks)}",
            f"方块: {blocks_drawn}",
            f"模式: {self.player.game_mode.name}",
        ]
        
        if self.online_mode:
            debug_info.append(f"网络玩家: {len(self.network_players)}")
        
        y = 70
        for info in debug_info:
            text = self.chinese_font.render(info, True, Config.WHITE, 'small')
            pygame.draw.rect(self.screen, (0, 0, 0, 128), 
                           (8, y - 2, text.get_width() + 4, text.get_height() + 4))
            self.screen.blit(text, (10, y))
            y += 22
    
    def draw_pause_menu(self):
        s = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        s.set_alpha(180)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))
        
        title = self.chinese_font.render("游戏菜单", True, Config.WHITE, 'big')
        title_rect = title.get_rect(center=(Config.SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        for i, (button, rect) in enumerate(zip(self.menu_buttons, self.menu_button_rects)):
            hover = rect.collidepoint(mouse_pos)
            
            if hover:
                color = Config.GREEN
                border_color = Config.YELLOW
            else:
                color = Config.DARK_GRAY
                border_color = Config.GRAY
            
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, border_color, rect, 3)
            
            text = self.chinese_font.render(button["text"], True, Config.WHITE)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
        
        hint = self.chinese_font.render("点击按钮或按ESC返回游戏", True, Config.GRAY, 'small')
        hint_rect = hint.get_rect(center=(Config.SCREEN_WIDTH//2, Config.SCREEN_HEIGHT - 50))
        self.screen.blit(hint, hint_rect)
    
    def draw_save_menu(self):
        s = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))
        
        title = self.chinese_font.render("存档/读档", True, Config.WHITE, 'big')
        title_rect = title.get_rect(center=(Config.SCREEN_WIDTH//2, 150))
        self.screen.blit(title, title_rect)
        
        options = ["保存游戏", "加载游戏"]
        for i, option in enumerate(options):
            color = Config.GREEN if i == self.menu_option else Config.WHITE
            text = self.chinese_font.render(option, True, color)
            text_rect = text.get_rect(center=(Config.SCREEN_WIDTH//2, 250 + i * 50))
            self.screen.blit(text, text_rect)
        
        if self.menu_option == 0:
            prompt = self.chinese_font.render("存档名称:", True, Config.WHITE)
            self.screen.blit(prompt, (Config.SCREEN_WIDTH//2 - 200, 350))
            
            input_text = self.chinese_font.render(self.save_name or "_", True, Config.WHITE)
            pygame.draw.rect(self.screen, Config.WHITE, 
                           (Config.SCREEN_WIDTH//2 - 200, 380, 400, 40), 2)
            self.screen.blit(input_text, (Config.SCREEN_WIDTH//2 - 190, 385))
        
        elif self.menu_option == 1:
            if self.saves:
                text = self.chinese_font.render("按回车加载最新存档", True, Config.WHITE)
                text_rect = text.get_rect(center=(Config.SCREEN_WIDTH//2, 350))
                self.screen.blit(text, text_rect)
                
                y = 400
                for save in self.saves[:5]:
                    save_text = self.chinese_font.render(f"• {save}", True, Config.GRAY, 'small')
                    self.screen.blit(save_text, (Config.SCREEN_WIDTH//2 - 100, y))
                    y += 25
            else:
                text = self.chinese_font.render("没有存档", True, Config.RED)
                text_rect = text.get_rect(center=(Config.SCREEN_WIDTH//2, 350))
                self.screen.blit(text, text_rect)
        
        hint = self.chinese_font.render("TAB切换选项  ENTER确认  ESC返回", True, Config.GRAY, 'small')
        hint_rect = hint.get_rect(center=(Config.SCREEN_WIDTH//2, 550))
        self.screen.blit(hint, hint_rect)
    
    def draw_network_menu(self):
        s = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))
        
        title = self.chinese_font.render("联机设置", True, Config.WHITE, 'big')
        title_rect = title.get_rect(center=(Config.SCREEN_WIDTH//2, 150))
        self.screen.blit(title, title_rect)
        
        host_label = self.chinese_font.render("服务器地址:", True, Config.WHITE)
        self.screen.blit(host_label, (Config.SCREEN_WIDTH//2 - 200, 250))
        
        host_bg = pygame.Rect(Config.SCREEN_WIDTH//2 - 200, 290, 400, 40)
        pygame.draw.rect(self.screen, Config.DARK_GRAY, host_bg)
        pygame.draw.rect(self.screen, Config.WHITE if self.network_input == "host" else Config.GRAY, host_bg, 2)
        
        host_text = self.chinese_font.render(self.network_host or "localhost", True, Config.WHITE)
        self.screen.blit(host_text, (Config.SCREEN_WIDTH//2 - 190, 295))
        
        port_label = self.chinese_font.render("端口:", True, Config.WHITE)
        self.screen.blit(port_label, (Config.SCREEN_WIDTH//2 - 200, 350))
        
        port_bg = pygame.Rect(Config.SCREEN_WIDTH//2 - 200, 390, 400, 40)
        pygame.draw.rect(self.screen, Config.DARK_GRAY, port_bg)
        pygame.draw.rect(self.screen, Config.WHITE if self.network_input == "port" else Config.GRAY, port_bg, 2)
        
        port_text = self.chinese_font.render(self.network_port or "5555", True, Config.WHITE)
        self.screen.blit(port_text, (Config.SCREEN_WIDTH//2 - 190, 395))
        
        if self.network_status:
            status_color = Config.GREEN if "成功" in self.network_status or "连接" in self.network_status else Config.RED
            status_text = self.chinese_font.render(self.network_status, True, status_color, 'small')
            status_rect = status_text.get_rect(center=(Config.SCREEN_WIDTH//2, 480))
            self.screen.blit(status_text, status_rect)
        
        hint = self.chinese_font.render("TAB切换输入框  ENTER确认  ESC返回", True, Config.GRAY, 'small')
        hint_rect = hint.get_rect(center=(Config.SCREEN_WIDTH//2, 550))
        self.screen.blit(hint, hint_rect)
    
    def draw_skin_menu(self):
        s = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))
        
        title = self.chinese_font.render("选择皮肤", True, Config.WHITE, 'big')
        title_rect = title.get_rect(center=(Config.SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        if not self.available_skins:
            text = self.chinese_font.render("没有找到皮肤文件", True, Config.RED)
            text_rect = text.get_rect(center=(Config.SCREEN_WIDTH//2, 250))
            self.screen.blit(text, text_rect)
            
            hint = self.chinese_font.render("请将PNG图片放到 skins/ 目录下", True, Config.GRAY, 'small')
            hint_rect = hint.get_rect(center=(Config.SCREEN_WIDTH//2, 300))
            self.screen.blit(hint, hint_rect)
        else:
            preview_x = Config.SCREEN_WIDTH // 2 - 200
            preview_y = 180
            
            for i, skin_file in enumerate(self.available_skins[:6]):
                color = Config.GREEN if i == self.selected_skin else Config.WHITE
                
                col = i % 2
                row = i // 2
                x = preview_x + col * 200
                y = preview_y + row * 120
                
                skin_path = os.path.join(SKINS_PATH, skin_file)
                try:
                    preview = pygame.image.load(skin_path)
                    preview = pygame.transform.scale(preview, (50, 90))
                    
                    border_rect = pygame.Rect(x - 5, y - 5, 60, 100)
                    pygame.draw.rect(self.screen, color, border_rect, 2)
                    
                    self.screen.blit(preview, (x, y))
                    
                    name_text = self.chinese_font.render(skin_file[:10], True, color, 'small')
                    self.screen.blit(name_text, (x, y + 95))
                    
                except Exception as e:
                    pass
            
            if len(self.available_skins) > 6:
                more_text = self.chinese_font.render(f"... 还有 {len(self.available_skins)-6} 个皮肤", True, Config.GRAY, 'small')
                more_rect = more_text.get_rect(center=(Config.SCREEN_WIDTH//2, preview_y + 240))
                self.screen.blit(more_text, more_rect)
        
        hint = self.chinese_font.render("上下箭头选择  ENTER确认  ESC返回", True, Config.GRAY, 'small')
        hint_rect = hint.get_rect(center=(Config.SCREEN_WIDTH//2, 550))
        self.screen.blit(hint, hint_rect)
    
    def run(self):
        while self.running:
            self.handle_events()
            
            if not self.paused and not self.show_chat and not self.show_inventory and not self.show_crafting and not self.show_crafting_2x2:
                self.player.update(self.world)
                self.update_camera()
                self.handle_block_interaction()
                self.update_time()
                
                if self.online_mode and self.client:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_position_send > self.position_send_interval:
                        self.send_position()
                        self.last_position_send = current_time
                    
                    messages = self.client.get_messages()
            
            self.draw()
            self.clock.tick(60)
        
        if self.server:
            self.server.stop()
        if self.client:
            self.client.disconnect()
        
        pygame.quit()


# ==================== 主函数 ====================

def main():
    parser = argparse.ArgumentParser(description='2D Minecraft - 完整版')
    parser.add_argument('--online', action='store_true', help='启用联机模式')
    parser.add_argument('--server', action='store_true', help='作为服务器运行')
    parser.add_argument('--host', default=Config.DEFAULT_HOST, help='服务器地址')
    parser.add_argument('--port', type=int, default=Config.DEFAULT_PORT, help='服务器端口')
    
    args = parser.parse_args()
    
    game = Game(
        online_mode=args.online,
        is_server=args.server,
        host=args.host,
        port=args.port
    )
    game.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"游戏出错: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")
