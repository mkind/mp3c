"""
mp3c is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

mp3c is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with mp3c.  If not, see <http://www.gnu.org/licenses/>.

"""

import mutagen.id3
import mutagen
import pty
import os

import verify


class colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'


def spwn_shell():
    #TODO change into current music directory
    pty.spawn("/bin/sh")


def _get_mp3_files(location):
    """ returns mp3 files in location """

    for root, _, files in os.walk(location):
        for f in files:
            # skip non mp3 files
            if (not f.endswith(".mp3")) or f.startswith("."):
                continue

            yield os.fsencode(os.path.join(root, f.replace("/", "")))

    raise StopIteration


def list_files(args):
    """
    list mp3 files found in location

    args    -- argparser NamesSpace object containing the pass arg

    """

    try:
        for fn in _get_mp3_files(args.location):
            errors = ""
            id3info = mutagen.id3.ID3(fn)

            if verify.is_duplicate(id3info, fn, args.interactive):
                errors += "D"

            if not verify.has_cover(id3info, fn, args.interactive):
                errors += "C"

            if not verify.has_id3tags(id3info, fn, args.interactive):
                errors += "3"

            if not errors:
                continue

            result = "{filename} [{col}{errors}{res}]".format(
                        filename=fn,
                        col=colors.WARNING,
                        errors=errors,
                        res=colors.RESET
                        )
            print(result)

    except StopIteration:
        pass

