class Cloud:
    def __init__(self, x, y, z):
        self.pos = [x, y, z]
        self.size = random.uniform(0.5, 2.0)  # Random size for variety
        self.opacity = random.uniform(0.1, 0.3)  # Random opacity
        self.color = [0.8, 0.8, 0.8, self.opacity]  # Light gray with opacity

    def update(self):
        # Move clouds slowly
        self.pos[2] += 0.01  # Move forward
        # Reset position if too far
        if self.pos[2] > 50:
            self.pos[2] = -50
            self.pos[0] = random.uniform(-20, 20)
            self.pos[1] = random.uniform(-15, 15)

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.pos)
        
        # Enable blending for transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Draw cloud particle
        glColor4f(*self.color)
        glutSolidSphere(self.size, 8, 8)
        
        glDisable(GL_BLEND)
        glPopMatrix()

def generate_clouds():
    global clouds
    clouds = []
    # Generate initial clouds
    for _ in range(50):  # Number of cloud particles
        x = random.uniform(-20, 20)
        y = random.uniform(-15, 15)
        z = random.uniform(-50, 50)
        clouds.append(Cloud(x, y, z))

def draw_clouds():
    global clouds
    for cloud in clouds:
        cloud.update()
        cloud.draw()

# Bullet class
class Bullet:
    def __init__(self, x, y, z):
        self.pos = [x, y, z]
        self.speed = 0.2
        self.damage = 1  # Basic damage
        self.alive = True

    def update(self):
        self.pos[2] -= self.speed  # Move bullet forward

    def draw(self):
        if self.alive:
            glPushMatrix()
            glTranslatef(self.pos[0], self.pos[1], self.pos[2])
            glColor3f(1.0, 0.0, 0.0)  # Red color for bullets
            glutSolidSphere(0.05, 8, 8)
            glPopMatrix()

# Missile class
class Missile:
    def __init__(self, x, y, z):
        self.pos = [x, y, z]
        self.speed = 0.3
        self.damage = 5  # Increased damage for missiles
        self.alive = True
        self.target = None  # Will store nearest enemy when fired
        self.explosion_radius = 2.0  # Area of effect for missile explosion

    def update(self):
        if self.alive:
            if self.target and self.target.alive:
                # Calculate direction to target
                dx = self.target.pos[0] - self.pos[0]
                dy = self.target.pos[1] - self.pos[1]
                dz = self.target.pos[2] - self.pos[2]
                dist = (dx*dx + dy*dy + dz*dz)**0.5
                
                # Move towards target
                if dist > 0:
                    self.pos[0] += (dx/dist) * self.speed
                    self.pos[1] += (dy/dist) * self.speed
                    self.pos[2] += (dz/dist) * self.speed
            else:
                # If no target, move forward
                self.pos[2] -= self.speed

    def draw(self):
        if self.alive:
            glPushMatrix()
            glTranslatef(self.pos[0], self.pos[1], self.pos[2])
            glColor3f(1.0, 0.5, 0.0)  # Orange color for missiles
            # Draw missile body
            glPushMatrix()
            glRotatef(90, 1, 0, 0)
            glutSolidCone(0.1, 0.3, 8, 8)
            glPopMatrix()
            # Draw missile trail
            glColor3f(1.0, 0.3, 0.0)
            glBegin(GL_LINES)
            glVertex3f(0, 0, 0.3)
            glVertex3f(0, 0, 0.5)
            glEnd()
            glPopMatrix()

def upgrade_spaceship():
    global bounty, spaceship_level, spaceship_color
    if bounty >= 200:
        bounty -= 200
        spaceship_level += 1
        # Randomly change spaceship color
        spaceship_color = [random.random(), random.random(), random.random()]
        print('Spaceship upgraded! Level:', spaceship_level)

def change_level_colors():
    global space_color, enemy_color, clouds
    if difficulty == 'medium':
        # Dark blue space with green enemies
        space_color = [0.0, 0.0, 0.2]  # Dark blue
        enemy_color = [0.0, 1.0, 0.0]  # Green
        # Update cloud colors for medium level
        for cloud in clouds:
            cloud.color = [0.6, 0.8, 1.0, cloud.opacity]  # Light blue clouds
    elif difficulty == 'hard':
        # Dark purple space with yellow enemies
        space_color = [0.2, 0.0, 0.2]  # Dark purple
        enemy_color = [1.0, 1.0, 0.0]  # Yellow
        # Update cloud colors for hard level
        for cloud in clouds:
            cloud.color = [0.8, 0.6, 1.0, cloud.opacity]  # Light purple clouds
    else:  # easy
        # Black space with red enemies
        space_color = [0.0, 0.0, 0.0]  # Black
        enemy_color = [1.0, 0.0, 0.0]  # Red
        # Update cloud colors for easy level
        for cloud in clouds:
            cloud.color = [0.8, 0.8, 0.8, cloud.opacity]  # Light gray clouds
    
    # Update the background color
    glClearColor(*space_color, 1.0)



    #     if enemies_left == 0:
    # if difficulty == 'easy':
    #     difficulty = 'medium'
    #     print('Difficulty increased to Medium!')
    #     reset_game()
    # elif difficulty == 'medium':
    #     difficulty = 'hard'
    #     print('Difficulty increased to Hard!')
    #     reset_game()
    # elif difficulty == 'hard':
    #     print('Congratulations! You have completed all difficulty levels!')
    #     game_over = True