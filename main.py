"""
Codex - Video Transcoding GUI
Entry point
"""
import sys
from src.ui.app import CodexApp

def main():
    app = CodexApp()
    app.mainloop()

if __name__ == "__main__":
    main()
