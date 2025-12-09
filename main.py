import pygame
import config
import components
import population

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
    while True:

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