import re
from sys import argv

from m.utils.console import console

from ..config.types import Alias

unsafe = re.compile(r"['\" ]", re.ASCII).search  # copied from shlex


def print_command(cmd: str, shell=False, extra_args: list[str] | None = None):
    from shlex import quote, split

    console.print("\n [d]>>", *(quote(i) if unsafe(i) else i for i in split(cmd)), end="", style="green" if shell else "blue")

    if extra_args:
        console.print(" " + " ".join(extra_args), style="yellow", end="\n\n")
    else:
        print("\n")


def run(cmd: str, shell=False):
    from shlex import join, split
    from subprocess import Popen

    print_command(cmd, shell, argv[2:])

    exit((Popen(f"{cmd} {join(argv[2:])}", shell=True) if shell else Popen(split(cmd) + argv[2:])).wait())


def get_runner(item: Alias | str):
    if isinstance(item, dict):
        return lambda: run(item["cmd"], item["shell"])
    return lambda: run(item)
