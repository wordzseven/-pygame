class Settings():

    def __init__(self):
        self.screen_width = 600
        self.screen_height = 800
        self.bg_color = (255, 255, 255)
        self.ship_speed = 1.5
        self.ship_limit = 3

        #Параметры снаряда
        self.bullet_speed = 2
        self.bullet_width = 1900
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)

        #параметры пришельцев
        self.alien_speed = 5.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
