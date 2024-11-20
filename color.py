import math
import pygame as pygame
from pygame import Vector2, Color
import moviepy.editor as mpy
import os
from datetime import datetime

# Pygame setup
width, height = 700, 700
fps = 120  # Frames per second for smooth video
duration = 15  # Video duration in seconds
total_frames = fps * duration

screen = pygame.Surface((width, height))  # Off-screen surface for rendering

class Ball:
    def __init__(self):
        self.position = Vector2(width / 2, height / 2)
        self.color = (255, 215, 0)
        self.gravity = Vector2(0, 0.32)
        self.velocity = Vector2(-7, -7)
        self.prevPos = Vector2(self.position.x, self.position.y)
        self.radius = 30

    def update(self):
        self.prevPos = Vector2(self.position.x, self.position.y)

        # Movement
        self.velocity += self.gravity
        self.position += self.velocity

        dirToCenter = Vector2(self.position.x - width / 2, self.position.y - height / 2)
        if self.isCollide():
            self.radius += 1
            self.position = Vector2(self.prevPos.x, self.prevPos.y)
            v = math.sqrt(self.velocity.x**2 + self.velocity.y**2)
            angleToCollisionPoint = math.atan2(-dirToCenter.y, dirToCenter.x)
            oldAngle = math.atan2(-self.velocity.y, self.velocity.x)
            newAngle = 2 * angleToCollisionPoint - oldAngle
            self.velocity = Vector2(-v * math.cos(newAngle), v * math.sin(newAngle))

    def isCollide(self):
        return self.distance(self.position.x, self.position.y, width / 2, height / 2) > width / 2 - self.radius

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)

# Ball and color setup
ball = Ball()
color = Color(211, 12, 211)
h, s, l = color.hsla[0], color.hsla[1], color.hsla[2]
colorDir = 1

# Frame storage for video
frames = []

for frame_num in range(total_frames):
    screen.fill((53, 53, 88))  # Background color
    pygame.draw.circle(screen, (255, 0, 0), (width // 2, height // 2), width // 2, 5)

    # Update ball and color
    ball.update()
    color.hsla = (h, s, l, 1)
    h += 1 * colorDir
    if h >= 360:
        colorDir = -1
    elif h <= 0:
        colorDir = 1

    pygame.draw.circle(screen,
                       (color.r, color.g, color.b),
                       (int(ball.position.x), int(ball.position.y)),
                       ball.radius + 2)

    ball.draw()

    # Save the current frame
    frames.append(pygame.surfarray.array3d(screen).swapaxes(0, 1))

    # Print progress
    if frame_num % fps == 0:
        print(f"Progress: {frame_num // fps} seconds")

# Generate a unique filename
def generate_unique_filename(base_name="output_video", ext=".mp4"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base_name}_{timestamp}{ext}"
    while os.path.exists(filename):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{base_name}_{timestamp}{ext}"
    return filename

output_file = generate_unique_filename()

# Create video with moviepy
clip = mpy.ImageSequenceClip(frames, fps=fps)
clip.write_videofile(output_file, codec="libx264", fps=fps)

print(f"Video saved as: {output_file}")
