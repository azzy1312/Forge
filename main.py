"""
Forge - Video Transcoding GUI
Entry point
"""
import sys
from src.ui.app import ForgeApp

def main():
    app = ForgeApp()
    app.mainloop()

if __name__ == "__main__":
    main()
