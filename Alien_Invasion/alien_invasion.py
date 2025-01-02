class Alien_Invasion:
    import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import Game_stats
from button import Button
class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
       """初始化游戏并创建游戏资源"""
       pygame.init()
       self.settings = Settings()
       self.screen = pygame.display.set_mode((0,0),pygame.RESIZABLE)
       self.settings.screen_width = self.screen.get_rect().width
       self.settings.screen_height = self.screen.get_rect().height
       pygame.display.set_caption("Alien Invation")
       #创建一个用于存储游戏统计信息的实例
       self.stats = Game_stats(self)
       self.ship = Ship(self) 
       self.bullets = pygame.sprite.Group()
       self.aliens = pygame.sprite.Group()
       self._create_fleet()
       self.play_button = Button(self,"Play")
    def run_game(self):
        """开始游戏的主循环""" 
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()  
                self._update_aliens()
            self._update_screeen()
    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pose = pygame.mouse.get_pos()#返回关于鼠标点击的坐标元组
                self._check_play_button(mouse_pose) 
    def _check_play_button(self,mouse_pose):
        """玩家在点击Play时开始游戏"""
        if self.play_button.rect.collidepoint(mouse_pose):
            self.stats.game_active = True
    def _check_keydown_events(self,event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_q:
            sys.exit()
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
       

    
    def _check_keyup_events(self,event):
        """响应松开"""
        if event.key == pygame.K_RIGHT:
           self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False 
    def _fire_bullet(self):
        """创建一个子弹,并将其加入编组bullets中"""          
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    def _update_bullets(self):
        #跟新子弹的位置
        self.bullets.update()        
        #删除多余的子弹
        for bullet in self.bullets.copy():  #不能从for循环遍历的列表中删除列表中的元素，创建个副本
            if bullet.rect.bottom < 0 :
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
    def _check_bullet_alien_collisions(self):
        """响应子弹与外星人碰撞"""
        #删除发生碰撞的外星人和子弹
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if not self.aliens:
            #删除现有的所有子弹，并创建一群新的外星人
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘,并更新整群外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()
        #检测外星人与飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        #检查是否有外星人到达屏幕底端
        self._check_aliens_bottom()
    def _ship_hit(self):
        """响应飞船被外星人撞到。"""  
        if self.stats.ships_left > 0:          
            #将ship_left减1
            self.stats.ships_left -= 1

            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            #创建一群新的外星人，并将飞船放到屏幕底端中央
            self._create_fleet()
            self.ship.center_ship()
            #暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
    def _create_fleet(self):
        """创建外星人群"""
        #创建一个外星人并计算一行可容纳多少个外星人
        #外星人的间距为外星人的宽度
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - 2 * alien_width
        number_alien_x = available_space_x // (alien_width * 2)
        #计算可容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height-(3*alien_height)-ship_height)
        number_rows = available_space_y // (alien_height * 2)
        #创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number,row_number)
    def _create_alien(self,alien_number,row_number):
        """创建一个外星人并将其放在第一行"""
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x =alien_width + 2 *alien_width * alien_number
        alien.rect.x =alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #像飞船被撞到一样处理
                self._ship_hit()
                break
    def _change_fleet_direction(self):
        """将整群外星人下移,并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    def _check_play_button(self,mouse_pos):
        """玩家在单击Play按钮时开始游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #重置游戏统计信息
            self.stats.reset_stats()
            self.stats.game_active = True

            #清空余下的子弹和外星人
            self.bullets.empty()
            self.aliens.empty()

            #创建新的外星人，并让飞船居中
            self._create_fleet()
            self.ship.center_ship()
    def _update_screeen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            #bullet.draw_bullet()
            bullet.blitme()
        self.aliens.draw(self.screen)
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()
        
if __name__ =='__main__':
    #创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()

