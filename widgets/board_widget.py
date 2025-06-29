from kivy.uix.gridlayout import GridLayout
from kivy.core.window    import Window

from .xo_cell import XOCell, CELL_SIZE

CELLS_PER_SIDE = 5  # 5×5 grid

class BoardWidget(GridLayout):
    """
    View layer for the 5×5 game board.
    Public API called by layout.py:
        • reset(board)               – redraw everything
        • update_cell((i,j), symbol) – set a piece
    """
    def __init__(self, board, on_cell_cb, **kw):
        super().__init__(rows=CELLS_PER_SIDE, cols=CELLS_PER_SIDE,
                         spacing=0, size_hint=(None, None), **kw)

        side_px = CELL_SIZE * CELLS_PER_SIDE
        self.size = (side_px, side_px)

        # Dict[(row,col) → XOCell]
        self._cells = {}
        for i in range(CELLS_PER_SIDE):
            for j in range(CELLS_PER_SIDE):
                cell = XOCell(i, j, on_cell_cb)
                self.add_widget(cell)
                self._cells[(i, j)] = cell

        # prevent window smaller than board
        Window.minimum_width  = side_px
        Window.minimum_height = side_px

    # ————— API for controller/layout ——————————————
    def reset(self, board):
        """Refresh whole board from model state."""
        for (i, j), cell in self._cells.items():
            if board.is_obstacle(i, j):
                cell.set_mark("#")
                cell.disabled = True
            else:
                cell.set_mark("")
                cell.disabled = False

    def update_cell(self, coords, symbol):
        cell = self._cells[coords]
        cell.set_mark(symbol)
        cell.disabled = True
