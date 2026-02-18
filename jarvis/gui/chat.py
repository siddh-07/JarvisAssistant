"""
jarvis/gui/chat.py — Chat Log Widget
Scrollable conversation panel with styled message bubbles.
"""

import customtkinter as ctk
from config import (
    PANEL_COLOR, ACCENT_DIM, ACCENT_COLOR,
    GREEN_ACCENT, TEXT_PRIMARY, USER_BUBBLE, JARVIS_BUBBLE,
)


class ChatLog(ctk.CTkScrollableFrame):
    """Scrollable chat log with distinct user and Jarvis bubbles."""

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=PANEL_COLOR,
            border_color=ACCENT_DIM,
            border_width=1,
            corner_radius=12,
            scrollbar_button_color=ACCENT_DIM,
            scrollbar_button_hover_color=ACCENT_COLOR,
            **kwargs,
        )

    def add_message(self, text: str, sender: str = "jarvis"):
        """
        Add a message bubble to the chat log.

        Args:
            text:   Message content.
            sender: 'user' or 'jarvis'
        """
        is_user    = sender == "user"
        bubble_bg  = USER_BUBBLE  if is_user else JARVIS_BUBBLE
        anchor     = "e"          if is_user else "w"
        prefix     = "YOU  ▶"    if is_user else "◀  JARVIS"
        label_color = GREEN_ACCENT if is_user else ACCENT_COLOR

        bubble = ctk.CTkFrame(
            self,
            fg_color=bubble_bg,
            corner_radius=10,
            border_color=ACCENT_DIM,
            border_width=1,
        )
        bubble.pack(anchor=anchor, pady=4, padx=8, fill="x")

        ctk.CTkLabel(
            bubble,
            text=prefix,
            font=ctk.CTkFont("Courier New", 9, "bold"),
            text_color=label_color,
        ).pack(anchor="w", padx=10, pady=(6, 0))

        ctk.CTkLabel(
            bubble,
            text=text,
            font=ctk.CTkFont("Courier New", 12),
            text_color=TEXT_PRIMARY,
            wraplength=380,
            justify="left",
        ).pack(anchor="w", padx=10, pady=(2, 8))

        # Auto-scroll to latest message
        self.after(100, lambda: self._parent_canvas.yview_moveto(1.0))