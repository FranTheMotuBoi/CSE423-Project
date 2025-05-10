##22101762_farhantanvir_cse423sec01


class Missile:
    def __init__(self, x, y, z):
        self.pos = [x, y, z]
        self.speed = 0.3
        self.damage = 5  
        self.alive = True
        self.target = None  
        self.explosion_radius = 2.0  

    def update(self):
        if self.alive:
            if self.target and self.target.alive:
        
                dx = self.target.pos[0] - self.pos[0]
                dy = self.target.pos[1] - self.pos[1]
                dz = self.target.pos[2] - self.pos[2]
                dist = (dx*dx + dy*dy + dz*dz)**0.5
                
                
                if dist > 0:
                    self.pos[0] += (dx/dist) * self.speed
                    self.pos[1] += (dy/dist) * self.speed
                    self.pos[2] += (dz/dist) * self.speed
            else:
                
                self.pos[2] -= self.speed

    def draw(self):
        if self.alive:
            glPushMatrix()
            glTranslatef(self.pos[0], self.pos[1], self.pos[2])
            glColor3f(1.0, 0.5, 0.0) 
            glPushMatrix()
            glRotatef(90, 1, 0, 0)
            glutSolidCone(0.1, 0.3, 8, 8)
            glPopMatrix()
            glColor3f(1.0, 0.3, 0.0)
            glBegin(GL_LINES)
            glVertex3f(0, 0, 0.3)
            glVertex3f(0, 0, 0.5)
            glEnd()
            glPopMatrix()
            
            
    def draw_bullets():
        
        for bullet in player_bullets:
            bullet.draw()
    
        
        for missile in player_missiles:
            missile.draw()
    
        
        for bullet in enemy_bullets:
            bullet.draw()

        enemies = []

class Enemy:
    def __init__(self, x, y, z):
        self.pos = [x, y, z]
        self.alive = True

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

for _ in range(5):
    x = random.uniform(-10, 10)
    y = 0.0
    z = ship_pos[2] - random.uniform(30, 50)
    enemies.append(Enemy(x, y, z))

enemy_bullets = []

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

last_enemy_fire_time = 0

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
    

def mouse(button, state, x, y):
    global current_weapon, spaceship_level, game_over
    width = glutGet(GLUT_WINDOW_WIDTH)
    height = glutGet(GLUT_WINDOW_HEIGHT)
   
   
   
   
    # Calculate ortho size
    ortho_left, ortho_right = -10, 10
    ortho_bottom, ortho_top = -10, 10
    margin_x = 0.5
    margin_y = 0.5
    btn_width = 2.5
    btn_height = 1.5
    spacing = 0.5
    restart_x = ortho_left + margin_x
    restart_y = ortho_top - margin_y - btn_height
    quit_x = restart_x + btn_width + spacing
    quit_y = restart_y
    if game_over and state == GLUT_DOWN:
        # Convert mouse x, y to orthographic coordinates
        ortho_x = (x / width) * 20 - 10
        ortho_y = 10 - (y / height) * 20
        # Check Restart button
        if (restart_x <= ortho_x <= restart_x + btn_width and
            restart_y <= ortho_y <= restart_y + btn_height):
            reset_game()
            return
        # Check Quit button
        if (quit_x <= ortho_x <= quit_x + btn_width and
            quit_y <= ortho_y <= quit_y + btn_height):
            os._exit(0)
            return
            
            nd
            
            
            
            
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if cheat_mode:
            # Find nearest enemy and fire a bullet that hits it
            nearest_enemy = None
            min_dist = float('inf')
            for enemy in enemies:
                if enemy.alive:
                    dx = enemy.pos[0] - ship_pos[0]
                    dy = enemy.pos[1] - ship_pos[1]
                    dz = enemy.pos[2] - ship_pos[2]
                    dist = dx*dx + dy*dy + dz*dz
                    if dist < min_dist:
                        min_dist = dist
                        nearest_enemy = enemy
            if nearest_enemy:
                bullet = Bullet(ship_pos[0], ship_pos[1], ship_pos[2])
                bullet.pos = nearest_enemy.pos.copy()
                player_bullets.append(bullet)
        else:
            player_bullets.append(Bullet(ship_pos[0], ship_pos[1], ship_pos[2]))
            
            
            
            
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and (spaceship_level >= 2 or difficulty in ['medium', 'hard']):
       
       
       
       
       
       
       
       
       
        # Find nearest enemy for missile targeting
        nearest_enemy = None
        min_dist = float('inf')
        for enemy in enemies:
            if enemy.alive:
                dx = enemy.pos[0] - ship_pos[0]
                dy = enemy.pos[1] - ship_pos[1]
                dz = enemy.pos[2] - ship_pos[2]
                dist = dx*dx + dy*dy + dz*dz
                if dist < min_dist:
                    min_dist = dist
                    nearest_enemy = enemy
        missile = Missile(ship_pos[0], ship_pos[1], ship_pos[2])
        missile.target = nearest_enemy
        player_missiles.append(missile)
        
        
        
        
        
          
    
    
def keyboard(key, x, y):
    global ship_pos, camera_mode, current_weapon, spaceship_level, game_over, mirror_enabled, cheat_mode
    key = key.decode('utf-8')
    
    # Move the spaceship
    if key == 's':
        ship_pos[2] += 1  # Move forward (Z-axis)
    elif key == 'w':
        ship_pos[2] -= 1  # Move backward (Z-axis)
    elif key == 'a':
        ship_pos[0] -= 1  # Move left (X-axis)
    elif key == 'd':
        ship_pos[0] += 1  # Move right (X-axis)
    elif key == 'v':    
    
    
    
    
    
    
    
    
    