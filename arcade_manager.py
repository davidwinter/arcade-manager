#!/usr/bin/env python
 
import gtk
import os
import sys

class ArcadeManager:

    def __init__(self):

        """Must ensure that emulators are on system path env variable"""
        self.emulator = ('dgen', 'Fusion')[sys.platform == 'win32']
        print self.emulator

        """Get ROM Path"""
        if '-r' in sys.argv:
            self.rom_path = sys.argv[sys.argv.index('-r') + 1]
            print self.rom_path
        else:
            self.rom_path = 'roms/'
            print 'Using default roms/'

        window = gtk.Window()
        vbox = gtk.VBox()
        window.add(vbox)

        self.gameChoice = gtk.combo_box_new_text()
        
        self.games = self.get_games()
        for game in self.games:
            self.gameChoice.append_text(game)
            print self.games[game]

        self.gameChoice.set_active(0)
        self.gameChoice.connect('key_press_event', self.key_press)
        vbox.add(self.gameChoice)

        button = gtk.Button()
        button.set_label("Play!")
        button.connect('clicked', self.play)
        vbox.add(button)
        
        window.connect('destroy', self.quit)
        window.show_all()

        if '-f' in sys.argv:
            window.fullscreen()

    def quit(self, extra):
        gtk.main_quit()

    def key_press(self, widget, key):
        key = gtk.gdk.keyval_name(key.keyval)
        if key == '1':
            self.play_selected_game()

    def get_games(self):
        dict = {}
        for file in os.listdir(self.rom_path):
            name = file.replace('.bin', '').replace('_', ' ')
            dict[name] = file

        return dict
    
    def play(self, button):
        self.play_selected_game()

    def play_selected_game(self):
        model = self.gameChoice.get_model()
        index = self.gameChoice.get_active()

        if index >= 0:
            game = self.games[model[index][0]]
            print game
            os.system(self.emulator + " " + self.rom_path + game)

if __name__ == "__main__":
  app = ArcadeManager()
  gtk.main()

