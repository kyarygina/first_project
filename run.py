import sys
from file_manager.cli import main as cli_main
from file_manager.gui import run_gui


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "gui":
        run_gui()
    else:
        cli_main()