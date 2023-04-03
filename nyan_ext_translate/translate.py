from pathlib import Path
from sys import stdout, stdin


class Translator:
    def __init__(self, lang: str, src: Path, dest: Path, stdo: bool = False, stdi: bool = False):
        self.lang = lang
        self.src = src
        self.dest = dest
        self.stdout = stdo
        self.stdin = stdi

    def read(self):
        if self.stdin:
            return stdin.read()
        with open(self.src, "r", encoding="utf-8") as _f:
            return _f.read()

    def write(self, source):
        with open(self.dest, "w", encoding="utf-8") as _f:
            _f.write(source)

    def std_output(self, source):
        stdout.write(source)

    def brainfuck(self):
        print(f"Translating '{self.src}' to '{self.dest}'...")
        mapper = {"<": "!", ">": "?", "+": "냥", "-": "냐", "[": "~", "]": "-", ",": ",", ".": ".", ' ': ' ',
                  '\n': "\n"}
        origin_program = self.read()
        source = ""
        comment_mode = False
        for char in origin_program:
            if char not in "<>+-[],. \n":
                if not comment_mode:
                    source += "\""
                comment_mode = True
                source += char
            else:
                if char == " " and comment_mode:
                    source += char
                    continue
                if comment_mode:
                    comment_mode = False
                    source += "\""
                source += mapper[char]
        if comment_mode:
            source += "\""
        self.write(source)
        if self.stdout:
            self.std_output(source)
