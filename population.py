import player
import config

class Population:
    def __init__(self, size):
        self.players = []
        self.size = size
        for i in range(size):
            self.players.append(player.Player())

    def update_live_players(self):
        for p in self.players:
            if p.alive:
                p.think()
                p.draw(config.screen)
                p.update(config.ground)
    def extinct (self):
        extinct = True
        for p in self.players:
            if p.alive:
                extinct = False
                break
        return extinct