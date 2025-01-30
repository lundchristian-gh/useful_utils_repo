"""
Note: This module contains common private functions that are used across
multiple modules.
"""


class Log:
    def __init__(self):
        self._html: list[str] = []
        self._text: list[str] = []
        self._terminal: list[str] = []

    def _plain(self, msg: str) -> None:
        formatted_msg = f"{msg}"
        self._html.append(f"<p>{formatted_msg}</p>")
        self._text.append(formatted_msg)
        self._terminal.append(formatted_msg)

    def _green(self, msg: str) -> None:
        formatted_msg = f"[+] {msg}"
        self._html.append(f"<p style='color: green;'>{formatted_msg}</p>")
        self._text.append(formatted_msg)
        self._terminal.append(f"\033[92m{formatted_msg}\033[0m")

    def _orange(self, msg: str) -> None:
        formatted_msg = f"[~] {msg}"
        self._html.append(f"<p style='color: orange;'>{formatted_msg}</p>")
        self._text.append(formatted_msg)
        self._terminal.append(f"\033[93m{formatted_msg}\033[0m")

    def _red(self, msg: str) -> None:
        formatted_msg = f"[-] {msg}"
        self._html.append(f"<p style='color: red;'>{formatted_msg}</p>")
        self._text.append(formatted_msg)
        self._terminal.append(f"\033[91m{formatted_msg}\033[0m")

    def write(self, msg: str, color: str = "plain"):
        if color == "red":
            self._red(msg)
        elif color == "green":
            self._green(msg)
        elif color == "orange":
            self._orange(msg)
        else:  # plain
            self._plain(msg)

    def save_html(self, filename: str) -> None:
        """Save the logs in HTML format."""
        html_content = (
            "<!DOCTYPE html>\n"
            "<html lang='en'>\n"
            "<head>\n"
            "    <meta charset='UTF-8'>\n"
            "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
            "    <title>Test Results</title>\n"
            "</head>\n"
            "<body>\n"
            "    <h1>Test Results</h1>\n"
            "    <div>\n"
            f"        {'<br>\n'.join(self._html)}\n"
            "    </div>\n"
            "</body>\n"
            "</html>"
        )
        with open(filename, "w") as file:
            file.write(html_content)

    def save_text(self, filename: str) -> None:
        """Save the logs in plain text format."""
        with open(filename, "w") as file:
            file.write("\n".join(self._text) + "\n")

    def print_terminal(self) -> None:
        """Print the terminal-formatted logs to the console."""
        print("\n".join(self._terminal))


def okay(msg: str) -> str:
    """Returns '[+] {msg}' formatted in green"""
    return f"\033[92m[+] {msg}\033[0m"


def note(msg: str) -> str:
    """Returns '[~] {msg}' formatted in yellow"""
    return f"\033[93m[~] {msg}\033[0m"


def fail(msg: str) -> str:
    """Returns '[-] {msg}' formatted in red"""
    return f"\033[91m[-] {msg}\033[0m"
