"""
jarvis/gui/waveform.py — Animated Waveform Widget
Sine-wave bar visualizer that pulses when Jarvis is active.
"""

import math
from tkinter import Canvas
from config import (
    BG_COLOR, ACCENT_DIM,
    WAVE_BAR_COUNT, WAVE_BAR_WIDTH, WAVE_BAR_GAP,
    WAVE_MAX_HEIGHT, WAVE_FPS,
)


class WaveformCanvas(Canvas):
    """Animated waveform canvas that pulses during speech/listening."""

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            bg=BG_COLOR,
            highlightthickness=0,
            height=70,
            **kwargs,
        )
        self._active   = False
        self._phase    = 0.0
        self._after_id = None
        self.bind("<Configure>", lambda e: self._draw_idle())
        self._draw_idle()

    # ------------------------------------------------------------------
    # PUBLIC
    # ------------------------------------------------------------------

    def start(self):
        """Start the animated waveform."""
        self._active = True
        self._animate()

    def stop(self):
        """Stop animation and reset to idle flat bars."""
        self._active = False
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None
        self._draw_idle()

    # ------------------------------------------------------------------
    # PRIVATE
    # ------------------------------------------------------------------

    def _draw_idle(self):
        """Draw flat idle bars."""
        self.delete("all")
        w       = self.winfo_width() or 400
        total   = WAVE_BAR_COUNT * (WAVE_BAR_WIDTH + WAVE_BAR_GAP)
        x_start = (w - total) // 2
        mid_y   = 35
        for i in range(WAVE_BAR_COUNT):
            x = x_start + i * (WAVE_BAR_WIDTH + WAVE_BAR_GAP)
            self.create_rectangle(
                x, mid_y - 3, x + WAVE_BAR_WIDTH, mid_y + 3,
                fill=ACCENT_DIM, outline="",
            )

    def _animate(self):
        if not self._active:
            return

        self.delete("all")
        w       = self.winfo_width() or 400
        total   = WAVE_BAR_COUNT * (WAVE_BAR_WIDTH + WAVE_BAR_GAP)
        x_start = (w - total) // 2
        mid_y   = 35
        self._phase += 0.18

        for i in range(WAVE_BAR_COUNT):
            x   = x_start + i * (WAVE_BAR_WIDTH + WAVE_BAR_GAP)
            raw = (
                math.sin(self._phase + i * 0.45)
                * math.cos(self._phase * 0.3 + i * 0.2)
            )
            h = max(3, int(abs(raw) * WAVE_MAX_HEIGHT))

            # Cyan → green gradient across bars
            ratio = abs(i / WAVE_BAR_COUNT - 0.5) * 2
            g     = int(255 * (1 - ratio * 0.4))
            b     = int(247 * (1 - ratio * 0.6))
            color = f"#00{g:02x}{b:02x}"

            # Main bar
            self.create_rectangle(
                x, mid_y - h, x + WAVE_BAR_WIDTH, mid_y + h,
                fill=color, outline="",
            )
            # Reflection glow
            self.create_rectangle(
                x, mid_y + h + 2,
                x + WAVE_BAR_WIDTH, mid_y + h + max(1, h // 3),
                fill=ACCENT_DIM, outline="",
            )

        self._after_id = self.after(WAVE_FPS, self._animate)