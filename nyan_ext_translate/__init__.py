from nyanlang.helper import Helper, Param, ParamItem
from nyanlang import return_
from .translate import Translator
import sys
from pathlib import Path

helpgen = Helper(__file__)

HELP = {
    "translate": helpgen.help(
        "translate",
        Param(
            "language",
            "Languages",
            ParamItem("bf", "Brainfuck"),
        ),
        Param("filename", "", no_desc=True),
        Param("dest", "", no_desc=True, optional=True, kw="d"),
        Param("stdout", "", no_desc=True, optional=True, kw="o"),
        Param("stdin", "", no_desc=True, optional=True, kw="i")
    ),
}


SUPPORTED_LANGS = {
    "bf": [".b", ".bf"]
}


def run():
    match sys.argv:
        case [_, _]:
            return_(HELP["translate"])
        case [_, _, _]:
            return_(HELP["translate"])
        case [_, _, language, f, *options]:
            dest = None
            stdout = False
            stdin = False
            if "-d" in options:
                dest = Path(options[options.index("-d") + 1]).absolute()
            elif "--dest" in options:
                dest = Path(options[options.index("--dest") + 1]).absolute()
            if "-o" in options or "--stdout" in options:
                stdout = True
            if "-i" in options or "--stdin" in options:
                stdin = True

            if language not in SUPPORTED_LANGS:
                raise ValueError(f"Invalid language {language}")

            _f = Path(f)

            if not _f.exists():
                raise FileNotFoundError(f"File {f} not found.")

            if _f.suffix not in SUPPORTED_LANGS[language]:
                raise ValueError(f"Invalid file extension .{' '.join(f).split('.')[-1]} - "
                                 f"File extension must be {'or'.join(['.' + i for i in SUPPORTED_LANGS[language]])}")

            if dest is None:
                dest = Path(_f.parent, _f.stem + ".nyan")

            if dest.exists():
                raise FileExistsError(f"File {dest} already exists.")

            t = Translator(language, _f, dest, stdout, stdin)
            match language:
                case "bf":
                    t.brainfuck()
