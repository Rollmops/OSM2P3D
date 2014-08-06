import mmap
import zlib
from struct import unpack

header_format = {'blob_header_length': (0, 3, ">L")}


class OSMFile(object):
    def __init__(self, filename):
        self.header = {}

        self.filename = filename

        self.file = open(filename, "r+b")
        self.mm = mmap.mmap(self.file.fileno(), 0)

        for key, values in header_format.items():
            if values[2] is not None:
                self.header[key] = unpack(values[2], self.mm[values[0]:values[1] + 1])[0]
            else:
                self.header[key] = self.mm[values[0]:values[1] + 1]





    def __del__(self):
        self.file.close()

