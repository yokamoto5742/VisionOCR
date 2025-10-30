import subprocess

from scripts.version_manager import update_main_py, update_version


def build_executable():
    new_version = update_version()
    update_main_py(new_version)

    subprocess.run([
        "pyinstaller",
        "--name=VisionOCR",
        "--windowed",
        "--icon=assets/VisionOCR.ico",
        "--add-data", "utils/config.ini:utils",
        "main.py"
    ])

    print(f"Executable built successfully. Version: {new_version}")


if __name__ == "__main__":
    build_executable()
