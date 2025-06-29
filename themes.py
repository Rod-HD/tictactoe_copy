from pathlib import Path

class Theme:
    def __init__(self, name: str):
        base = Path("assets") / name
        self.bg       = str(base / "bg.png")
        self.cell_bg  = str(base / "cell.png")   # nếu đã thêm
        self.x_icon   = str(base / "x.png")
        self.o_icon   = str(base / "o.png")
        self.obs_icon = str(base / "obstacle.png")