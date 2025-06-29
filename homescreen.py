# homescreen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.uix.popup import Popup
from kivy.app import App

class HomeScreen(Screen):
    """Home screen with game mode selection."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Use FloatLayout as base
        root = FloatLayout()
        
        # Background - same as game
        with root.canvas.before:
            self.bg = Rectangle(source='assets/wood/bg.png', pos=root.pos, size=root.size)
        root.bind(size=self._update_bg, pos=self._update_bg)
        
        # Main layout for content
        main_layout = BoxLayout(orientation='vertical', padding=50, spacing=30)
        
        # Title
        title = Label(
            text='[b]Tic Tac Toe[/b]',
            font_size='60sp',
            size_hint=(1, 0.4),
            markup=True
        )
        
        # Buttons container
        button_container = BoxLayout(
            orientation='vertical',
            spacing=20,
            size_hint=(1, 0.6)
        )
        
        # Play vs Bot button
        vs_bot_btn = Button(
            text='Play vs Bot',
            font_size='24sp',
            size_hint=(1, 0.3),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        vs_bot_btn.bind(on_release=self.show_difficulty_popup)
        
        # Play with Friend button
        vs_friend_btn = Button(
            text='Play with Friend',
            font_size='24sp',
            size_hint=(1, 0.3),
            background_color=(0.8, 0.4, 0.2, 1)
        )
        vs_friend_btn.bind(on_release=lambda x: self.start_game('friend'))
        
        # Add widgets
        button_container.add_widget(vs_bot_btn)
        button_container.add_widget(vs_friend_btn)
        
        main_layout.add_widget(title)
        main_layout.add_widget(button_container)
        
        root.add_widget(main_layout)
        self.add_widget(root)
        
        # Store reference to root for background updates
        self.root_widget = root
    
    def _update_bg(self, widget, *args):
        self.bg.pos = widget.pos
        self.bg.size = widget.size
    
    def show_difficulty_popup(self, instance):
        """Show difficulty selection popup."""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Create popup first
        popup = Popup(
            title='Select Difficulty',
            content=content,
            size_hint=(0.8, 0.5)
        )
        
        # Difficulty buttons
        easy_btn = Button(text='Easy', size_hint=(1, 0.3))
        easy_btn.bind(on_release=lambda x: self.select_difficulty('easy', popup))
        
        medium_btn = Button(text='Medium', size_hint=(1, 0.3))
        medium_btn.bind(on_release=lambda x: self.select_difficulty('medium', popup))
        
        hard_btn = Button(text='Hard', size_hint=(1, 0.3))
        hard_btn.bind(on_release=lambda x: self.select_difficulty('hard', popup))
        
        content.add_widget(easy_btn)
        content.add_widget(medium_btn)
        content.add_widget(hard_btn)
        
        popup.open()
    
    def select_difficulty(self, difficulty, popup):
        """Handle difficulty selection."""
        popup.dismiss()
        self.start_game('bot', difficulty)
    
    def start_game(self, mode, difficulty=None):
        """Start the game with selected mode."""
        app = App.get_running_app()
        if app:
            app.start_game(mode, difficulty)
