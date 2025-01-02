import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """管理飞船所发射子弹的类"""
    def __init__(self,ai_game):
        """在飞船当前位置创建一个子弹对象"""
        super().__init__()
        self.screen = ai_game.screen #子弹实例提供一个引用到主游戏窗口（屏幕）的接口。
        self.settings = ai_game.settings #创建接口
        #self.color = self.settings.bullet_color
        #在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
        image = pygame.image.load("images/fire.bmp")
        self.imaged = pygame.transform.scale(image,(self.settings.bullet_width,self.settings.bullet_height))
        self.rect = self.imaged.get_rect()
        #self.rect = pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        #存储用小数表示的子弹位置
        self.y = float(self.rect.y)
    def update(self):
        """向上移动子弹"""
        #更新表示子弹位置的小数值
        self.y -= self.settings.bullet_speed
        #跟新子弹位置的小数值
        self.rect.y = self.y
    '''   
    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen,self.rect)
    '''

    def blitme(self):
        self.screen.blit(self.imaged,self.rect)
    