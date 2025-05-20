import pygame
import random
import sys
import time
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)  # Color for obstacles
ORANGE = (255, 165, 0)  # Color for speed boost power-up
PINK = (255, 192, 203)  # Color for invincibility power-up
LIGHT_BLUE = (173, 216, 230)  # Color for destroy obstacles power-up
DARK_RED = (139, 0, 0)  # Dragon obstacle color

# Game modes
CLASSIC_MODE = "Classic"
MULTIPLAYER_MODE = "Multiplayer"
CHALLENGE_MODE = "Challenge"
DRAGON_MODE = "Dragon"

# Snake colors dictionary
SNAKE_COLORS = {
    'Blue': BLUE,
    'Green': GREEN,
    'Yellow': YELLOW,
    'Purple': PURPLE,
    'Cyan': CYAN
}

# Power-up types
INVINCIBILITY = "Invincibility"
DESTROY_OBSTACLES = "Destroy Obstacles"

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = BLUE
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        if new in self.positions[3:]:
            return False
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, 
                           (p[0] * GRID_SIZE, p[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))

    def render(self, surface):
        pygame.draw.rect(surface, self.color,
                        (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Directional constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def choose_snake_color():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Choose Snake Color')
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    # Create color options
    color_options = list(SNAKE_COLORS.items())
    button_height = 50
    button_width = 200
    spacing = 20
    total_height = (button_height + spacing) * len(color_options)
    start_y = (WINDOW_HEIGHT - total_height) // 2
    
    selected_color = None
    
    while selected_color is None:
        screen.fill(BLACK)
        
        # Draw title
        title = font.render('Choose Your Snake Color', True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, start_y - 50))
        screen.blit(title, title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        for i, (color_name, color_value) in enumerate(color_options):
            button_y = start_y + i * (button_height + spacing)
            button_rect = pygame.Rect((WINDOW_WIDTH - button_width) // 2, button_y, button_width, button_height)
            
            # Check if mouse is hovering over button
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, WHITE, button_rect, 3)
            else:
                pygame.draw.rect(screen, WHITE, button_rect, 1)
            
            # Draw color preview
            preview_rect = pygame.Rect(button_rect.left + 10, button_rect.top + 10, 
                                     button_height - 20, button_height - 20)
            pygame.draw.rect(screen, color_value, preview_rect)
            
            # Draw color name
            text = font.render(color_name, True, WHITE)
            text_rect = text.get_rect(midleft=(preview_rect.right + 10, 
                                             button_rect.top + button_height // 2))
            screen.blit(text, text_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, (color_name, color_value) in enumerate(color_options):
                    button_y = start_y + i * (button_height + spacing)
                    button_rect = pygame.Rect((WINDOW_WIDTH - button_width) // 2, 
                                            button_y, button_width, button_height)
                    if button_rect.collidepoint(event.pos):
                        selected_color = color_value
        
        pygame.display.update()
        clock.tick(60)
    
    return selected_color

def show_game_over_screen(screen, score):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    game_over_text = font.render('GAME OVER', True, WHITE)
    score_text = font.render(f'Final Score: {score}', True, WHITE)
    
    game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
    
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    pygame.display.update()
    
    # Wait for 2 seconds before continuing
    pygame.time.wait(2000)

def show_start_menu(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    
    # Create menu options
    menu_options = [CLASSIC_MODE, MULTIPLAYER_MODE, CHALLENGE_MODE, DRAGON_MODE]
    button_height = 60
    button_width = 300
    spacing = 20
    total_height = (button_height + spacing) * len(menu_options)
    start_y = (WINDOW_HEIGHT - total_height) // 2
    
    selected_mode = None
    
    while selected_mode is None:
        screen.fill(BLACK)
        
        # Draw title
        title = font.render('SNAKE GAME', True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, start_y - 100))
        screen.blit(title, title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        for i, option in enumerate(menu_options):
            button_y = start_y + i * (button_height + spacing)
            button_rect = pygame.Rect((WINDOW_WIDTH - button_width) // 2, button_y, button_width, button_height)
            
            # Check if mouse is hovering over button
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, WHITE, button_rect, 3)
            else:
                pygame.draw.rect(screen, WHITE, button_rect, 1)
            
            # Draw option text
            text = small_font.render(option, True, WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, option in enumerate(menu_options):
                    button_y = start_y + i * (button_height + spacing)
                    button_rect = pygame.Rect((WINDOW_WIDTH - button_width) // 2, 
                                            button_y, button_width, button_height)
                    if button_rect.collidepoint(event.pos):
                        selected_mode = option
        
        pygame.display.update()
        clock.tick(60)
    
    return selected_mode

class Obstacle:
    def __init__(self):
        self.positions = []
        self.color = GRAY
        self.generate_obstacles()

    def generate_obstacles(self):
        # Clear existing obstacles
        self.positions = []
        
        # Generate random number of obstacles (between 5 and 10)
        num_obstacles = random.randint(5, 10)
        
        # Create obstacles ensuring they don't overlap with each other
        # and don't block the entire path
        for _ in range(num_obstacles):
            while True:
                pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
                # Don't place obstacles in the center area where the snake starts
                if (abs(pos[0] - GRID_WIDTH//2) > 3 or abs(pos[1] - GRID_HEIGHT//2) > 3) and \
                   pos not in self.positions:
                    self.positions.append(pos)
                    break

    def render(self, surface):
        for pos in self.positions:
            pygame.draw.rect(surface, self.color,
                           (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class PowerUp:
    def __init__(self):
        self.position = (0, 0)
        self.type = None
        self.color = None
        self.active = False
        self.duration = 0
        self.start_time = 0
        self.randomize_position()
        self.randomize_type()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))

    def randomize_type(self):
        power_ups = [
            (INVINCIBILITY, PINK, 3),   # 3 seconds duration
            (DESTROY_OBSTACLES, LIGHT_BLUE, 1)  # Instant effect
        ]
        self.type, self.color, self.duration = random.choice(power_ups)

    def render(self, surface):
        if not self.active:
            pygame.draw.rect(surface, self.color,
                           (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, 
                            GRID_SIZE, GRID_SIZE))
            # Draw a star shape to make it look more like a power-up
            center_x = self.position[0] * GRID_SIZE + GRID_SIZE // 2
            center_y = self.position[1] * GRID_SIZE + GRID_SIZE // 2
            points = []
            for i in range(5):
                angle = i * (2 * 3.14159 / 5) - 3.14159 / 2
                points.append((
                    center_x + GRID_SIZE // 3 * 0.8 * math.cos(angle),
                    center_y + GRID_SIZE // 3 * 0.8 * math.sin(angle)
                ))
            pygame.draw.polygon(surface, WHITE, points)

    def activate(self):
        self.active = True
        self.start_time = time.time()

    def is_expired(self):
        if not self.active:
            return False
        return time.time() - self.start_time > self.duration

    def deactivate(self):
        self.active = False
        self.start_time = 0

class FireTrail:
    def __init__(self, position):
        self.position = position
        self.lifetime = 10  # Frames the trail will last
        self.color = ORANGE

    def update(self):
        self.lifetime -= 1
        return self.lifetime > 0

    def render(self, surface):
        alpha = int((self.lifetime / 10) * 255)  # Fade out effect
        color = (*self.color, alpha)
        pygame.draw.circle(surface, color,
                         (self.position[0] * GRID_SIZE + GRID_SIZE // 2,
                          self.position[1] * GRID_SIZE + GRID_SIZE // 2),
                         GRID_SIZE // 3)

class DragonObstacle:
    def __init__(self):
        self.position = (0, 0)
        self.color = DARK_RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))

    def render(self, surface):
        # Draw a dragon-like shape
        x = self.position[0] * GRID_SIZE
        y = self.position[1] * GRID_SIZE
        
        # Draw the main body
        pygame.draw.rect(surface, self.color, (x, y, GRID_SIZE, GRID_SIZE))
        
        # Draw spikes
        spike_points = [
            (x + GRID_SIZE//2, y - GRID_SIZE//4),  # Top spike
            (x + GRID_SIZE//4, y + GRID_SIZE//4),  # Left spike
            (x + 3*GRID_SIZE//4, y + GRID_SIZE//4)  # Right spike
        ]
        pygame.draw.polygon(surface, self.color, spike_points)

class Fireball:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.color = ORANGE
        self.active = True
        self.trail = []  # List to store fire trail positions
        self.lifetime = 30  # Number of frames the fireball will live
        self.speed = 3  # Fireball moves 3 times faster than snake
        self.destroy_radius = 1  # Radius of obstacle destruction

    def update(self):
        # Add current position to trail
        self.trail.append(FireTrail(self.position))
        
        # Update position with increased speed
        x, y = self.position
        dx, dy = self.direction
        # Move 3 times in the same direction
        for _ in range(self.speed):
            x = (x + dx) % GRID_WIDTH
            y = (y + dy) % GRID_HEIGHT
        self.position = (x, y)
        
        # Update and remove expired trails
        self.trail = [t for t in self.trail if t.update()]
        
        # Decrease lifetime
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.active = False

    def get_destroy_area(self):
        # Return all positions that will be affected by this fireball
        x, y = self.position
        positions = []
        for dx in range(-self.destroy_radius, self.destroy_radius + 1):
            for dy in range(-self.destroy_radius, self.destroy_radius + 1):
                pos = ((x + dx) % GRID_WIDTH, (y + dy) % GRID_HEIGHT)
                positions.append(pos)
        return positions

    def render(self, surface):
        if self.active:
            # Render trail first (so it appears behind the fireball)
            for trail in self.trail:
                trail.render(surface)
            
            # Render the fireball
            pygame.draw.circle(surface, self.color,
                             (self.position[0] * GRID_SIZE + GRID_SIZE // 2,
                              self.position[1] * GRID_SIZE + GRID_SIZE // 2),
                             GRID_SIZE // 2)

class DragonSnake(Snake):
    def __init__(self):
        super().__init__()
        self.fireballs = []
        self.fire_cooldown = 0
        self.fire_cooldown_time = 5  # Reduced cooldown time for more responsive shooting
        self.trail = []  # List to store snake's fire trail

    def shoot_fireball(self):
        if self.fire_cooldown <= 0:
            # Create fireball at the head position
            head_pos = self.get_head_position()
            self.fireballs.append(Fireball(head_pos, self.direction))
            self.fire_cooldown = self.fire_cooldown_time

    def update(self):
        # Add current position to trail
        self.trail.append(FireTrail(self.get_head_position()))
        
        # Update fire cooldown
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1

        # Update fireballs
        for fireball in self.fireballs[:]:
            fireball.update()
            if not fireball.active:  # Remove inactive fireballs
                self.fireballs.remove(fireball)

        # Update and remove expired trails
        self.trail = [t for t in self.trail if t.update()]

        # Update snake position
        return super().update()

    def render(self, surface):
        # Render fire trail
        for trail in self.trail:
            trail.render(surface)
        
        # Render fireballs
        for fireball in self.fireballs:
            fireball.render(surface)
        
        # Render snake
        super().render(surface)

class Particle:
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.velocity = (random.uniform(-2, 2), random.uniform(-2, 2))
        self.lifetime = 20
        self.size = random.randint(2, 4)

    def update(self):
        x, y = self.position
        vx, vy = self.velocity
        self.position = (x + vx, y + vy)
        self.lifetime -= 1
        return self.lifetime > 0

    def render(self, surface):
        alpha = int((self.lifetime / 20) * 255)
        color = (*self.color, alpha)
        pygame.draw.circle(surface, color,
                         (int(self.position[0]), int(self.position[1])),
                         self.size)

class DestructionEffect:
    def __init__(self, position):
        self.position = position
        self.particles = []
        self.lifetime = 15
        self.create_particles()

    def create_particles(self):
        x = self.position[0] * GRID_SIZE + GRID_SIZE // 2
        y = self.position[1] * GRID_SIZE + GRID_SIZE // 2
        for _ in range(10):  # Create 10 particles
            self.particles.append(Particle((x, y), ORANGE))

    def update(self):
        self.particles = [p for p in self.particles if p.update()]
        self.lifetime -= 1
        return self.lifetime > 0

    def render(self, surface):
        for particle in self.particles:
            particle.render(surface)

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Snake Game')
    
    while True:
        # Show start menu and get selected game mode
        game_mode = show_start_menu(screen)
        
        # Choose snake color before starting the game
        snake_color = choose_snake_color()
        
        if game_mode == CLASSIC_MODE:
            # Classic mode implementation
            clock = pygame.time.Clock()
            snake = Snake()
            snake.color = snake_color
            food = Food()
            
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and snake.direction != DOWN:
                            snake.direction = UP
                        elif event.key == pygame.K_DOWN and snake.direction != UP:
                            snake.direction = DOWN
                        elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                            snake.direction = LEFT
                        elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                            snake.direction = RIGHT
                        elif event.key == pygame.K_ESCAPE:
                            break  # Return to main menu
                
                if not snake.update():
                    show_game_over_screen(screen, snake.score)
                    break
                    
                if snake.get_head_position() == food.position:
                    snake.length += 1
                    snake.score += 1
                    food.randomize_position()
                
                screen.fill(BLACK)
                snake.render(screen)
                food.render(screen)
                
                # Display score
                font = pygame.font.Font(None, 36)
                score_text = font.render(f'Score: {snake.score}', True, WHITE)
                screen.blit(score_text, (10, 10))
                
                pygame.display.update()
                clock.tick(10)
        
        elif game_mode == MULTIPLAYER_MODE:
            # Placeholder for multiplayer mode
            font = pygame.font.Font(None, 36)
            text = font.render('Multiplayer mode coming soon!', True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.update()
            pygame.time.wait(2000)
        
        elif game_mode == CHALLENGE_MODE:
            clock = pygame.time.Clock()
            snake = Snake()
            snake.color = snake_color
            food = Food()
            obstacles = Obstacle()
            power_up = PowerUp()
            
            # Power-up states
            active_power_up = None
            power_up_start_time = 0
            power_up_duration = 0
            
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and snake.direction != DOWN:
                            snake.direction = UP
                        elif event.key == pygame.K_DOWN and snake.direction != UP:
                            snake.direction = DOWN
                        elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                            snake.direction = LEFT
                        elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                            snake.direction = RIGHT
                        elif event.key == pygame.K_ESCAPE:
                            break  # Return to main menu
                
                # Update snake position
                if not snake.update():
                    show_game_over_screen(screen, snake.score)
                    break
                
                # Check for collision with obstacles (unless invincible)
                if active_power_up != INVINCIBILITY and snake.get_head_position() in obstacles.positions:
                    show_game_over_screen(screen, snake.score)
                    break
                
                # Check for power-up collision
                if snake.get_head_position() == power_up.position and not power_up.active:
                    active_power_up = power_up.type
                    power_up_start_time = time.time()
                    power_up_duration = power_up.duration
                    power_up.activate()
                    
                    # Apply power-up effects
                    if active_power_up == DESTROY_OBSTACLES:
                        # Remove obstacles in a 3x3 area around the snake
                        head_pos = snake.get_head_position()
                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:
                                pos = ((head_pos[0] + dx) % GRID_WIDTH, 
                                      (head_pos[1] + dy) % GRID_HEIGHT)
                                if pos in obstacles.positions:
                                    obstacles.positions.remove(pos)
                    
                    # Generate new power-up
                    power_up = PowerUp()
                    while power_up.position in obstacles.positions or \
                          power_up.position == food.position:
                        power_up.randomize_position()
                
                # Check for power-up expiration
                if active_power_up and time.time() - power_up_start_time > power_up_duration:
                    active_power_up = None
                    power_up.deactivate()
                
                # Check for food collision
                if snake.get_head_position() == food.position:
                    snake.length += 1
                    snake.score += 1
                    # Generate new food position that's not on an obstacle
                    while True:
                        food.randomize_position()
                        if food.position not in obstacles.positions and \
                           food.position != power_up.position:
                            break
                
                # Render everything
                screen.fill(BLACK)
                obstacles.render(screen)
                snake.render(screen)
                food.render(screen)
                power_up.render(screen)
                
                # Display score and active power-up
                font = pygame.font.Font(None, 36)
                score_text = font.render(f'Score: {snake.score}', True, WHITE)
                screen.blit(score_text, (10, 10))
                
                if active_power_up:
                    power_up_text = font.render(f'Active: {active_power_up}', True, WHITE)
                    screen.blit(power_up_text, (10, 50))
                
                pygame.display.update()
                clock.tick(10)
        
        elif game_mode == DRAGON_MODE:
            clock = pygame.time.Clock()
            snake = DragonSnake()
            snake.color = snake_color
            food = Food()
            obstacles = [DragonObstacle() for _ in range(5)]  # Create 5 dragon obstacles
            destruction_effects = []  # List to store active destruction effects
            
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and snake.direction != DOWN:
                            snake.direction = UP
                        elif event.key == pygame.K_DOWN and snake.direction != UP:
                            snake.direction = DOWN
                        elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                            snake.direction = LEFT
                        elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                            snake.direction = RIGHT
                        elif event.key == pygame.K_SPACE:  # Shoot fireball
                            snake.shoot_fireball()
                        elif event.key == pygame.K_ESCAPE:
                            break  # Return to main menu
                
                if not snake.update():
                    show_game_over_screen(screen, snake.score)
                    break
                
                # Check for collision with obstacles
                if snake.get_head_position() in [obs.position for obs in obstacles]:
                    show_game_over_screen(screen, snake.score)
                    break
                
                # Check for food collision (both direct and fireball)
                food_collected = False
                if snake.get_head_position() == food.position:
                    food_collected = True
                else:
                    # Check fireball collisions with food
                    for fireball in snake.fireballs[:]:
                        if fireball.position == food.position:
                            food_collected = True
                            snake.fireballs.remove(fireball)
                            break
                
                if food_collected:
                    snake.length += 1
                    snake.score += 1
                    # Generate new food position that's not on an obstacle
                    while True:
                        food.randomize_position()
                        if food.position not in [obs.position for obs in obstacles]:
                            break
                
                # Check fireball collisions with obstacles
                for fireball in snake.fireballs[:]:
                    # Get all positions that will be affected by this fireball
                    destroy_positions = fireball.get_destroy_area()
                    
                    # Check if any obstacles are in the destroy area
                    obstacles_to_remove = []
                    for obstacle in obstacles:
                        if obstacle.position in destroy_positions:
                            obstacles_to_remove.append(obstacle)
                            # Create destruction effect
                            destruction_effects.append(DestructionEffect(obstacle.position))
                    
                    # Remove affected obstacles
                    for obstacle in obstacles_to_remove:
                        obstacles.remove(obstacle)
                    
                    # Remove the fireball if it hit any obstacles
                    if obstacles_to_remove:
                        if fireball in snake.fireballs:
                            snake.fireballs.remove(fireball)
                
                # Update destruction effects
                destruction_effects = [effect for effect in destruction_effects if effect.update()]
                
                # Render everything
                screen.fill(BLACK)
                for obstacle in obstacles:
                    obstacle.render(screen)
                snake.render(screen)
                food.render(screen)
                
                # Render destruction effects
                for effect in destruction_effects:
                    effect.render(screen)
                
                # Display score and obstacle count
                font = pygame.font.Font(None, 36)
                score_text = font.render(f'Score: {snake.score}', True, WHITE)
                screen.blit(score_text, (10, 10))
                
                # Display controls and obstacle count
                controls_text = font.render('SPACE to shoot fireball', True, WHITE)
                screen.blit(controls_text, (10, 50))
                
                obstacle_text = font.render(f'Obstacles: {len(obstacles)}', True, WHITE)
                screen.blit(obstacle_text, (10, 90))
                
                pygame.display.update()
                clock.tick(10)

if __name__ == '__main__':
    main()
   