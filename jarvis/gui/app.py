"""
jarvis/gui/app.py — Main Application Window
Assembles all GUI components and manages the background listener thread.
"""

import sys
import threading
import datetime
import customtkinter as ctk

from jarvis.gui.waveform    import WaveformCanvas
from jarvis.gui.weather_card import WeatherCard
from jarvis.gui.chat        import ChatLog
from jarvis.tts             import speak
from jarvis.speech          import listen, calibrate
from jarvis.commands        import process
from config import (
    APP_TITLE, APP_GEOMETRY, APP_MIN_SIZE,
    WAKE_WORD, WAKE_TIMEOUT, WAKE_PHRASE_LIM,
    CMD_TIMEOUT, CMD_PHRASE_LIM,
    BG_COLOR, PANEL_COLOR, ACCENT_COLOR, ACCENT_DIM,
    GREEN_ACCENT, TEXT_PRIMARY, TEXT_DIM,
    MIC_ACTIVE, MIC_IDLE, ERROR_COLOR,
    FOOTER_TEXT,
)


class JarvisApp(ctk.CTk):
    """Main Jarvis GUI application window."""

    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)
        self.minsize(*APP_MIN_SIZE)
        self.configure(fg_color=BG_COLOR)

        self._is_speaking  = False
        self._mic_active   = False

        self._build_ui()
        self._start_listener()

    # ==================================================================
    # UI CONSTRUCTION
    # ==================================================================

    def _build_ui(self):
        self._build_header()
        self._build_content()
        self._build_footer()

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color=PANEL_COLOR, corner_radius=0, height=64)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="◈  J.A.R.V.I.S",
            font=ctk.CTkFont("Courier New", 22, "bold"),
            text_color=ACCENT_COLOR,
        ).pack(side="left", padx=20, pady=10)

        self.clock_label = ctk.CTkLabel(
            header,
            text="",
            font=ctk.CTkFont("Courier New", 13),
            text_color=TEXT_DIM,
        )
        self.clock_label.pack(side="right", padx=20)
        self._tick_clock()

    def _build_content(self):
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=16, pady=(12, 0))

        self._build_left_column(content)
        self._build_right_column(content)

    def _build_left_column(self, parent):
        left = ctk.CTkFrame(parent, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(
            left,
            text="◈  COMM LOG",
            font=ctk.CTkFont("Courier New", 10, "bold"),
            text_color=TEXT_DIM,
        ).pack(anchor="w", pady=(0, 4))

        self.chat_log = ChatLog(left)
        self.chat_log.pack(fill="both", expand=True)

        # Waveform
        wave_frame = ctk.CTkFrame(
            left,
            fg_color=PANEL_COLOR,
            border_color=ACCENT_DIM,
            border_width=1,
            corner_radius=12,
            height=75,
        )
        wave_frame.pack(fill="x", pady=(10, 0))
        wave_frame.pack_propagate(False)

        self.waveform = WaveformCanvas(wave_frame, width=400)
        self.waveform.pack(fill="both", expand=True, padx=8, pady=4)

        # Status + mic button row
        bottom = ctk.CTkFrame(left, fg_color="transparent")
        bottom.pack(fill="x", pady=(10, 12))

        self.status_label = ctk.CTkLabel(
            bottom,
            text=f"Say  '{WAKE_WORD.capitalize()}'  to wake me up",
            font=ctk.CTkFont("Courier New", 11),
            text_color=TEXT_DIM,
        )
        self.status_label.pack(side="left", expand=True)

        self.mic_btn = ctk.CTkButton(
            bottom,
            text="⏺  MIC",
            width=100,
            height=36,
            corner_radius=8,
            fg_color=ACCENT_DIM,
            hover_color=ACCENT_DIM,
            border_color=MIC_IDLE,
            border_width=2,
            font=ctk.CTkFont("Courier New", 12, "bold"),
            text_color=ACCENT_COLOR,
            command=self._on_mic_click,
        )
        self.mic_btn.pack(side="right")

    def _build_right_column(self, parent):
        right = ctk.CTkFrame(parent, fg_color="transparent", width=220)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        ctk.CTkLabel(
            right,
            text="◈  SENSOR ARRAY",
            font=ctk.CTkFont("Courier New", 10, "bold"),
            text_color=TEXT_DIM,
        ).pack(anchor="w", pady=(0, 4))

        self.weather_card = WeatherCard(right)
        self.weather_card.pack(fill="x")

        # System status panel
        status_panel = ctk.CTkFrame(
            right,
            fg_color=PANEL_COLOR,
            border_color=ACCENT_DIM,
            border_width=1,
            corner_radius=12,
        )
        status_panel.pack(fill="x", pady=(10, 0))

        ctk.CTkLabel(
            status_panel,
            text="⬡  SYSTEM STATUS",
            font=ctk.CTkFont("Courier New", 10, "bold"),
            text_color=TEXT_DIM,
        ).pack(anchor="w", padx=14, pady=(10, 4))

        ctk.CTkLabel(
            status_panel,
            text="◉  AI CORE  [ ONLINE ]",
            font=ctk.CTkFont("Courier New", 11),
            text_color=GREEN_ACCENT,
        ).pack(anchor="w", padx=14, pady=2)

        ctk.CTkLabel(
            status_panel,
            text="◉  VOICE    [ READY ]",
            font=ctk.CTkFont("Courier New", 11),
            text_color=GREEN_ACCENT,
        ).pack(anchor="w", padx=14, pady=(2, 10))

    def _build_footer(self):
        ctk.CTkFrame(self, fg_color=ACCENT_DIM, height=2, corner_radius=0).pack(fill="x")
        footer = ctk.CTkFrame(self, fg_color=PANEL_COLOR, corner_radius=0, height=28)
        footer.pack(fill="x")
        footer.pack_propagate(False)
        ctk.CTkLabel(
            footer,
            text=FOOTER_TEXT,
            font=ctk.CTkFont("Courier New", 9),
            text_color=TEXT_DIM,
        ).pack(side="left", padx=16, pady=4)

    # ==================================================================
    # CLOCK
    # ==================================================================

    def _tick_clock(self):
        now = datetime.datetime.now().strftime("%a  %d %b %Y    %H:%M:%S")
        self.clock_label.configure(text=now)
        self.after(1000, self._tick_clock)

    # ==================================================================
    # PUBLIC API — called by tts / commands
    # ==================================================================

    def add_message(self, text: str, sender: str = "jarvis"):
        self.chat_log.add_message(text, sender)

    def set_status(self, text: str, color: str = TEXT_DIM):
        self.status_label.configure(text=text, text_color=color)

    def start_waveform(self):
        self.waveform.start()

    def stop_waveform(self):
        self.waveform.stop()

    def update_weather_card(self, data: dict):
        self.weather_card.update(data)

    # ==================================================================
    # MIC BUTTON
    # ==================================================================

    def _on_mic_click(self):
        if self._mic_active or self._is_speaking:
            return
        self._set_mic_state(True)
        threading.Thread(target=self._manual_listen, daemon=True).start()

    def _set_mic_state(self, active: bool):
        self._mic_active = active
        if active:
            self.mic_btn.configure(text="⏹  STOP", border_color=MIC_ACTIVE, text_color=MIC_ACTIVE)
            self.set_status("Listening...", MIC_ACTIVE)
            self.start_waveform()
        else:
            self.mic_btn.configure(text="⏺  MIC", border_color=MIC_IDLE, text_color=ACCENT_COLOR)
            self.stop_waveform()
            self.set_status(f"Say  '{WAKE_WORD.capitalize()}'  to wake me up", TEXT_DIM)

    def _manual_listen(self):
        command = listen(timeout=CMD_TIMEOUT, phrase_limit=CMD_PHRASE_LIM)
        self._set_mic_state(False)
        if command:
            self.add_message(command, sender="user")
            threading.Thread(target=self._run_command, args=(command,), daemon=True).start()
        else:
            self.set_status("Didn't catch that. Try again.", ERROR_COLOR)
            self.after(2000, lambda: self.set_status(
                f"Say  '{WAKE_WORD.capitalize()}'  to wake me up", TEXT_DIM
            ))

    # ==================================================================
    # COMMAND RUNNER
    # ==================================================================

    def _run_command(self, command: str):
        self._is_speaking = True

        # Thread-safe UI update
        self.after(0, lambda: self.set_status("Thinking...", ACCENT_COLOR))

        def on_reply(text):
            # Always update UI from main thread
            self.after(0, lambda: self.add_message(text, sender="jarvis"))
            self.after(0, lambda: self.set_status("Speaking...", ACCENT_COLOR))
            self.after(0, self.start_waveform)
            speak(text)
            self.after(0, self.stop_waveform)

        def on_weather(data):
            self.after(0, lambda: self.update_weather_card(data))

        def on_exit():
            # Delay close so Jarvis finishes speaking goodbye
            self.after(1200, self.destroy)

        process(command, on_reply=on_reply, on_weather=on_weather, on_exit=on_exit)

        self._is_speaking = False
        self.after(0, lambda: self.set_status(
            f"Say  '{WAKE_WORD.capitalize()}'  to wake me up", TEXT_DIM
        ))

    # ==================================================================
    # BACKGROUND WAKE WORD LISTENER
    # ==================================================================

    def _start_listener(self):
        threading.Thread(target=self._listener_loop, daemon=True).start()

    def _listener_loop(self):
        calibrate()

        greeting = "Jarvis online. Say Jarvis to wake me up."
        self.after(0, lambda: self.add_message(greeting, sender="jarvis"))
        speak(greeting)

        while True:
            if self._is_speaking or self._mic_active:
                continue

            word = listen(timeout=WAKE_TIMEOUT, phrase_limit=WAKE_PHRASE_LIM)
            if not word:
                continue

            if WAKE_WORD in word:
                self.after(0, lambda: self.set_status(
                    "Activated! Listening for command...", ACCENT_COLOR
                ))
                reply = "Yes, how can I help you?"
                self.after(0, lambda: self.add_message(reply, sender="jarvis"))
                speak(reply)

                # ---- Retry up to 3 times before going back to wake word ----
                command = None
                for attempt in range(3):
                    command = listen(timeout=CMD_TIMEOUT, phrase_limit=CMD_PHRASE_LIM)
                    if command:
                        break
                    # Don't ask again on last attempt
                    if attempt < 2:
                        retry_msg = "Sorry, didn't catch that. Please say your command."
                        self.after(0, lambda m=retry_msg: self.add_message(m, sender="jarvis"))
                        speak(retry_msg)

                if command:
                    self.after(0, lambda c=command: self.add_message(c, sender="user"))
                    threading.Thread(
                        target=self._run_command, args=(command,), daemon=True
                    ).start()
                else:
                    msg = "I couldn't hear you. Say Jarvis to try again."
                    self.after(0, lambda: self.add_message(msg, sender="jarvis"))
                    speak(msg)
                    self.after(0, lambda: self.set_status(
                        f"Say  '{WAKE_WORD.capitalize()}'  to wake me up", TEXT_DIM
                    ))

            elif word in ["exit", "quit", "bye"]:
                msg = "Goodbye!"
                self.after(0, lambda: self.add_message(msg, sender="jarvis"))
                speak(msg)
                self.after(1200, self.destroy)