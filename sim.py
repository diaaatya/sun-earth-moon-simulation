import pygame
import math

# Step 1: Initialize pygame and create a display window
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sun-Earth-Moon Simulation")

# Step 2: Define colors for each celestial body
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)    # Earth
YELLOW = (255, 255, 0)  # Sun
GRAY = (169, 169, 169)  # Moon
LIGHT_BLUE = (173, 216, 230)  # Lighter blue for the Earth's trail

# Step 3: Define a simplified gravitational constant
G = 1  # Simplified gravitational constant for simulation stability

# Step 4: Define the Body class to represent the Sun and Earth
class Body:
    def __init__(self, x, y, mass, vx=0, vy=0, color=WHITE):
        self.x = x      # x position
        self.y = y      # y position
        self.mass = mass  # mass of the body
        self.vx = vx    # x velocity
        self.vy = vy    # y velocity
        self.color = color  # color to draw the body
        # Scale the radius based on mass for visualization
        self.radius = max(5, int(self.mass ** (1/3)))  # Simplified radius calculation

    # Step 5: Update the body's position based on its velocity
    def update_position(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    # Step 6: Draw the body on the pygame screen
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Step 7: Calculate gravitational force between two bodies
def calculate_gravitational_force(body1, body2):
    dx = body2.x - body1.x  # x distance
    dy = body2.y - body1.y  # y distance
    distance = math.sqrt(dx**2 + dy**2)  # distance between two bodies

    if distance < 1:  # Avoid division by zero or extremely small distance
        distance = 1

    # Gravitational force magnitude with simplified G
    force = G * body1.mass * body2.mass / distance**2

    # Force components in x and y directions
    angle = math.atan2(dy, dx)
    fx = math.cos(angle) * force
    fy = math.sin(angle) * force

    return fx, fy

# Step 8: Define the Sun and Earth with simplified masses
# Sun is stationary at the center with a simplified mass
sun = Body(x=400, y=300, mass=1000, color=YELLOW)

# Earth orbits the Sun with simplified mass and speed
earth = Body(x=600, y=300, mass=1, vy=2, color=BLUE)  # Simplified orbital speed

# Moon properties (circular orbit around Earth)
moon_distance = 50  # Distance between Earth and Moon in pixels
moon_orbital_speed = 0.09  # Fixed angular speed (in radians per second)
moon_angle = 0  # Initial angle of the Moon

# Create a list to store Earth's previous positions (for the trail effect)
earth_trail = []  # List to store the positions
max_trail_length = 100  # Limit the number of trail points

# Step 9: Main simulation loop
running = True
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60) / 100  # Frame time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(BLACK)

    # Step 10: Calculate gravitational force between Sun and Earth
    fx_se, fy_se = calculate_gravitational_force(sun, earth)

    # Step 11: Update Earth's velocity based on forces from the Sun
    earth.vx -= fx_se / earth.mass * dt
    earth.vy -= fy_se / earth.mass * dt

    # Step 12: Update Earth's position
    earth.update_position(dt)

    # Step 13: Update Moon's position relative to the Earth
    moon_angle += moon_orbital_speed * dt  # Increment the Moon's angle
    moon_x = earth.x + moon_distance * math.cos(moon_angle)
    moon_y = earth.y + moon_distance * math.sin(moon_angle)

    # Step 14: Draw the trail for the Earth
    # Add the current position of the Earth to the trail list
    earth_trail.append((int(earth.x), int(earth.y)))

    # Limit the trail length
    if len(earth_trail) > max_trail_length:
        earth_trail.pop(0)  # Remove the oldest point if the trail exceeds the max length

    # Draw the trail points with a smaller radius and lighter color
    for pos in earth_trail:
        pygame.draw.circle(screen, LIGHT_BLUE, pos, 2)  # Thinner and different color for trail

    # Step 15: Draw the Sun, Earth, and Moon
    sun.draw(screen)  # The Sun stays stationary
    earth.draw(screen)  # Draw Earth after the trail so it's on top
    pygame.draw.circle(screen, GRAY, (int(moon_x), int(moon_y)), 5)  # Moon

    # Update the display
    pygame.display.flip()

pygame.quit()
