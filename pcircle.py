import math
import pygame
from pygame import Vector2, Color, mixer
import moviepy.editor as mp
import random

# Initialize pygame
pygame.init()

# Screen dimensions
width = 700
height = 700

# Set up display and clock
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
screen.fill((53, 53, 88), (0, 0, width, height))

# Draw the circle
pygame.draw.circle(screen, (255, 0, 0), (width / 2, height / 2), width / 2, 5)

# Initialize mixer for sound
mixer.init()
sound = mixer.Sound("jump.wav")

# Ball class
class Ball:
    def __init__(self):
        self.position = Vector2(random.uniform(100, width-100), random.uniform(100, height-100))
        self.color = (0, 0, 0)
        self.gravity = Vector2(0, 0.32)
        self.velocity = Vector2(random.uniform(-7, 7), random.uniform(-7, 7))
        self.prevPos = Vector2(self.position.x, self.position.y)
        self.radius = random.randint(5, 15)  # Random radius between 15 and 30

    def update(self):
        self.prevPos = Vector2(self.position.x, self.position.y)

        # Ball movement
        self.velocity += self.gravity
        self.position += self.velocity

        dirToCenter = Vector2(self.position.x - width / 2, self.position.y - height / 2)
        if self.isCollide():
            pygame.mixer.Sound.play(sound)
            self.radius += 1
            self.position = Vector2(self.prevPos.x, self.prevPos.y)
            v = math.sqrt(self.velocity.x * self.velocity.x + self.velocity.y * self.velocity.y)
            angleToCollisionPoint = math.atan2(-dirToCenter.y, dirToCenter.x)
            oldAngle = math.atan2(-self.velocity.y, self.velocity.x)
            newAngle = 2 * angleToCollisionPoint - oldAngle
            self.velocity = Vector2(-v * math.cos(newAngle), v * math.sin(newAngle))

    def isCollide(self):
        if self.distance(self.position.x, self.position.y, width / 2, height / 2) > width / 2 - self.radius:
            return True
        return False

    def distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) * 1.0)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.position.x, self.position.y), self.radius)

# Create multiple ball instances
balls = [Ball() for _ in range(4)]  # Adjust the number of balls as needed

circle_color = Color(255, 0, 0)
hit_count = 0

# Movie frame capture
frames = []

# Main loop
duration = 20  # Total time in seconds
start_ticks = pygame.time.get_ticks()
while pygame.time.get_ticks() - start_ticks < duration * 1000:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # Update each ball and check for collision
    for ball in balls:
        ball.update()

    # Change color of ball and circle gradually after collision
    if hit_count < 10:
        for ball in balls:
            if ball.isCollide():
                ball.color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                hit_count += 1

    # Draw the background and circle
    screen.fill((53, 53, 88), (0, 0, width, height))
    pygame.draw.circle(screen, (circle_color.r, circle_color.g, circle_color.b), (width / 2, height / 2), width / 2, 6)

    # Draw all balls
    for ball in balls:
        ball.draw()

    # Capture the current frame for video
    frames.append(pygame.surfarray.array3d(pygame.display.get_surface()).transpose(1, 0, 2))

    # Update the display
    pygame.display.flip()

# Create a video from the captured frames using moviepy
clip = mp.ImageSequenceClip(frames, fps=60)
clip.write_videofile("bouncing_balls_in_circle.mp4", codec="libx264")

# Quit pygame
pygame.quit()
