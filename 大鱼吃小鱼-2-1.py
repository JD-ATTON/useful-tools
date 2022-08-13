from arcade import*
from PIL import Image
import random

SCREEN_WIDTH=900
SCREEN_HEIGHT=600
SCREEN_TITLE="大傻逼吃小傻逼"
speed=5
left=1
right=0

class Player(Sprite):
    def __init__(self,image):
        super().__init__(image)
        self.center_x=SCREEN_WIDTH//2
        self.center_y=SCREEN_HEIGHT//2
        self.append_texture(load_texture("image/1.png",mirrored=True,scale=1))

        self.size=2

    def update(self):
        super().update()
        if self.left<0:
            self.left=0
        elif self.right>SCREEN_WIDTH:
            self.right=SCREEN_WIDTH
        if self.bottom<0:
            self.bottom=0
        elif self.top>SCREEN_HEIGHT:
            self.top=SCREEN_HEIGHT

    def jhua(self,score):
        if score>=9:
            self.size=9
        elif score>=5:
            self.size=6

class Enemy(Sprite):
    def __init__(self,image):
        super().__init__(image)
        face=random.choice(["left","right"])
        speed=random.choice([2,2.5,3,3.5,4])
        if face=="left":
            self.center_x=SCREEN_WIDTH+60
            self.change_x=-speed
            self.append_texture(load_texture(
                image, mirrored=True, scale=1))
            self.set_texture(1)
        elif face=="right":
            self.center_x=-60
            self.change_x = speed

        self.center_y = random.randint(0, SCREEN_HEIGHT)
        


class Game(arcade.Window):
    def __init__(self,width,height,title):
        super().__init__(width,height,title)
        self.setup()

    def setup(self):
        #Image.open("image/5.png").transpose(Image.FLIP_LEFT_RIGHT).save("image/5.png")
        self.background=Sprite("image/new_sea.png")
        self.background.center_x=SCREEN_WIDTH//2
        self.background.center_y=SCREEN_HEIGHT//2
        self.player=Player("image/1.png")
        self.player_list=SpriteList()
        self.player_list.append(self.player)
        self.fishes={"image/2.png":1,"image/3.png":3,"image/4.png":5,"image/5.png":7,"image/6.png":9}
        self.score=0
        self.enemy_sprite_list=SpriteList()
        self.totle_time=0
        self.last_time=0
        self.num=1

    def on_draw(self):
        start_render()
        self.background.draw()
        self.player_list.draw()
        self.enemy_sprite_list.draw()
        draw_text(f"score:{self.score}",0,SCREEN_HEIGHT-30,color.WHITE,font_name=("simhei","PingFang"),font_size=30)

    def on_update(self,delta_time):
        self.totle_time+=delta_time
        if int(self.totle_time) % 1 == 0 and int(self.last_time) != int(self.totle_time):
            self.scdr()
            self.last_time=self.totle_time
            self.num+=0.001
        self.player_list.update()
        self.enemy_sprite_list.update()
        for enemy in self.enemy_sprite_list:
            if enemy.center_x < -60 or enemy.center_x > SCREEN_WIDTH+60:
                enemy.kill()

        hit_list=check_for_collision_with_list(self.player,self.enemy_sprite_list)
        if hit_list:
            for hit in hit_list:
                if self.player.size>hit.size:
                    hit.kill()
                    self.score+=1
                else:
                    self.player.kill()
        self.player.jhua(self.score)
        

    def on_key_press(self,symbol,modifiers):
        if symbol==key.UP:
            self.player.change_y=speed
        elif symbol==key.DOWN:
            self.player.change_y=-speed
        elif symbol==key.LEFT:
            self.player.change_x=-speed
            self.player.set_texture(left)
        elif symbol==key.RIGHT:
            self.player.change_x=speed
            self.player.set_texture(right)
        elif symbol==key.RETURN:
            image=get_image(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
            image.save('screenshot.png')

    def on_key_release(self,symbol,modifiers):
        if symbol==key.UP or symbol==key.DOWN:
            self.player.change_y=0
        elif symbol==key.LEFT or symbol==key.RIGHT:
            self.player.change_x=0

    def scdr(self):
        for i in range(int(self.num)):
            fish=random.choice(list(self.fishes.keys()))
            size=self.fishes[fish]
            enemy_sprite=Enemy(fish)
            enemy_sprite.size=size
            self.enemy_sprite_list.append(enemy_sprite)
    


if __name__=='__main__':
    game=Game(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
    run()
