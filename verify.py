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

from mutagen.id3 import ID3
import os

from advice import Advice

dups = {}

def is_duplicate(id3info, fn, interactive):
    """
    verifies whether the combination of

        TPE1 (Lead Performer/Solo Artist)
        TIT2 (Content Group Description)

    already occured

    id3info -- mutagen id3 info object to check
    fn      -- file name of corresponding file
    interactive -- running mode
    returns true if set otherwise false
    """
    global dups

    try:
        key = id3info["TPE1"].text[0] + id3info["TIT2"].text[0]
    except KeyError:
        key = os.path.basename(fn)

    if key in dups:
        dups[key].append(fn)

        if interactive:
            a = Advice(
                helptext="Found duplicates (key: '{key}'). What to do?".
                         format(key=key))
            a.parse_args()
        return True

    dups[key] = [fn]
    return False


def has_proper_filename(fn):
    """
    verifies that the file name of file is of correct format

    fn -- file to check
    returns true if set otherwise false

    """
    id3info = ID3(fn)

    if not "TRCK" in id3info:
        return False
    elif not "TIT2" in id3info:
        return False

    title = id3info["TIT2"].text[0].replace(" ", "-")

    filename = "{tracknumber}_{title}".format(
                    tracknumber=id3info["TRCK"].text[0],
                    title=title
                )

    tocheck, _ = os.path.splitext(os.path.split(fn)[1])

    return tocheck == filename


def has_proper_dirname(fn, root):
    """
    verifies that the file is located in a directory of correct
    format

    fn      -- file to check
    root    -- root directory that contains music files
    returns true if set otherwise false

    """
    id3info = ID3(fn)

    if not "TALB" in id3info:
        return False
    elif not "TPUB" in id3info:
        return False

    publisher = id3info["TPUB"].text[0].replace(" ", "-")
    ep = id3info["TALB"].text[0].replace(" ", "-")

    filename = "{root}/{publisher}/{ep}".format(
                    root=root,
                    publisher=publisher,
                    ep=ep
                )

    tocheck = os.path.dirname(fn)

    return tocheck == filename


def has_cover(id3info, fn, interactive):
    """
    verifies that the passed file has a picture tag set

    id3info -- mutagen id3 info object to check
    fn      -- file name of corresponding file
    interactive -- running mode
    returns true if set otherwise false
    """
    has_file = False
    has_tag = False

    base = os.path.dirname(fn)

    if os.path.isfile(os.path.join(base, b"cover.png")) or \
       os.path.isfile(os.path.join(base, b"cover.jpg")) or \
       os.path.isfile(os.path.join(base, b"cover.jpeg")):
        has_file = True

    for tag in id3info.keys():
        if tag.startswith("APIC"):
            has_tag = True

    if interactive and (not has_tag or not has_file):
        output = "APIC" if not has_tag else ""
        output += ", cover.{png,jpg,jpeg}" if not has_file else ""
        a = Advice(
            helptext="Missing cover ({0}) for {1}. What to do?".
                     format(output, fn))
        a.parse_args()

    return has_file and has_tag


def has_id3tags(id3info, fn, interactive):
    """
    verifies that the passed file has a picture tag set

    id3info -- mutagen id3 info object to check
    fn      -- file name of corresponding file
    interactive -- running mode
    returns true if set otherwise false

    """

    return ("TPUB" in id3info and
            "TALB" in id3info and
            "TRCK" in id3info and
            "TDAT" in id3info and
            "TPE1" in id3info
            )

