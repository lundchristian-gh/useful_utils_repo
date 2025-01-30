class ANSIColor:
    END: str = "\033[0m"
    RED: str = "\033[91m"
    GREEN: str = "\033[92m"
    YELLOW: str = "\033[93m"


class Document:
    def __init__(self) -> None:
        self._lines: list[tuple[str, str]] = []
        self._formats: list[str] = ["text"]
        self._color_map: dict[str, str] = {
            "plain": "",
            "red": ANSIColor.RED,
            "green": ANSIColor.GREEN,
            "yellow": ANSIColor.YELLOW,
        }

    def write(self, msg: str, color: str = "plain") -> None:
        if color not in self._color_map:
            color = "plain"
        self._lines.append((msg, color))

    def get_text(self) -> str:
        content: str = ""
        for msg, color in self._lines:
            ansi_color = self._color_map[color]
            content += f"{ansi_color}{msg}{ANSIColor.END if ansi_color else ''}\n"
        return content

    def save(self, filename: str, format: str = "text") -> None:
        if format not in self._formats:
            format = self._formats[0]
        content: str = ""
        if format == "text":
            content = self.get_text()
        with open(filename, "w") as file:
            file.write(content)

    def print(self) -> None:
        for msg, color in self._lines:
            ansi_color = self._color_map[color]
            print(f"{ansi_color}{msg}{ANSIColor.END if ansi_color else ''}")
