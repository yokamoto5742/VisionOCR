from app.app_window import OCRApplication
from utils.log_rotation import setup_logging


def main() -> None:
    setup_logging()
    app = OCRApplication()
    app.root.mainloop()


if __name__ == "__main__":
    main()
