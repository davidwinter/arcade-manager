#!/usr/bin/env python
 
import gtk
import gtk.glade
import os
import sys

class ArcadeView:

    def __init__(self):

        self.wTree = gtk.glade.XML('arcade-manager.glade')
        
        self.window = self.wTree.get_widget('window')
        self.games_list = self.wTree.get_widget('games_list')

        self.window.show_all()

    def build_games_list(self, games):

        self.games_list_store = gtk.ListStore(str)
        
        for game in games:
            self.games_list_store.append([game])

        self.games_column = gtk.TreeViewColumn('Games')
        self.text_renderer = gtk.CellRendererText()
        self.games_column.pack_start(self.text_renderer, True)
        self.games_column.set_attributes(self.text_renderer, text = 0)
        self.games_list.set_model(self.games_list_store)
        self.games_list.append_column(self.games_column)

    def get_game_selection(self):
        (model, iterator) = self.games_list.get_selection().get_selected()
        
        if iterator:
            return model.get_value(iterator, 0)   

class ArcadeController:

    def __init__(self):
        
        # Program arguments
        if '-r' in sys.argv:
            rom_path = sys.argv[sys.argv.index('-r') + 1]
        else:
            rom_path = 'roms/'
        
        self.environment = ArcadeEnvironment(rom_path)
        
        self.view = ArcadeView()
        
        self.view.window.connect('destroy', self.quit)
        self.view.games_list.connect('key_release_event', 
            self.games_list_key_release)

        if '-f' in sys.argv:
            self.view.window.fullscreen()
        
        game_names = []
        
        self.games = self.environment.get_games()
        
        for game in self.games:
            game_names.append(game)
        
        self.view.build_games_list(game_names)

    def games_list_key_release(self, widget, key):
        key = gtk.gdk.keyval_name(key.keyval)
                
        if key == '1':
            # Play game
            game_file = self.games[self.view.get_game_selection()]
            self.play_game(game_file)
        
    def quit(self, window):
        gtk.main_quit()

    def play_game(self, game):
        os.system(self.environment.emulator + ' ' +
                    self.environment.rom_path + game)

class ArcadeEnvironment:

    def __init__(self, rom_path = 'roms/'):
        self.__determine_os()
        self.__determine_emulator()
        self.rom_path = rom_path
        
    def __determine_os(self):
        
        if sys.platform == 'win32':
            self.os = 'Windows'
        elif sys.platform == 'linux2':
            self.os = 'Linux'
        elif sys.platform == 'darwin':
            self.os = 'Mac'

    def __determine_emulator(self):
        
        if self.os == 'Windows':
            self.emulator = 'Fusion'
        elif self.os == 'Linux':
            self.emulator = 'dgen'
        elif self.os == 'Mac':
            self.emulator = 'open -a Genesis\ Plus'

    def get_games(self):
        dict = {}
        for file in os.listdir(self.rom_path):
            name = file.replace('.bin', '').replace('_', ' ')
            dict[name] = file

        return dict

if __name__ == "__main__":
  app = ArcadeController()
  gtk.main()

