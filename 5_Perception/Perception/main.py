# Some resource that helped a lot :)
# http://opengameart.org/content/fantasy-ui-button
# http://opengameart.org/content/ui-button
# http://opengameart.org/content/brick-wall
# http://opengameart.org/content/menu-loop

from kivy.utils import platform
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock #clock to schedule the game update
from kivy.storage.jsonstore import JsonStore
from os.path import join
import random

if platform() == "android":
    from jnius import cast
    from jnius import autoclass
    from revmob import RevMob as revmob


#here we create a custom class called ImageButton. It's a image, however with
# some button properties. We use this class to use the on_press event
class ImageButton(ButtonBehavior, Image):
    pass

# This is the App screen, all game scenes(menu and the game) extends this object
class AppScreen(FloatLayout):
    # MainApp referece, so we can call some functions provided by this object
     app = ObjectProperty(None)

# This is our menu screen.
class MenuScreen(AppScreen):
    def __init__(self, app): #init the object, receiving the MainApp instance
        super(MenuScreen, self).__init__()
        self.app = app # get the MainApp reference

    # switch to the GameScreen
    def new_game(self):
        self.app.open_screen('game')

    # just close our application
    def exit_game(self):
        exit(0)

    # App share with Android
    # It will open an intent to share a message
    def share(self):
        if platform() == 'android': #check if the app is on Android
            # read more here: http://developer.android.com/training/sharing/send.html
            PythonActivity = autoclass('org.renpy.android.PythonActivity') #request the activity instance
            Intent = autoclass('android.content.Intent') # get the Android Intend class

            String = autoclass('java.lang.String') # get the Java object

            intent = Intent() # create a new Android Intent
            intent.setAction(Intent.ACTION_SEND) #set the action
            # to send a message, it need to be a Java char array. So we use the cast to convert and Java String to a Java Char array
            intent.putExtra(Intent.EXTRA_SUBJECT, cast('java.lang.CharSequence', String('Fast Perception')))
            intent.putExtra(Intent.EXTRA_TEXT, cast('java.lang.CharSequence', String('Wow, I just scored %d on Fast Perception. Check this game: https://play.google.com/store/apps/details?id=com.aronbordin.fastperception' % (self.best_score))))

            intent.setType('text/plain') #text message

            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            currentActivity.startActivity(intent) # show the intent in the game activity

    # will be called when our screen be displayed
    def run(self):
        self.best_score = self.app.store.get('score')['best'] # get the best score saved
        self.ids.label_best.text = 'Best score: ' + str(self.best_score) #show it
        if platform() == 'android': # if we are using android, we can show an ADs
            if(random.randint(0, 5) == 1): # get a random and show a ads in the menu
                revmob.show_popup()

#Our game screen, where everything happens :)
class GameScreen(AppScreen):
    def __init__(self, app): #init the object, receiving the MainApp instance
        super(GameScreen, self).__init__()
        self.app = app
        self.init()

    #initialize defaults values to start a new game
    def init(self):
        self.level = 1 # the current level
        self.best_level = self.app.store.get('score')['best'] # best level
        self.game_grid = self.ids.game_grid # the game grid widget instance
        self.label_level = self.ids.label_level # the label widget to show the current level
        self.grid_size = 2 #we are using a grid layout to show our blocks, the fist level has a 2x2 grid
        self.last_id = None #last btn blinked
        self.remain_interaction = 4 # number of blinks before turn off
        self.can_click = False # if the user can choose a block. Only true while not blinking

    # called when the game scene be displayed
    def run(self):
        self.start_game()

    # start a new game round
    def start_game(self, dt = None):
        self.can_click = False #while playing, user cannot choose a block
        self.ids.label_last_block.text = "" # clear the id of last blinked block
        self.check_best() #check if user has a new highscore
        self.ids.label_best.text = 'Best level: ' + str(self.best_level) # show the best score in the screen
        self.ids.restart.pos_hint = {'x': -1, 'y': 0.025} #hide the restart button
        Clock.unschedule(self.update) # stop updating the game screen

        self.label_level.text = 'Level: ' + str(self.level) #show the current level

        self.remain_interaction = random.randint(2 + self.level/2, self.level*2) #generate a random number of interactions

        self.draw_screen() #show the blocks in the screen

        # here we set the speed of the animation
        if self.level < 10:
            interval = 1 - self.level*0.1
        else:
            interval = 0.1 - self.level*0.001

        #update the screen using the interval calculated above
        Clock.schedule_interval(self.update, interval)

    #each update a different block will blink
    def update(self, dt):
        # when last_id is not none there is a green block in the screen
        if(self.last_id is not None):
            self.game_grid.ids.get(self.last_id).source = "res/block.png" #turn off the block

        if self.remain_interaction == 0: #if executed all interactions
            Clock.unschedule(self.update) #stop updating the screen
            self.ids.label_last_block.text = 'Click in the last block that blinked' #ask user to click in a block
            self.can_click = True # allow the click
            return

        #if we can still blinking:

        id = 'btn_' + str(random.randint(0, self.grid_size*self.grid_size-1)) #generate a random int to blink a random block
        self.game_grid.ids.get(id).source="res/block_blink.png" #make this block border green
        self.last_id = id # save the id of the green block
        self.remain_interaction -= 1

    # draw the blocks in the screen
    def draw_screen(self):
        self.game_grid.clear_widgets() # this command remove all children(blocks) from the game_grid

        # according to the level, we can change the size of the grid
        if(self.level < 3):
            self.game_grid.cols = 2
            self.game_grid.rows = 2
            self.grid_size = 2
        elif self.level < 5:
            self.game_grid.cols = 3
            self.game_grid.rows = 3
            self.grid_size = 3
        elif self.level < 10:
            self.game_grid.cols = 4
            self.game_grid.rows = 4
            self.grid_size = 4
        elif self.level < 15:
            self.game_grid.cols = 5
            self.game_grid.rows = 5
            self.grid_size = 5
        elif self.level < 20:
            self.game_grid.cols = 6
            self.game_grid.rows = 6
            self.grid_size = 6

        # this is a block in KV lang.
        btn_str = '''
ImageButton:
    source: "res/block.png"
    allow_stretch: True
    keep_ratio: False'''


        # generate a grid_sizeXgrid_size grid
        for i in range(0, self.grid_size*self.grid_size):
            btn = Builder.load_string(btn_str) # create a ImageButton from the string
            id = 'btn_' + str(i)
            btn.id = id # set the button ID
            self.game_grid.ids[id] = btn #add this button to the list of children of the GameGrid
            btn.bind(on_press=self.on_btn_press) # bind the press event
            self.game_grid.add_widget(btn) # and show this button on the grid

    # grid button event
    def on_btn_press(self, btn):
        if(self.can_click is True): # check if the user can click
            self.can_click = False
            self.game_grid.ids.get(self.last_id).source = 'res/block_blink.png' # blink the clicked button
            if(btn.id == self.last_id): # if the clicked button was the last one to blink
                self.ids.label_last_block.text = 'Right!' # the user was right
                self.level += 1 #user can go to the next level
                Clock.schedule_once(self.start_game, 1) #wait a second and start the next level
            else:
                self.ids.label_last_block.text = 'Wrong :(' #user was wrong
                self.ids.restart.pos_hint = {'x': 0.75, 'y': 0.025} #the restart button is visible now

    # compare the current level with the highscore
    def check_best(self):
        if self.level > self.best_level:
            self.best_level = self.level
            self.app.store.put('score', best=self.level) #save the best score. We are saving it in the key 'score', in the child 'best'

    # open the menu screen
    def go_menu(self):
        Clock.unschedule(self.update)
        self.init()
        self.app.open_screen('menu')

    # restart the first level
    def restart(self):
        Clock.unschedule(self.update)
        self.init()
        self.start_game()


# This is the main app
# This object create our application and manage all game screens
class MainApp(App):
    #create the application screens
    def build(self):

        data_dir = getattr(self, 'user_data_dir') #get a writable path to save our score
        self.store = JsonStore(join(data_dir, 'score.json')) # create a JsonScore file in the available location

        if(not self.store.exists('score')): # if there is no file, we need to save the best score as 1
            self.store.put('score', best=1)

        if platform() == 'android': # if we are on Android, we can initialize the ADs service
            revmob.start_session('54c247f420e1fb71091ad44a')

        self.screens = {} # list of app screens
        self.screens['menu'] = MenuScreen(self) #self the MainApp instance, so others objects can change the screen
        self.screens['game'] = GameScreen(self)
        self.root = FloatLayout()

        self.open_screen('menu')

        self.sound = SoundLoader.load('res/background.mp3') # open the background music
        # kivy support music loop, but it was not working on Android. I coded in a different way to fix it
        # but if fixed, we can just set the loop to True and call the play(), so it'll auto repeat
        # self.sound.loop = True It # was not working on android, so I wrote the following code:
        self.sound.play() # play the sound
        Clock.schedule_interval(self.check_sound, 1) #every second force the music to be playing

        return self.root

    # play the sound
    def check_sound(self, dt = None):
        self.sound.play()

    # when the app is minimized on Android
    def on_pause(self):
        self.sound.stop() # the stop the sound
        Clock.unschedule(self.check_sound)
        if platform() == 'android': #if on android, we load an ADs and show it
            revmob.show_popup()
        return True

    # when the app is resumed
    def on_resume(self):
        self.sound.play() # we start the music again
        Clock.schedule_interval(self.check_sound, 1)

    # show a new screen.
    def open_screen(self, name):
        self.root.clear_widgets() #remove the current screen
        self.root.add_widget(self.screens[name]) # add a new one
        self.screens[name].run() # call the run method from the desired screen

if __name__ == '__main__':
    MainApp().run()