class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""
    def __init__(self):
        """初始化游戏设置"""
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        self.ship_speed = 1.5
        self.ship_limit = 3
        self.bullet_speed = 1.5
        self.bullet_width = 6
        self.bullet_height = 15
        #self.bullet_color = (60,60,60)
        self.bullet_allowed = 3
        #外星人设置
        self.alien_speed = 0.5
        self.fleet_drop_speed = 50
        #fleet_direction 为1表示右移，-1 左移
        self.fleet_direction = 1