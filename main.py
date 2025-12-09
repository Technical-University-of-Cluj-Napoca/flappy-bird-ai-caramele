import pygame
import config
import components
import population
import button
import player

pygame.init()
clock = pygame.time.Clock()
population = population.Population(100)

def scroll_ground(screen, img, y, speed, pos):
    pos -= speed
    if pos <= -img.get_width():
        pos = 0
    screen.blit(img, (pos, y))
    screen.blit(img, (pos + img.get_width(), y))
    return pos


def title_screen():
    manual_btn = button.Button(150, 350, 250, 60, "Manual Mode")
    auto_btn = button.Button(150, 430, 250, 60, "Autonomous Mode")
    score_btn = button.Button(150, 510, 250, 60, "High score")
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if manual_btn.handle_event(event):
                return "manual"
            if auto_btn.handle_event(event):
                return "auto"
            if score_btn.handle_event(event):
                print("score todo")
        
        config.screen.blit(config.BACKROUND_IMG, (0,0))
        config.screen.blit(config.GROUND_IMG, (0, config.GROUND_Y))
       

        manual_btn.draw(config.screen)
        auto_btn.draw(config.screen)
        score_btn.draw(config.screen)

        title = config.TITLE_FONT.render("FLAPPY BIRD", True, (255,255,255))
        title_rect = title.get_rect(center=(config.SCREEN_WIDTH//2, 150))
        config.screen.blit(title, title_rect)

        copyright_font = pygame.font.SysFont("Arial", 20)
        copyright_text = copyright_font.render("© 2025 Team Caramele", True, (255, 255, 255))
        copyright_rect = copyright_text.get_rect(center=(config.SCREEN_WIDTH//2, 600))
        config.screen.blit(copyright_text, copyright_rect)

        bird_x = title_rect.right + 10
        bird_y = title_rect.centery - 25
        bird = player.Bird(bird_x, bird_y)
        bird.draw(config.screen)
        pygame.display.flip()
        clock.tick(60)

def tutorial_screen(mode):
   
    bird = player.Bird(100, config.SCREEN_HEIGHT // 2)
    ground_x = 0

    while True:
        #keep running until player starts game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        config.screen.blit(config.BACKROUND_IMG, (0,0))
        ground_x = scroll_ground(config.screen,
                                        config.GROUND_IMG,
                                        config.GROUND_Y,
                                        config.GROUND_SPEED,
                                        ground_x
                                        )
    
        bird.flop()
        bird.draw(config.screen)

        tutorial_font = pygame.font.SysFont("Arial", 30)
        if mode == "manual":
            text = tutorial_font.render("Press SPACE to start playing", True, (255, 255, 255))
        if mode == "auto":
            text = tutorial_font.render("Press SPACE and watch Faby play", True, (255, 255, 255))
        text_rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, 200))
        config.screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)

    

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
def generate_pipes():
    config.pipes.append(components.Pipes(config.SCREEN_WIDTH))
def main():

    pipes_spawn_time = 10
    ground_x = 0
    mode = title_screen()
    tutorial_screen(mode)
    config.pipes.clear()
    manual_bird = player.ManualBird(100,100)
    while True:

        if mode == "manual":
            
            config.screen.blit(config.BACKROUND_IMG, (0,0))

            ground_x = scroll_ground(config.screen,
                                    config.GROUND_IMG,
                                    config.GROUND_Y,
                                    config.GROUND_SPEED,
                                    ground_x
                                    )

            if pipes_spawn_time <= 0:
                generate_pipes()
                pipes_spawn_time = 200
            pipes_spawn_time -= 1

            for pipe in config.pipes:
                pipe.draw(config.screen)
                pipe.update()
                if pipe.off_screen:
                    config.pipes.remove(pipe)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    manual_bird.jump()
            manual_bird.update()
            manual_bird.draw(config.screen)

            if  manual_bird.hit_pipe() or manual_bird.hit_ground():
                print("Game Over")
                return
            

        if mode == "auto":
            quit_game()
            config.screen.blit(config.BACKROUND_IMG, (0,0))

            ground_x = scroll_ground(config.screen,
                                    config.GROUND_IMG,
                                    config.GROUND_Y,
                                    config.GROUND_SPEED,
                                    ground_x
                                    )

            #config.screen.blit(config.GROUND_IMG, (0, config.GROUND_Y))
            if pipes_spawn_time <= 0:
                generate_pipes()
                pipes_spawn_time = 200
            pipes_spawn_time -= 1

            for pipe in config.pipes:
                pipe.draw(config.screen)
                pipe.update()
                if pipe.off_screen:
                    config.pipes.remove(pipe)

            if not population.extinct():
                population.update_live_players()
            else:
                pass

        clock.tick(60)
        pygame.display.flip()
main()