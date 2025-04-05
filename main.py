import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
GRAVITY = 0.25
BIRD_JUMP = -6
PIPE_SPEED = 3
PIPE_GAP = 200

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

class Bird:
    def __init__(self):
        self.x = WIDTH // 4
        self.y = HEIGHT // 2
        self.velocity = 0
        self.radius = 20

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def jump(self):
        self.velocity = BIRD_JUMP

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(100, HEIGHT - PIPE_GAP - 100)
        self.width = 80
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self):
        # Top pipe
        pygame.draw.rect(screen, WHITE, (self.x, 0, self.width, self.height))
        # Bottom pipe
        pygame.draw.rect(screen, WHITE, (self.x, self.height + PIPE_GAP, 
                                       self.width, HEIGHT - self.height - PIPE_GAP))

def check_collision(bird, pipe):
    bird_rect = pygame.Rect(bird.x - bird.radius, bird.y - bird.radius,
                          bird.radius * 2, bird.radius * 2)
    top_pipe = pygame.Rect(pipe.x, 0, pipe.width, pipe.height)
    bottom_pipe = pygame.Rect(pipe.x, pipe.height + PIPE_GAP,
                            pipe.width, HEIGHT - pipe.height - PIPE_GAP)
    
    return bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe)

def main():
    bird = Bird()
    pipes = []
    score = 0
    pipe_spawn_timer = 0
    
    # Font for score
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        # Update
        bird.update()
        
        # Spawn pipes
        pipe_spawn_timer += 1
        if pipe_spawn_timer >= 90:  # Spawn new pipe every ~1.5 seconds at 60 FPS
            pipes.append(Pipe())
            pipe_spawn_timer = 0

        # Update pipes
        for pipe in pipes[:]:
            pipe.update()
            if pipe.x + pipe.width < 0:
                pipes.remove(pipe)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                score += 1

        # Check collisions
        for pipe in pipes:
            if check_collision(bird, pipe):
                running = False

        # Check boundaries
        if bird.y - bird.radius < 0 or bird.y + bird.radius > HEIGHT:
            running = False

        # Draw
        screen.fill(BLACK)
        
        for pipe in pipes:
            pipe.draw()
        bird.draw()
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()