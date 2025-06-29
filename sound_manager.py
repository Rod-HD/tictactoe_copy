from kivy.core.audio import SoundLoader

class SoundManager:
    """Load & reuse background / SFX once."""
    def __init__(self):
        self.bg   = SoundLoader.load("sounds/bg_music.ogg")
        self.tap  = SoundLoader.load("sounds/click.wav")
        self.win  = SoundLoader.load("sounds/win.wav")
        self.draw = SoundLoader.load("sounds/draw.wav")

        for s in (self.bg, self.tap, self.win, self.draw):
            if s:
                s.volume = .4

        if self.bg:
            self.bg.loop = True
            self.bg.play()

    # helper wrappers --------------------------------------------------
    def play_tap(self):   self._safe(self.tap)
    def play_win(self):   self._safe(self.win)
    def play_draw(self):  self._safe(self.draw)

    @staticmethod
    def _safe(snd):
        if snd:
            snd.stop()
            snd.play()
