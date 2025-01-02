class Game_stats():
    """跟踪游戏的统计信息"""
    def __init__(self,ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_stats()
        #让游戏一开始处于非活跃状态
        self.game_active = False
    def reset_stats(self):
        """初始化在游戏期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit 