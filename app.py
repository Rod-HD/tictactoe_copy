# app.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.button import Button

from board import Board
from controller import GameController
from themes import Theme
from layout import TicTacToeLayout
from homescreen import HomeScreen

# ------------------------------------------------------------------ #
def create_game(mode: str = "friend", difficulty: str = "medium", element: str = "wood") -> TicTacToeLayout:
    board      = Board()
    controller = GameController(board, mode, difficulty)
    theme      = Theme(element)
    return TicTacToeLayout(controller, theme)

# ------------------------------------------------------------------ #
class GameScreen(Screen):
    """Screen that contains the game."""
    
    def __init__(self, mode: str, difficulty: str = None, **kwargs):
        super().__init__(**kwargs)
        self.mode = mode
        self.difficulty = difficulty
        self.game_widget = create_game(mode, difficulty)
        self.add_widget(self.game_widget)
        
        # Add back button
        self.back_btn = Button(
            text='Back to Menu',
            size_hint=(0.2, 0.05),
            pos_hint={'x': 0, 'top': 1}
        )
        self.back_btn.bind(on_release=self.go_back)
        self.add_widget(self.back_btn)
    
    def go_back(self, instance):
        """Return to home screen."""
        app = App.get_running_app()
        if app:
            app.go_home()

# ------------------------------------------------------------------ #
class TicTacToeApp(App):
    def build(self):
        # Create screen manager
        self.sm = ScreenManager(transition=FadeTransition())
        
        # Add home screen
        self.home_screen = HomeScreen(name='home')
        self.sm.add_widget(self.home_screen)
        
        return self.sm
    
    def start_game(self, mode: str, difficulty: str = None):
        """Start a new game with the specified mode."""
        # Remove old game screen if exists
        if self.sm.has_screen('game'):
            old_screen = self.sm.get_screen('game')
            # Stop sounds before removing
            if hasattr(old_screen, 'game_widget') and hasattr(old_screen.game_widget, '_sounds'):
                if old_screen.game_widget._sounds.bg:
                    old_screen.game_widget._sounds.bg.stop()
            self.sm.remove_widget(old_screen)
        
        # Create new game screen
        game_screen = GameScreen(mode, difficulty, name='game')
        self.sm.add_widget(game_screen)
        
        # Switch to game screen
        self.sm.current = 'game'
    
    def go_home(self):
        """Return to home screen."""
        # Stop any playing sounds
        if self.sm.has_screen('game'):
            game_screen = self.sm.get_screen('game')
            if hasattr(game_screen, 'game_widget') and hasattr(game_screen.game_widget, '_sounds'):
                if game_screen.game_widget._sounds.bg:
                    game_screen.game_widget._sounds.bg.stop()
        
        self.sm.current = 'home'

    def on_stop(self):
        # Clean up background music if still playing
        if self.sm.current == 'game' and self.sm.has_screen('game'):
            game_screen = self.sm.get_screen('game')
            if hasattr(game_screen, 'game_widget') and hasattr(game_screen.game_widget, '_sounds'):
                if game_screen.game_widget._sounds.bg:
                    game_screen.game_widget._sounds.bg.stop()
