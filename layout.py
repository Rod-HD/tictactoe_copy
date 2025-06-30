from __future__ import annotations
"""layout.py – keeps original public API (TicTacToeLayout) but fixes sizing

* Board always remains **perfectly square**.
* Board **fills the window width** when the window is portrait / square.
* Board never exceeds the window height; if landscape it shrinks to fit.
* The square is **vertically centred**; status + restart stay at the bottom.
* The playable 5 × 5 GameGrid is framed with a 1⁄12 margin (so each cell = 1⁄6 board side).
"""

from typing import Optional, Tuple

from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.graphics import Rectangle

from controller import GameController, GameState, GameObserver  # giữ nguyên
from board import Board
from themes import Theme
from sound_manager import SoundManager
from widgets import BoardWidget
from kivy.app import App
from utils import style_round_button
# --------------------------------------------------------------------------- #
class TicTacToeLayout(FloatLayout):          # type: ignore[misc]
    """Main root widget shown by the App.

    NOTE: the class name is unchanged so **all existing imports remain valid**.
    """
    
    status_message = StringProperty("X's turn")

    # --------------------------- construction ------------------------------ #
    def __init__(self, controller: GameController, theme: Theme, **kw):
        LIGHT = (0.75, 0.60, 0.45, 1)
        super().__init__(**kw)

        # ---------- background that stretches with the window -------------
        with self.canvas.before:
            self._bg = Rectangle(source=theme.bg, pos=self.pos, size=self.size)
        self.bind(size=self._sync_bg, pos=self._sync_bg)
        
        # ---------- keep refs --------------------------------------------
        self._controller = controller
        self._board: Board = controller.getBoard()
        self._theme = theme
        self._sounds = SoundManager()

        # ---------- board container --------------------------------------
        self._board_container = FloatLayout(size_hint=(None, None),
                                            pos_hint={"center_x": .5, "center_y": .5})


        # 5×5 playable grid (safe‑zone)
        self._grid = BoardWidget(
            self._board,
            self._on_cell,            # callback đã có sẵn
        )
        # Căn giữa trong _board_container
        self._grid.pos_hint = {"center_x": .5, "center_y": .5}
        self._board_container.add_widget(self._grid)
        self._grid.reset(self._board)
        # ---------- status + restart bar at the bottom --------------------
        BAR_HEIGHT   = 200
        LABEL_HEIGHT = 28

        self._ui_bar = BoxLayout(orientation="vertical",
                                 size_hint=(1, None),
                                 height=BAR_HEIGHT,
                                 pos_hint={"x": 0, "y": 0})

        self._status = Label(text=self.status_message,
                             size_hint=(1, None), height=LABEL_HEIGHT, font_size='20sp')

        self._restart = Button(text="Restart",
                               size_hint=(1, None), height=BAR_HEIGHT - LABEL_HEIGHT, font_size='32sp',
                               opacity=0, disabled=True)
        self._restart.bind(on_release=self._on_restart)

        self._ui_bar.add_widget(self._status)
        self._ui_bar.add_widget(self._restart)
        style_round_button(self._restart, rgba=LIGHT)
        # ---------- assemble ---------------------------------------------
        self.add_widget(self._board_container)
        self.add_widget(self._ui_bar)

        # respond to window resize
        Window.bind(size=self._update_board_geometry)
        self.bind(size=self._update_board_geometry)
        self._update_board_geometry()           # initial placement

        controller.register(self)               # listen for game events

    # ------------------ geometric helpers --------------------------------- #
    def _update_board_geometry(self, *_):
        win_w, win_h = Window.size
        ui_h   = self._ui_bar.height          # thanh trạng thái + nút Restart

        # ❶ Phần không gian thực sự có thể đặt bàn cờ  
        free_h = win_h - ui_h                 # trừ đi thanh dưới cùng

        # ❷ Cạnh bàn cờ lấy cạnh nhỏ hơn giữa free_h và win_w  
        side   = min(win_w, free_h)

        # ❸ (tuỳ chọn) phóng to thêm 5 % nếu bạn muốn sát biên
        # side = int(side * 1.05)   # bỏ dòng này nếu không cần

        # ❹ Cập nhật kích thước & căn giữa  
        self._board_container.size = (side, side)
        self._board_container.pos  = (
            (win_w - side) / 2,              # căn giữa theo trục X
            ui_h + (free_h - side) / 2       # căn giữa phần trống còn lại
        )

    def _sync_bg(self, *_):
        self._bg.pos, self._bg.size = self.pos, self.size

    # --------------------------- UI events -------------------------------- #
    def _on_cell(self, row, col):
        self._controller.play(row, col)

    def _on_restart(self, *_):
        self._controller.reset()
        self._grid.reset(self._board)
        self._hide_restart()

    # ------------------- GameObserver callbacks --------------------------- #
    def on_board_change(self, coords: Tuple[int, int], symbol: str) -> None:
        self._grid.update_cell(coords, symbol)
        self._sounds.play_tap()

    def on_state_change(self, state: GameState, next_turn: Optional[str]) -> None:
        if state is GameState.IN_PROGRESS:
            self.status_message = f"{next_turn}'s turn"
            self._hide_restart()
        else:
            self.status_message = (
                "Draw!" if state is GameState.DRAW else f"{state.name.split('_')[0]} wins!"
            )
            self._sounds.play_draw() if state is GameState.DRAW else self._sounds.play_win()
            self._end_game()

        self._status.text = self.status_message

    # --------------------------- helpers ---------------------------------- #
    def _end_game(self):
        Clock.schedule_once(lambda *_: self._show_restart(), .3)

    def _show_restart(self):
        self._restart.disabled, self._restart.opacity = False, 1

    def _hide_restart(self):
        self._restart.disabled, self._restart.opacity = True, 0

    