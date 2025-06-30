# app.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.button import Button

from board import Board
from controller import GameController
from themes import Theme
from layout import TicTacToeLayout
from homescreen import HomeScreen

from utils import style_round_button

ELEMENTS = ["metal", "wood", "water", "fire", "earth"]
# ------------------------------------------------------------------ #
def create_game(mode="friend",
                difficulty="medium",
                element="wood"):            # vẫn giữ tham số element
    board      = Board()
    controller = GameController(board, mode, difficulty)
    theme      = Theme(element)
    return TicTacToeLayout(controller, theme)

# ------------------------------------------------------------------ #
class GameScreen(Screen):
    """Screen that contains the game."""
    
    def __init__(self, mode: str,
                 difficulty: str = None,
                 element: str = "wood",    # NEW
                 **kwargs):
        super().__init__(**kwargs)
        self.mode = mode
        self.difficulty = difficulty
        self.game_widget = create_game(mode, difficulty)
        self.add_widget(self.game_widget)
        self.game_widget = create_game(mode, difficulty, element)
        # Add back button
        self.back_btn = Button(
            text='Back to Menu',
            size_hint=(0.22, 0.07),             # rộng & cao linh hoạt
            pos_hint={'x': 0.02, 'top': 0.98},
            halign='center', valign='middle',
            shorten=True, shorten_from='right'
)
        self.back_btn.bind(size=self._fit_back_btn)
        self.back_btn.bind(on_release=self.go_back) 
        style_round_button(self.back_btn, rgba=(0.75, 0.60, 0.45, 1))
        self.add_widget(self.back_btn)
    
    def _fit_back_btn(self, btn, *_):
        pad = 10                            # chừa padding
        btn.text_size = (btn.width - pad, None)
        # Font co giãn: 40 % chiều cao nhưng tối đa 22sp
        btn.font_size = min(btn.height * 0.4, 22)

    def go_back(self, instance):
        """Return to home screen."""
        app = App.get_running_app()
        if app:
            app.go_home()

# ------------------------------------------------------------------ #
class TicTacToeApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._level = 0                     # đếm màn hiện tại

    def _next_element(self) -> str:
        element = ELEMENTS[self._level % len(ELEMENTS)]
        self._level += 1
        return element
    
    def build(self):
        # Create screen manager
        self.sm = ScreenManager(transition=FadeTransition())
        
        # Add home screen
        self.home_screen = HomeScreen(name='home')
        self.sm.add_widget(self.home_screen)
        
        return self.sm
    
    def start_game(self, mode: str, difficulty: str| None = None):
        """Start a new game with the specified mode."""
        element = self._next_element()        # NEW – bốc theme kế tiếp

        # ---------- dọn màn cũ ----------
        if self.sm.has_screen('game'):
            old = self.sm.get_screen('game')
            if hasattr(old, 'game_widget') and hasattr(old.game_widget, '_sounds'):
                if old.game_widget._sounds.bg:
                    old.game_widget._sounds.bg.stop()
            self.sm.remove_widget(old)

        # ---------- tạo màn mới ----------
        game_screen = GameScreen(mode, difficulty, element, name='game')  # NEW
        self.sm.add_widget(game_screen)
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
