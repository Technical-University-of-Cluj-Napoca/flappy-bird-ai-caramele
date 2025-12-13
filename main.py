import pygame
import config
import components
import population
import button
import player
from datetime import datetime

pygame.init()
clock = pygame.time.Clock()
population = population.Population(50)
auto_score = 0

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
                return "score"

        config.screen.blit(config.BACKROUND_IMG, (0,0))
        config.screen.blit(config.GROUND_IMG, (0, config.GROUND_Y))


        manual_btn.draw(config.screen)
        auto_btn.draw(config.screen)
        score_btn.draw(config.screen)

        title = config.TITLE_FONT.render("FLAPPY BIRD", True, (255,255,255))
        title_rect = title.get_rect(center=(config.SCREEN_WIDTH//2, 150))
        config.screen.blit(title, title_rect)


        year = datetime.now().year
        s = str(year)
        copyright_font = pygame.font.Font("assets/fonts/LuckiestGuy-Regular.ttf", 18)
        copyright_text = copyright_font.render("©" + s + " Team Caramele", True, (255, 255, 255))
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

        tutorial_font = pygame.font.Font("assets/fonts/LuckiestGuy-Regular.ttf", 30)
        if mode == "manual":
            text = tutorial_font.render("Press SPACE to start playing", True, (255, 255, 255))
        if mode == "auto":
            text = tutorial_font.render("Press SPACE and watch Faby play", True, (255, 255, 255))
        text_rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, 200))
        config.screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)

def display_score(score):
    font =pygame.font.Font("assets/fonts/LuckiestGuy-Regular.ttf", 30)
    score_txt = font.render("Score: " + str(score), True, (255, 255, 255))
    score_rect = score_txt.get_rect(center=(config.SCREEN_WIDTH // 2, 50))
    config.screen.blit(score_txt, score_rect)

def display_generation():
    font =pygame.font.Font("assets/fonts/LuckiestGuy-Regular.ttf", 30)
    generation_txt = font.render("Generation: " + str(population.generation), True, (255, 255, 255))
    generation_rect = generation_txt.get_rect(bottomleft=(20, config.SCREEN_HEIGHT - 20))
    config.screen.blit(generation_txt, generation_rect)


#display the highschore window
def highscore_window():
    highscore = config.HIGH_SCORE

    display = True#flag to check if to display window
    font_title = pygame.font.Font("assets/fonts/LuckiestGuy-Regular.ttf", 50)
    font_score = pygame.font.Font("assets/fonts/LuckiestGuy-Regular.ttf", 30)
    while display:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                display = False

        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0,0,0))
        config.screen.blit(overlay, (0,0))

        title_text = font_title.render("HIGH SCORE", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(config.SCREEN_WIDTH // 2, 200))
        config.screen.blit(title_text, title_rect)

        score_text = font_score.render(str(highscore), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(config.SCREEN_WIDTH // 2, 300))
        config.screen.blit(score_text, score_rect)

        instr_text = font_score.render("Press SPACE to continue", True, (200, 200, 200))
        instr_rect = instr_text.get_rect(center=(config.SCREEN_WIDTH // 2, 400))
        config.screen.blit(instr_text, instr_rect)

        pygame.display.flip()


def gameover_screen(score):

    play_again = button.Button(150, 430, 250, 60, "Play again")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if play_again.handle_event(event):
                return True

        config.screen.blit(config.BACKROUND_IMG, (0,0))
        config.screen.blit(config.GROUND_IMG, (0, config.GROUND_Y))


        play_again.draw(config.screen)

        title = config.TITLE_FONT.render("Game over", True, (255,255,255))
        title_rect = title.get_rect(center=(config.SCREEN_WIDTH//2, 150))
        config.screen.blit(title, title_rect)
        display_score(score)

        pygame.display.flip()
        clock.tick(60)




def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
def generate_pipes():
    pipe = components.Pipes(config.SCREEN_WIDTH)
    pipe.counted = False
    config.pipes.append(pipe)



def main():
    global auto_score
    score = 0
    pipes_spawn_time = 10
    ground_x = 0
    while True:
        mode = title_screen()
        if mode == "score":
            highscore_window()
            continue
        else:
            break
    running = True
    tutorial_screen(mode)
    config.pipes.clear()
    manual_bird = player.ManualBird(100,100)
    while running:



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
                pipes_spawn_time = 100
            pipes_spawn_time -= 1

            for pipe in config.pipes:
                pipe.draw(config.screen)
                if score >= 5:
                    pipe.move_gap = True
                pipe.update()
                if pipe.off_screen:
                    config.pipes.remove(pipe)

                if not pipe.passed and manual_bird.x > pipe.x + pipe.width:
                    pipe.passed = True
                    score += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    manual_bird.jump()
            manual_bird.update()
            manual_bird.draw(config.screen)
            display_score(score)

            if  manual_bird.hit_pipe() or manual_bird.hit_ground():


                if score > config.HIGH_SCORE:
                    config.save_score(score)

                play_again = gameover_screen(score)

                if play_again:
                    score = 0
                    pipes_spawn_time = 10
                    ground_x = 0
                    manual_bird = player.ManualBird(100, config.SCREEN_HEIGHT // 2)
                    config.pipes.clear()
                    continue
                else:
                    running = False
                return
                pygame.display.flip()
                clock.tick(60)


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
                pipes_spawn_time = 100
            pipes_spawn_time -= 1

            for pipe in config.pipes:
                pipe.draw(config.screen)
                if auto_score >= 5:
                    pipe.move_gap = True
                pipe.update()
                if pipe.off_screen:
                    config.pipes.remove(pipe)

                if not pipe.counted and pipe.x+pipe.width <= 50:
                    pipe.counted = True
                    auto_score += 1

            if not population.extinct():
                population.update_live_players()
            else:
                config.pipes.clear()
                population.natural_selection()
                auto_score = 0

            display_score(auto_score)
            display_generation()

        clock.tick(60)
        pygame.display.flip()
main()