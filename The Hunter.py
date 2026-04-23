import pygame
import random
import math
import sys
import os


# ## PATH HELPER FUNCTION ##
# This is CRITICAL for the "One-File" software to work.
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ## PART 1: ENGINE SETUP ##
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("The Hunter")
screen = pygame.display.set_mode((1400, 700))
clock = pygame.time.Clock()

# ## PART 2: FONTS ##
score_font = pygame.font.SysFont("Arial", 32)
game_over_font = pygame.font.SysFont("Arial", 100)
menu_font = pygame.font.SysFont("Arial", 50)

# ## PART 3: ASSET LOADING ##
# All images/sounds must use resource_path()
bg_img = pygame.image.load(resource_path('background2.png'))
bg_img = pygame.transform.scale(bg_img, (1400, 700))

man_btn_img = pygame.image.load(resource_path('player_male1.png'))
man_btn_img = pygame.transform.scale(man_btn_img, (200, 200))
woman_btn_img = pygame.image.load(resource_path('player_gir1l.png'))
woman_btn_img = pygame.transform.scale(woman_btn_img, (200, 200))

player_girl = pygame.image.load(resource_path('player_girl.png'))
player_girl = pygame.transform.scale(player_girl, (75, 75))
player_boy = pygame.image.load(resource_path('player_male.png'))
player_boy = pygame.transform.scale(player_boy, (75, 75))

dead_ostrich_img = pygame.image.load(resource_path('ostritchdead.png'))
dead_ostrich_img = pygame.transform.scale(dead_ostrich_img, (75, 75))
enemy_frame1 = pygame.image.load(resource_path('ostritch1.png'))
enemy_frame2 = pygame.image.load(resource_path('ostritch2.png'))
enemy_frame1 = pygame.transform.scale(enemy_frame1, (75, 75))
enemy_frame2 = pygame.transform.scale(enemy_frame2, (75, 75))

arrow_original = pygame.image.load(resource_path('arrow-removebg.png'))
arrow_original = pygame.transform.scale(arrow_original, (40, 15))

boss_frame1 = pygame.image.load(resource_path('lion11.png'))
boss_frame2 = pygame.image.load(resource_path('lion22.png'))
boss_frame1 = pygame.transform.scale(boss_frame1, (150, 150))
boss_frame2 = pygame.transform.scale(boss_frame2, (150, 150))
dead_boss_img = pygame.image.load(resource_path('lion dead.png'))
dead_boss_img = pygame.transform.scale(dead_boss_img, (150, 150))

# ## PART 4: AUDIO ##
pygame.mixer.music.load(resource_path('background music.mp3'))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.4)
walk_sound = pygame.mixer.Sound(resource_path('foot step.flac'))
shoot_sound = pygame.mixer.Sound(resource_path('shoot.ogg'))
hit_sound = pygame.mixer.Sound(resource_path('arrow impact.mp3'))
ostrich_spawn_sound = pygame.mixer.Sound(resource_path('ostrich1.mp3'))
game_over_sound = pygame.mixer.Sound(resource_path('talo ka boii.mp3'))
lion_sound = pygame.mixer.Sound(resource_path('lion2.mp3'))
lion_channel = pygame.mixer.Channel(5)

# ## PART 5: VARIABLES ##
state = "SELECT"
enemies, dead_enemies, arrows, dead_bosses = [], [], [], []
player_x, player_Y = 650, 350
angle, arrow_speed, score = 0, 15, 0
spawn_cooldown, enemy_timer = 100, 0
gamerun, is_game_over, walk_delay = True, False, 0
player_img = None

# Boss Specifics
boss_active = False
boss_hp, boss_x, boss_y, boss_angle = 20, 0, 0, 0
boss_anim = 0  # Tracks animation timing
boss_frame = 0  # Switches between 0 and 1
boss_milestones = [20, 40, 60, 80, 100]

man_rect = pygame.Rect(400, 250, 200, 200)
woman_rect = pygame.Rect(800, 250, 200, 200)

