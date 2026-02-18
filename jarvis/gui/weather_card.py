"""
jarvis/gui/weather_card.py — Weather Card Widget
Displays live weather data in a sci-fi styled panel.
"""

import customtkinter as ctk
from config import (
    PANEL_COLOR, ACCENT_DIM, ACCENT_COLOR,
    GREEN_ACCENT, TEXT_PRIMARY, TEXT_DIM,
)


class WeatherCard(ctk.CTkFrame):
    """Sci-fi styled weather data display card."""

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=PANEL_COLOR,
            border_color=ACCENT_DIM,
            border_width=1,
            corner_radius=12,
            **kwargs,
        )
        self._build()

    def _build(self):
        ctk.CTkLabel(
            self,
            text="⬡  ATMOSPHERIC DATA",
            font=ctk.CTkFont("Courier New", 10, "bold"),
            text_color=TEXT_DIM,
        ).pack(anchor="w", padx=14, pady=(10, 2))

        self.city_label = ctk.CTkLabel(
            self,
            text="—",
            font=ctk.CTkFont("Courier New", 18, "bold"),
            text_color=ACCENT_COLOR,
        )
        self.city_label.pack(anchor="w", padx=14)

        self.condition_label = ctk.CTkLabel(
            self,
            text="Awaiting scan...",
            font=ctk.CTkFont("Courier New", 11),
            text_color=TEXT_PRIMARY,
        )
        self.condition_label.pack(anchor="w", padx=14)

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(6, 12))

        self.temp_label = ctk.CTkLabel(
            row,
            text="—°C",
            font=ctk.CTkFont("Courier New", 22, "bold"),
            text_color=GREEN_ACCENT,
        )
        self.temp_label.pack(side="left", padx=(0, 20))

        self.humidity_label = ctk.CTkLabel(
            row,
            text="HUM: —%",
            font=ctk.CTkFont("Courier New", 13),
            text_color=TEXT_DIM,
        )
        self.humidity_label.pack(side="left")

    def update(self, data: dict):
        """
        Update card with new weather data.

        Args:
            data: Dict with keys city, condition, temperature, humidity.
        """
        self.city_label.configure(text=data["city"].upper())
        self.condition_label.configure(text=data["condition"])
        self.temp_label.configure(text=f"{data['temperature']}°C")
        self.humidity_label.configure(text=f"HUM: {data['humidity']}%")