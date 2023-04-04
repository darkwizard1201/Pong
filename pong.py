from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint, choice

class PongPaddle(Widget):

    score = NumericProperty(0)

    def Collision(self, ball):
        if self.collide_widget(ball):
            speedup = 1.1
            ball.velocity = speedup * Vector(ball.velocity_x * -1, ball.velocity_y).rotate(randint(-30, 30))

class PongGame(Widget): 
    
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def on_touch_move(self, touch):
        if touch.x < self.width/3:
            self.player1.center_y = touch.y
        if touch.x > self.width*2/3:
            self.player2.center_y = touch.y
    
    def on_touch_down(self, touch):

        if touch.x < self.width/3:
            self.player1.center_y = touch.y
        if touch.x > self.width*2/3:
            self.player2.center_y = touch.y
    

    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(8, 0).rotate(choice([randint(-45, 45), randint(135, 225)]))

    def update(self, dt):
        self.ball.move()

        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        self.player1.Collision(self.ball)
        self.player2.Collision(self.ball)

        if (self.ball.x < 0):
            self.player2.score += 1
            self.serve_ball()
        elif (self.ball.right > self.width):
            self.player1.score += 1
            self.serve_ball()

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(self.velocity) + self.pos


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game
    

if __name__ == '__main__':
    PongApp().run()