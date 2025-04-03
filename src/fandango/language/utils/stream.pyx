from fandango.language.utils.token import Token

cdef class InputStream:
    cdef int _index = 0
    cdef int _size = 0
    cdef str data = None

    def __init__(self, str data):
        self.data = data
        self._size = len(data)

    property index:
        def __get__(self):
            return self._index

    property size:
        def __get__(self):
            return self._size

    cdef reset(self):
        self._index = 0

    cdef char LA(self, int offset):
        if offset == 0:
            return 0
        if offset < 0:
            offset += 1
        pos = self._index + offset - 1
        if pos < 0 or pos >= self._size:
            return Token.EOF
        return self.data[pos]

    cdef char LT(self, int offset):
        return self.LA(offset)

    cdef seek(self, int index):
        if index < self._index:
            self._index = index
        else:
            self._index = min(index, self._size)

    cdef get_text(self, int start, int stop):
        if stop >= self._size:
            stop = self._size - 1
        if start >= self._size:
            return ""
        return self.data[start:stop + 1]

