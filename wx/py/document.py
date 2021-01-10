"""Document class."""

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"

import os


class Document:
    """Document class."""

    def __init__(self, filename=None):
        """Create a Document instance."""
        self.filename = filename
        self.filepath = None
        self.filedir = None
        self.filebase = None
        self.fileext = None
        if self.filename:
            self.filepath = os.path.realpath(self.filename)
            self.filedir, self.filename = os.path.split(self.filepath)
            self.filebase, self.fileext = os.path.splitext(self.filename)

    def read(self):
        """Return contents of file."""
        if self.filepath and os.path.exists(self.filepath):
            with open(self.filepath, 'rb') as f:
                return f.read().decode('utf-8')
        return ''

    def write(self, text):
        """Write text to file."""
        with open(self.filepath, 'wb') as f:
            try:  # Convert from unicode to bytes
                text = text.encode('utf-8')
                f.write(text)
            except AttributeError:
                pass
