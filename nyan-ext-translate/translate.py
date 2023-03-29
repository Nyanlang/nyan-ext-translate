from pathlib import Path


def translate(lang, src: Path, dest: Path):
    print(f"Translating '{src}' to '{dest}'...")
    match lang:
        case "bf":
            mapper = {"<": "!", ">": "?", "+": "냥", "-": "냐", "[": "~", "]": "-", ",": ",", ".": ".", ' ': ' ',
                      '\n': "\n"}
            with open(src, "r") as _f:
                origin_program = _f.read()
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
            with open(dest, "w") as _f:
                _f.write(source)
