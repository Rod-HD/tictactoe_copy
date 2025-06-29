# widgets_board.py
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from kivy.properties import StringProperty

CELL_SIZE = 80      # px – cố định
CELLS_PER_SIDE = 5  # 5×5

class XOCell(ButtonBehavior, Image):
    mark = StringProperty('')

    def __init__(self, row, col, on_press_cb, **kw):
        super().__init__(**kw)
        self.row, self.col = row, col
        self.source = 'assets/wood/cell.png'   # ô trống
        self.allow_stretch = True
        self.keep_ratio    = False
        self.size_hint = (None, None)
        self.size       = (CELL_SIZE, CELL_SIZE)
        self._cb = on_press_cb           # gọi về controller

    # ―――― sự kiện người chơi ―――――――――――――――――――――――――――――――――
    def on_release(self):
        self._cb(self.row, self.col)

    # ―――― cập nhật quân cờ ―――――――――――――――――――――――――――――――――――
    def set_mark(self, symbol):
        if symbol == 'X':
            self.source = 'assets/wood/X.png'
        elif symbol == 'O':
            self.source = 'assets/wood/O.png'
        elif symbol == '#':
            self.source = 'assets/wood/obstacle.png'
        else:
            self.source = 'assets/wood/cell.png'

class BoardWidget(GridLayout):
    """
    View – chỉ nhận lệnh từ controller:
        • reset(board)               – vẽ lại toàn bộ
        • update_cell((i,j), symbol) – đặt quân tại ô
    """
    def __init__(self, board, on_cell_cb, **kw):
        super().__init__(rows=CELLS_PER_SIDE, cols=CELLS_PER_SIDE,
                         spacing=0, size_hint=(None, None), **kw)
        self.size = (CELL_SIZE * CELLS_PER_SIDE,
                     CELL_SIZE * CELLS_PER_SIDE)

        self._cells = {}
        for i in range(CELLS_PER_SIDE):
            for j in range(CELLS_PER_SIDE):
                c = XOCell(i, j, on_cell_cb)
                self.add_widget(c)
                self._cells[(i, j)] = c

        # chặn cửa sổ nhỏ hơn bàn cờ
        Window.minimum_width  = CELL_SIZE * CELLS_PER_SIDE   # 400
        Window.minimum_height = CELL_SIZE * CELLS_PER_SIDE   # 400

    # ------------------- public API dùng trong layout ---------------------
    def reset(self, board):
        for (i, j), cell in self._cells.items(): 
            if board.is_obstacle(i, j): 
                cell.set_mark('#') 
                cell.disabled = True
            else: 
                cell.set_mark('') 
                cell.disabled = False

    def update_cell(self, coords, symbol):
        self._cells[coords].set_mark(symbol)
        self._cells[coords].disabled = True
