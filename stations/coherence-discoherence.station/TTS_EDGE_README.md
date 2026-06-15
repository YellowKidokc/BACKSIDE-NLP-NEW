# Edge TTS Batch Kit

Use `TTS_EDGE_RUN.bat`.

Flow:

1. Put `.md` or `.txt` files in `TTS_EDGE\inbox`.
2. Run `TTS_EDGE_RUN.bat`.
3. Press Enter.
4. MP3 parts appear in `TTS_EDGE\outbox`.
5. Source files move to `TTS_EDGE\processed`.

Voice: `en-US-BrianMultilingualNeural`

Speed: `+75%`

Change voice or speed in `TTS_EDGE\config.json`.

Use `TTS_EDGE_TROUBLESHOOT.bat` to check Python, Edge TTS, Brian voices, and inbox state.

Use `TTS_EDGE_INSTALL_OR_SYNC_TO_NETWORK.bat` to copy the same kit to `%STATIONS_ROOT%\TTS_EDGE`.