# ## PART 6: MAIN LOOP ##
while gamerun:
    screen.blit(bg_img, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamerun = False

        if state == "SELECT":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if man_rect.collidepoint(mouse_pos):
                    player_img, state = player_boy, "GAME"
                if woman_rect.collidepoint(mouse_pos):
                    player_img, state = player_girl, "GAME"

        elif state == "GAME":
            if not is_game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    arrows.append([player_x + 37, player_Y + 37, angle])
                    shoot_sound.play()
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    player_x, player_Y = 650, 350
                    enemies, dead_enemies, arrows, dead_bosses = [], [], [], []
                    score, enemy_timer, spawn_cooldown = 0, 0, 100
                    boss_active, is_game_over = False, False
                    state = "SELECT"
                    pygame.mixer.music.play(-1)

    if state == "SELECT":
        overlay = pygame.Surface((1400, 700))
        overlay.set_alpha(150);
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        title = menu_font.render("SELECT YOUR HUNTER", True, (255, 255, 255))
        screen.blit(title, (450, 100))
        screen.blit(man_btn_img, (man_rect.x, man_rect.y))
        screen.blit(woman_btn_img, (woman_rect.x, woman_rect.y))
        if man_rect.collidepoint(mouse_pos): pygame.draw.rect(screen, (255, 255, 255), man_rect, 3)
        if woman_rect.collidepoint(mouse_pos): pygame.draw.rect(screen, (255, 255, 255), woman_rect, 3)

    elif state == "GAME":
        if not is_game_over:
            keys = pygame.key.get_pressed()
            moving = False
            if keys[pygame.K_a]: player_x -= 5; angle = 180; moving = True
            if keys[pygame.K_d]: player_x += 5; angle = 0; moving = True
            if keys[pygame.K_w]: player_Y -= 5; angle = 90; moving = True
            if keys[pygame.K_s]: player_Y += 5; angle = 270; moving = True

            player_x = max(0, min(player_x, 1325));
            player_Y = max(0, min(player_Y, 625))

            if moving and walk_delay <= 0:
                walk_sound.play();
                walk_delay = 20
            if walk_delay > 0: walk_delay -= 1

            if score in boss_milestones and not boss_active:
                boss_active = True;
                boss_hp = 20
                boss_x, boss_y = random.choice([-150, 1450]), random.choice([-150, 750])
                lion_channel.play(lion_sound);
                boss_milestones.remove(score)

            enemy_timer += 1
            if enemy_timer > spawn_cooldown:
                side = random.randint(0, 3)
                if side == 0:
                    ex, ey = random.randint(0, 1400), -70
                elif side == 1:
                    ex, ey = random.randint(0, 1400), 770
                elif side == 2:
                    ex, ey = -70, random.randint(0, 700)
                else:
                    ex, ey = 1470, random.randint(0, 700)
                enemies.append({'x': ex, 'y': ey, 'health': 2, 'angle': 0, 'anim': 0, 'frame': 0})
                enemy_timer = 0;
                ostrich_spawn_sound.play()

            for e in enemies:
                if e['x'] < player_x:
                    e['x'] += 2
                elif e['x'] > player_x:
                    e['x'] -= 2
                if e['y'] < player_Y:
                    e['y'] += 2
                elif e['y'] > player_Y:
                    e['y'] -= 2

                dx, dy = player_x - e['x'], player_Y - e['y']
                e['angle'] = math.degrees(math.atan2(-dy, dx))
                e['anim'] += 1
                if e['anim'] > 10: e['frame'] = 1 if e['frame'] == 0 else 0; e['anim'] = 0

                if pygame.Rect(player_x, player_Y, 60, 60).colliderect(pygame.Rect(e['x'], e['y'], 60, 60)):
                    is_game_over = True

            if boss_active:
                if boss_x < player_x:
                    boss_x += 1.5
                elif boss_x > player_x:
                    boss_x -= 1.5
                if boss_y < player_Y:
                    boss_y += 1.5
                elif boss_y > player_Y:
                    boss_y -= 1.5
                bdx, bdy = player_x - boss_x, player_Y - boss_y
                boss_angle = math.degrees(math.atan2(-bdy, bdx))

                # Boss Animation Toggle
                boss_anim += 1
                if boss_anim > 10:
                    boss_frame = 1 if boss_frame == 0 else 0
                    boss_anim = 0

                if pygame.Rect(player_x, player_Y, 70, 70).colliderect(pygame.Rect(boss_x, boss_y, 130, 130)):
                    is_game_over = True

            if is_game_over:
                pygame.mixer.stop();
                pygame.mixer.music.stop();
                game_over_sound.play()

            for a in arrows[:]:
                if a[2] == 0:
                    a[0] += arrow_speed
                elif a[2] == 180:
                    a[0] -= arrow_speed
                elif a[2] == 90:
                    a[1] -= arrow_speed
                elif a[2] == 270:
                    a[1] += arrow_speed

                if boss_active and pygame.Rect(a[0], a[1], 40, 15).colliderect(pygame.Rect(boss_x, boss_y, 150, 150)):
                    if a in arrows: arrows.remove(a)
                    boss_hp -= 1;
                    hit_sound.play()
                    if boss_hp <= 0:
                        boss_active = False;
                        score += 25
                        dead_bosses.append({'x': boss_x, 'y': boss_y, 'angle': boss_angle, 'timer': 180})

                for e in enemies[:]:
                    if pygame.Rect(a[0], a[1], 40, 15).colliderect(pygame.Rect(e['x'], e['y'], 75, 75)):
                        if a in arrows: arrows.remove(a)
                        e['health'] -= 1;
                        hit_sound.play()
                        if e['health'] <= 0:
                            score += 1;
                            dead_enemies.append({'x': e['x'], 'y': e['y'], 'timer': 30})
                            enemies.remove(e)

        # ## RENDERING ##
        for db in dead_bosses[:]:
            screen.blit(pygame.transform.rotate(dead_boss_img, db['angle']), (db['x'], db['y']))
            db['timer'] -= 1
            if db['timer'] <= 0: dead_bosses.remove(db)
        for d in dead_enemies[:]:
            screen.blit(dead_ostrich_img, (d['x'], d['y']))
            d['timer'] -= 1
            if d['timer'] <= 0: dead_enemies.remove(d)

        for e in enemies:
            img = enemy_frame1 if e['frame'] == 0 else enemy_frame2
            rotated_enemy = pygame.transform.rotate(img, e['angle'] + 90)
            new_rect = rotated_enemy.get_rect(center=img.get_rect(topleft=(e['x'], e['y'])).center)
            screen.blit(rotated_enemy, new_rect.topleft)

        if boss_active:
            cur_boss = boss_frame1 if boss_frame == 0 else boss_frame2
            rot_b = pygame.transform.rotate(cur_boss, boss_angle)
            new_rect_b = rot_b.get_rect(center=cur_boss.get_rect(topleft=(boss_x, boss_y)).center)
            screen.blit(rot_b, new_rect_b.topleft)
            pygame.draw.rect(screen, (200, 0, 0), (boss_x, boss_y - 20, 150, 10))
            pygame.draw.rect(screen, (0, 255, 0), (boss_x, boss_y - 20, boss_hp * 7.5, 10))

        for a in arrows:
            screen.blit(pygame.transform.rotate(arrow_original, a[2]), (a[0], a[1]))

        if not is_game_over:
            rot_p = pygame.transform.rotate(player_img, angle)
            new_rect_p = rot_p.get_rect(center=player_img.get_rect(topleft=(player_x, player_Y)).center)
            screen.blit(rot_p, new_rect_p.topleft)

        screen.blit(score_font.render(f"Score: {score}", True, (255, 255, 255)), (20, 20))
        if is_game_over:
            screen.blit(game_over_font.render("GAME OVER", True, (255, 0, 0)), (450, 300))
            screen.blit(score_font.render("Press 'R' to Restart", True, (255, 255, 255)), (550, 500))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()