from serpent.game_launcher import GameLauncher, GameLauncherException
from serpent.utilities import is_linux, is_macos, is_windows

import shlex
import subprocess


class ExecutableGameLauncher(GameLauncher):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def launch(self, **kwargs):
        executable_path = kwargs.get("executable_path")
        current_work_directory = kwargs.get("current_work_directory")

        if executable_path is None:
            raise GameLauncherException("An 'executable_path' kwarg is required...")

        if is_linux():
            subprocess.Popen(shlex.split(executable_path),cwd=current_work_directory)
        elif is_macos():
            subprocess.Popen(shlex.split(executable_path),cwd=current_work_directory)
        elif is_windows():
            subprocess.Popen(shlex.split(executable_path),cwd=current_work_directory)