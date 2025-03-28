import pygame
import sys
import math

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Light Reflection Simulation")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Mirror:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.color = BLUE

    def draw(self):
        pygame.draw.line(screen, self.color, self.start, self.end, 3)

class Ray:
    def __init__(self, pos, direction):
        self.pos = pos
        self.dir = direction.normalize()
        self.max_bounces = 5  # Limit reflections to prevent infinite loops
        self.bounces = 0

    def update(self, mirrors):
        current_pos = self.pos
        step = self.dir * 2  # Step size for ray movement

        for _ in range(1000):  # Max ray length
            current_pos += step
            if not (0 <= current_pos.x <= WIDTH and 0 <= current_pos.y <= HEIGHT):
                break

            # Check for collisions with mirrors
            for mirror in mirrors:
                intersection = self.check_intersection(current_pos, mirror)
                if intersection and self.bounces < self.max_bounces:
                    self.bounces += 1
                    self.dir = self.reflect(self.dir, mirror)
                    current_pos = intersection
                    break

            pygame.draw.line(screen, RED, current_pos - step, current_pos, 1)
        return

    def check_intersection(self, pos, mirror):
        # Line-line intersection logic
        x1, y1 = mirror.start
        x2, y2 = mirror.end
        x3, y3 = pos - self.dir * 10  # Previous position
        x4, y4 = pos

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return None

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        if 0 <= t <= 1 and 0 <= u <= 1:
            return pygame.Vector2(x1 + t * (x2 - x1), y1 + t * (y2 - y1))
        return None

    def reflect(self, dir, mirror):
        # Calculate mirror's normal vector
        mirror_line = pygame.Vector2(mirror.end) - pygame.Vector2(mirror.start)
        normal = pygame.Vector2(-mirror_line.y, mirror_line.x).normalize()
        return dir.reflect(normal)

# Main loop
mirrors = []
light_source = pygame.Vector2(WIDTH//2, HEIGHT//2)
rays = [Ray(light_source, pygame.Vector2(math.cos(angle), math.sin(angle))) 
        for angle in [0, math.pi/4, math.pi/2, 3*math.pi/4]]

running = True
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click to place mirrors
                start = pygame.mouse.get_pos()
                end = start + pygame.Vector2(50, 50)
                mirrors.append(Mirror(start, end))

    # Update and draw rays
    for ray in rays:
        ray.update(mirrors)
    
    # Draw mirrors
    for mirror in mirrors:
        mirror.draw()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
