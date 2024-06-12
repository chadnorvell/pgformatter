import sys
import difflib
from argparse import ArgumentParser
from colorama import init, Fore, Style
from pathlib import Path
from typing import Optional

from pgformatter.pg_format import pg_format


def pretty_print_diff_line(line: str) -> None:
    if line.startswith("+"):
        print(Fore.GREEN + line + Style.RESET_ALL)
    elif line.startswith("-"):
        print(Fore.RED + line + Style.RESET_ALL)
    elif line.startswith("@"):
        print(Fore.CYAN + line + Style.RESET_ALL)
    else:
        print(line)


def check_file(file_path: Path, config_file: Optional[Path] = None) -> bool:
    original_content = file_path.read_text()
    formatted_content = pg_format(original_content.encode("utf-8"), config_file).decode(
        "utf-8"
    )

    if original_content != formatted_content:
        diff = difflib.unified_diff(
            original_content.splitlines(),
            formatted_content.splitlines(),
            fromfile=f"{file_path} (original)",
            tofile=f"{file_path} (formatted)",
            lineterm="",
        )

        for line in diff:
            pretty_print_diff_line(line)

        return False
    return True


def main() -> None:
    init(autoreset=True)
    parser = ArgumentParser(prog="pg_format")
    parser.add_argument(
        "-c", "--config", type=Path, help="path to a pg_format config file"
    )
    parser.add_argument("files", nargs="+", type=Path, help="files to format")
    args = parser.parse_args()

    all_fine = True

    for file_path in args.files:
        if not check_file(file_path, args.config):
            all_fine = False

    if all_fine:
        print("All files are formatted correctly")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
