# Set up camera view
    if camera_mode == 'third':
        gluLookAt(
            ship_pos[0], ship_pos[1] + 2, ship_pos[2] + 5,  # Eye position (behind and above the ship)
            ship_pos[0], ship_pos[1], ship_pos[2],          # Look at position (the ship itself)
            0, 1, 0                                      # Up vector (positive Y-axis)
        )
    elif camera_mode == 'first':
        gluLookAt(
            ship_pos[0], ship_pos[1] + 0.5, ship_pos[2] + 0.5,
            ship_pos[0], ship_pos[1], ship_pos[2] - 1,
            0, 1, 0
        )
        elif camera_mode == 'first':
        gluLookAt(
            ship_pos[0], ship_pos[1] + 0.5, ship_pos[2] + 0.5,  # Eye position (inside/slightly above the ship)
            ship_pos[0], ship_pos[1], ship_pos[2] - 1,          # Look at position (a point in front of the ship)
            0, 1, 0                                      # Up vector (positive Y-axis)
        )
        


class Enemy:
    def __init__(self, x, y, z):
        self.pos = [x, y, z]  # 3D position
        self.alive = True   # Is the enemy active?

    def update(self):
        # Move toward the player
        speed = 0.05
        if spaceship_level >= 2:
            speed = 0.12  # Increase speed at level 2
        self.pos[2] += speed  # Speed towards player

    def draw(self):
        if self.alive:
            glPushMatrix()
            glTranslatef(*self.pos)
            glScalef(0.5, 0.5, 0.5)  # Make enemy smaller than player
            glColor3f(*enemy_color)  # Use enemy_color

            # Body (cone)
            glPushMatrix()
            glRotatef(-90, 1, 0, 0)
            glutSolidCone(0.4, 1.0, 10, 10)
            glPopMatrix()

            # Wings (mini cubes)
            glColor3f(0.8, 0.0, 0.0)  # Darker red
            glPushMatrix()
            glTranslatef(-0.4, 0, 0)
            glScalef(0.2, 0.05, 0.3)
            glutSolidCube(1)
            glPopMatrix()

            glPushMatrix()
            glTranslatef(0.4, 0, 0)
            glScalef(0.2, 0.05, 0.3)
            glutSolidCube(1)
            glPopMatrix()

            glPopMatrix()

enemies = []  # List to store Enemy objects


if difficulty == 'easy':
    for _ in range(5):
        x = random.uniform(-10, 10)
        y = 0.0
        z = ship_pos[2] - random.uniform(30, 50)
        enemies.append(Enemy(x, y, z))
elif difficulty == 'medium':
    for _ in range(10):
        x = random.uniform(-10, 10)
        y = 0.0
        z = ship_pos[2] - random.uniform(30, 50)
        enemies.append(Enemy(x, y, z))
elif difficulty == 'hard':
    for _ in range(15):
        x = random.uniform(-10, 10)
        y = 0.0
        z = ship_pos[2] - random.uniform(30, 50)
        enemies.append(Enemy(x, y, z))

enemies_left = len(enemies)        
enemy_bullets = []  # List to store enemy bullets
last_enemy_fire_time = 0

class EnemyBullet:
    def __init__(self, x, y, z, direction):
        self.pos = [x, y, z]
        self.direction = direction  # A unit vector toward the player
        self.alive = True

    def update(self):
        if self.alive:
            self.pos[0] += self.direction[0] * 0.2
            self.pos[1] += self.direction[1] * 0.2
            self.pos[2] += self.direction[2] * 0.2

    def draw(self):
        if self.alive:

            glPushMatrix()
            glTranslatef(*self.pos)
            glColor3f(1.0, 0.5, 0.0)
            glutSolidSphere(0.1, 8, 8)
            glPopMatrix()

def fire_enemy_bullets():
    global last_enemy_fire_time
    now = time.time()
    if now - last_enemy_fire_time < 1.5:  # 1.5 seconds between shots
        return
    last_enemy_fire_time = now

    for enemy in enemies:
        if enemy.alive:
            dx = ship_pos[0] - enemy.pos[0]
            dy = ship_pos[1] - enemy.pos[1]
            dz = ship_pos[2] - enemy.pos[2]
            mag = (dx**2 + dy**2 + dz**2)**0.5
            direction = [dx/mag, dy/mag, dz/mag]
            bullet = EnemyBullet(enemy.pos[0], enemy.pos[1], enemy.pos[2], direction)
            enemy_bullets.append(bullet)
def check_collision(obj1_pos, obj2_pos, threshold=1.0):
    """Returns True if the distance between obj1 and obj2 is within the threshold."""
    dx = obj1_pos[0] - obj2_pos[0]
    dy = obj1_pos[1] - obj2_pos[1]
    dz = obj1_pos[2] - obj2_pos[2]
    distance = math.sqrt(dx**2 + dy**2 + dz**2)
    return distance < threshold

def check_bullet_enemy_collision():
    global enemies_destroyed, enemies_left, score, spaceship_level, difficulty, bounty
    collision_occurred = False

    # Check bullet collisions
    for bullet in player_bullets:
        for enemy in enemies:
            if bullet.alive and enemy.alive and check_collision(bullet.pos, enemy.pos, threshold=0.5):
                bullet.alive = False
                enemy.alive = False
                enemies_destroyed += 1
                enemies_left -= 1
                score += 100  # Basic points for bullet kills
                bounty += 50  # Increase bounty
                collision_occurred = True
                # Level up after 10 enemies destroyed
                if enemies_destroyed == 10 and spaceship_level == 1:
                    spaceship_level = 2
                    print('Level Up! Missiles unlocked and enemies move faster!')

    # Check missile collisions
    for missile in player_missiles:
        for enemy in enemies:
            if missile.alive and enemy.alive:
                # Check for direct hit
                if check_collision(missile.pos, enemy.pos, threshold=0.8):
                    missile.alive = False
                    enemy.alive = False
                    enemies_destroyed += 1
                    enemies_left -= 1
                    score += 300  # Increased points for missile kills
                    bounty += 150  # Increase bounty
                    collision_occurred = True
                    # Level up after 10 enemies destroyed
                    if enemies_destroyed == 10 and spaceship_level == 1:
                        spaceship_level = 2
                        print('Level Up! Missiles unlocked and enemies move faster!')
                    # Check for nearby enemies that might be affected by explosion
                    for other_enemy in enemies:
                        if other_enemy != enemy and other_enemy.alive:
                            if check_collision(missile.pos, other_enemy.pos, threshold=missile.explosion_radius):
                                other_enemy.alive = False
                                enemies_destroyed += 1
                                enemies_left -= 1
                                score += 150  # Bonus points for explosion kills
                                bounty += 75  # Increase bounty
                                collision_occurred = True

    # Check difficulty level change after all collisions are processed
    if enemies_left == 0:
        if difficulty == 'easy':
            difficulty = 'medium'
            print('Difficulty increased to Medium!')
            reset_game()
        elif difficulty == 'medium':
            difficulty = 'hard'
            print('Difficulty increased to Hard!')
            reset_game()
        elif difficulty == 'hard':
            print('Congratulations! You have completed all difficulty levels!')
            game_over = True

    return collision_occurred

def check_enemy_player_collision():
    for enemy in enemies:
        if enemy.alive and check_collision(enemy.pos, ship_pos, threshold=0.7):
            return True
    return False

def check_bullet_player_collision():
    for bullet in enemy_bullets:
        if check_collision(bullet.pos, ship_pos, threshold=0.5):
            bullet.alive = False  # Destroy enemy bullet
            return True
    return False            