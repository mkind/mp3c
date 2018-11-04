#!/usr/bin/env python3

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

""" a little helper tool to handle my mp3 files """
import argparse

__author__ = "mkind"

from utils import list_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser.add_argument("-i",
        help="interactive mode. tool stops in case of errors to "
             "and asks for advice",
        action="store_true",
        dest="interactive");

    # list
    parser_list = subparsers.add_parser("list",
                 help="lists *.mp3 files found in passed location")

    parser_list.add_argument("--id3",
                 action="store_true",
                 help="show id3 information for each file")

    parser_list.add_argument("--duplicate",
                 action="store_true",
                 help="show duplicate files. first check for "
                      "duplicate artist-track combination. if "
                      "id3 tags are incomplete, check file name")

    parser_list.add_argument("location",
                             help="location where to search for mp3s")
    parser_list.set_defaults(func=list_files)

    args = parser.parse_args()
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("cancelled")
