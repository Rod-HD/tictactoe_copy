from kivy.uix.image    import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties    import StringProperty
from kivy.core.window   import Window

CELL_SIZE = 80         # px – fixed
ASSET_ROOT = "assets/wood"

class XOCell(ButtonBehavior, Image):
    """A single clickable cell in the Tic-Tac-Toe grid."""
    mark = StringProperty("")

    def __init__(self, row: int, col: int, on_press_cb, **kw):
        super().__init__(**kw)
        self.row, self.col = row, col
        self.allow_stretch = True
        self.keep_ratio    = False
        self.size_hint     = (None, None)
        self.size          = (CELL_SIZE, CELL_SIZE)
        self._cb           = on_press_cb

        self.set_mark("")  # start blank

    # —— player interaction ——————————————————————————
    def on_release(self):
        self._cb(self.row, self.col)

    # —— update graphic ————————————————————————————
    def set_mark(self, symbol: str):
        mapping = {
            "X": f"{ASSET_ROOT}/X.png",
            "O": f"{ASSET_ROOT}/O.png",
            "#": f"{ASSET_ROOT}/obstacle.png",
            "":  f"{ASSET_ROOT}/cell.png",
        }
        self.source = mapping.get(symbol, mapping[""])
