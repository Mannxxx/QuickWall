"""Functions related to setting the wallpaper."""

import subprocess

from pathlib import Path
from os import makedirs, remove
from QuickWall.download import download


class SetPaper:
    """
    Download the wallpaper and set it using nitrogen.
    """
    def __init__(self, entity):
        self._url = entity['dw_link']
        self._dir_path = Path('~/.QuickWall').expanduser()
        makedirs(self._dir_path, exist_ok=True)
        self._file_path = self._dir_path.joinpath(entity['unique_id'] + '.jpg')
        self.desc = entity['desc']
        self.name = entity['name']

    def _dw(self):
        """
        Download the file using a download manager.
        """
        download(self._url, self._file_path)

    def _restore(self):
        """
        Restore the wallpaper.
        """
        print("Restoring the last wallpaper...")
        c = 'nitrogen --restore'
        subprocess.Popen(c.split(), stdout=subprocess.PIPE)

    def _set(self):
        """
        Set the wallpaper.
        """
        c = 'nitrogen --set-zoom-fill {}'.format(self._file_path)
        p = subprocess.Popen(c.split(' '), stdout=subprocess.PIPE)
        ret, err = p.communicate()

        # Handle if error thrown

    def _set_perma(self):
        c = 'nitrogen --save --set-zoom-fill {}'.format(self._file_path)
        subprocess.Popen(c.split(), stdout=subprocess.PIPE)

    def do(self):
        print(self.desc, 'by', self.name)
        # TODO: Check if the wall already exists before downloading
        self._dw()
        self._set()
        # Interaction
        ask = input("Save this wallpapers? [Y]es [N]o [E]xit ")
        if ask.lower() == 'y':
            self._set_perma()
            exit()
        elif ask.lower() == 'e':
            self._restore()
            exit()
        else:
            remove(self._file_path)