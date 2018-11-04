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

from collections import namedtuple

import utils

Choice = namedtuple("Choice", ["args", "action"])

class Advice:

    def __init__(self, helptext, shell=True, nothing=True):
        self.help = helptext
        self.choices = {}

        if shell:
            self.add_choice("spawn shell", action=utils.spwn_shell)
        if nothing:
             self.add_choice("do nothing")


    def add_choice(self, key, action=print, args=[]):
        if key in self.choices:
            self.choices[key].args.extend(args)
        else:
            self.choices[key] = Choice(args=args, action=action)

    def __ask_choice_details(self, key):
        choice = self.choices[key]
        args = map(str, choice.args)

        options = ""
        for i, a in enumerate(args):
            options += "\t[{id}] {arg}\n".format(id=i, arg=str(a))

        output = "{key}:\n{options}".format(
            key=key,
            options=options
        )

        while 1:
            try:
                s = int(input(output))
                choice.action(choice.args[s])
                break
            except Exception as e:
                print("Tell me! WHAT HAVE YOU DONE TO ME? ({err})".format(err=str(e)))


    def __ask_choices(self):
        output = ""
        for i, c in enumerate(self.choices.keys()):
            output = "[{id}] {key}".format(
                id=i,
                key=c
            )
            print(output)

        while 1:
            try:
                s = int(input("But choose wisely, for while the true Grail "
                          "will bring you life, the false Grail will take "
                          "it from you: "))

                key = list(self.choices.keys())[s]
                if self.choices[key].args:
                    self.__ask_choice_details(key)
                elif callable(self.choices[key].action):
                    self.choices[key].action()

                break
            except Exception as e:
                print("He chose... unwisely. ({err})".format(err=str(e)))


    def parse_args(self):
        print(self.help)
        self.__ask_choices()

