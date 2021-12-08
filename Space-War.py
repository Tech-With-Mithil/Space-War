import os 
import random
import winsound
import time

#Import the Turtle module:
import turtle
#Required by MacOSX to show the window:
turtle.fd(0)
#Set the animations speed to the maximum:
turtle.speed(0)
#Change the background color:
turtle.bgcolor("black")
#Change the window title:
turtle.title("SpaceWar")
#Change the background image:
turtle.bgpic("starfield.gif")
#Hide the turtle:
turtle.ht()
#This saves memory:
turtle.setundobuffer(1)
#This speeds up the drawing:
turtle.tracer(20)

class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        #Boundary detection:
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

    def is_collision(self, other):
        if (self.xcor() >= (other.xcor() - 20)) and \
        (self.xcor() <= (other.xcor() + 20)) and \
        (self.ycor() >= (other.ycor() - 20)) and \
        (self.ycor() <= (other.ycor() + 20)):
            return True
        else:
            return False

class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid = 0.6, stretch_len = 1.1, outline = None)
        self.speed = 4
        self.lives = 3
        
    def turn_left(self):
        self.lt(45)

    def turn_right(self):
        self.rt(45)

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1

class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0,360))

class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 8
        self.setheading(random.randint(0,360))

        def move(self):
            self.fd(self.speed)

            #Boundary detection:
            if self.xcor() > 290:
                self.setx(290)
                self.lt(60)

            if self.xcor() < -290:
                self.setx(-290)
                self.lt(60)

            if self.ycor() > 290:
                self.sety(290)
                self.lt(60)

            if self.ycor() < -290:
                self.sety(-290)
                self.lt(60)


class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid = 0.2, stretch_len = 0.4, outline = None)
        self.speed = 40
        self.status = "ready"
        self.goto(-1000, 1000)

    def fire(self):
        if self.status == "ready":
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"

    def move(self):
        if self.status == "ready":
            self.goto(-1000, 1000)
        
        if self.status == "firing":
            self.fd(self.speed)

        #Border Checking:
            if self.xcor()< -290 or self.xcor() > 290 or \
               self.ycor()< -290 or self.ycor() > 290:
                self.goto(-1000, 1000)
                self.status = "ready"

class Particles(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid = 0.1, stretch_len = 0.1, outline = None)
        self.goto(-1000, 1000)
        self.frame = 0

    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0,360))
        self.frame = 1

    def move(self):
        if self.frame > 0:
            self.fd(10)
            self.frame += 1

        if self.frame > 20:
            self.frame = 0
            self.goto(-1000, -1000)


class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3

    def draw_border(self):
        #Draw border:
        self.pen.speed(0)
        self.pen.color("alice blue")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg = "Score: %s" %(self.score)
        self.pen.penup()
        self.pen.goto(-300, 310)
        self.pen.write(msg, font = ("Times New Roman", 16, "bold"))

#Create game object:
game = Game()

#Draw the game border:
game.draw_border()

#Show the gane status:
game.show_status()
    
#Create my sprites:
player = Player("triangle", "cyan2", 0, 0)
#enemy = Enemy("circle", "red", -100, 0)
missile = Missile("triangle", "yellow", 0, 0)
#ally = Ally("square", "blue", 100, 0)


enemies = []
for i in range(8):
    enemies.append(Enemy("circle", "red", -100, 0))

allies = []
for i in range(7):
    allies.append(Ally("square", "blue", 100, 0))

particles = []
for i in range(50):
    particles.append(Particles("circle", "orange", 0,0))


#Keyboard Bindings:
turtle.listen()
turtle.onkey(player.turn_left, "a")
turtle.onkey(player.turn_right, "d")
turtle.onkey(player.accelerate, "w")
turtle.onkey(player.decelerate, "s")
turtle.onkey(missile.fire, "space")

#Main Game Loop:
while True:
    turtle.update()
    time.sleep(0.02)

    player.move()
    missile.move()
    
    #Enemy:
    for enemy in enemies:
        enemy.move()

        #Check for a collision with the player:
        if player.is_collision(enemy):
            winsound.PlaySound("laser.mp3", winsound.SND_ASYNC)
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            game.score -= 350
            game.show_status()


        #Check for a collision b/w the missile and the enemy:
        if missile.is_collision(enemy):
            winsound.PlaySound("laser.mp3", winsound.SND_ASYNC)
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            missile.status = "ready"
            #Increase the score:
            game.score += 500
            game.show_status()
            #Do the explosion:
            for particle in particles:
                particle.explode(missile.xcor(), missile.ycor())
                



    #Ally:                
    for ally in allies:
        ally.move()

        #Check for a collision b/w the missile and the ally:
        if missile.is_collision(ally):
            winsound.PlaySound("laser.mp3", winsound.SND_ASYNC)
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            missile.status = "ready"
            #Decrease the score:
            game.score -= 100
            game.show_status()

        #Check for a collision with the enemy:
        if ally.is_collision(enemy):
            winsound.PlaySound("laser.mp3", winsound.SND_ASYNC)
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            game.score += 100
            game.show_status()


    #Particle
    for particle in particles:
        particle.move()

        if particle.is_collision(enemy):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            game.score += 8
