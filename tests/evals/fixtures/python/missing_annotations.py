from loguru import logger


class FileProcessor:
    """
    A simple class to process text files line by line.
    Demonstrates logging, error handling, and docstrings,
    but intentionally omits type annotations (violates PY002).
    """

    def __init__(self, file_path: str):
        """
        Initialize the processor with a file path.
        """
        self.file_path = file_path

    def read_lines(self, strip_newlines: bool = True):
        """
        Read lines from the file and optionally strip newlines.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            logger.info(f"Successfully read {len(lines)} lines from {self.file_path}")
            if strip_newlines:
                return [line.strip() for line in lines]
            return lines
        except FileNotFoundError as e:
            logger.error(f"File not found: {self.file_path}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error while reading {self.file_path}: {e}")
            raise e
