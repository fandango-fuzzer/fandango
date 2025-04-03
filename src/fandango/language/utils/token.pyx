cdef class Token:
    cdef tuple source = None
    cdef int type = 0
    cdef int start = -1
    cdef int stop = -1
    cdef int index = -1
    cdef int line = -1
    cdef int column = -1
    cdef str _text = None

    cdef int EOF = -1
    cdef int INVALID = 0

    property text:
        def __get__(self):
            return self._text
        def __set__(self, str value):
            self._text = value

    cdef str get_token_source(self):
        return self.source[0]

    cdef get_input_stream(self):
        return self.source[1]

cdef class CommonToken(Token):
    cdef tuple EMPTY_SOURCE = (None, None)

    def __init__(self, tuple source = EMPTY_SOURCE, int type = -1, int start = -1, int stop = -1):
        self.source = source
        self.type = type
        self.start = start
        self.stop = stop

    cdef CommonToken clone(self):
        t = CommonToken(self.source, self.type, self.start, self.stop)
        t.index = self.index
        t.line = self.line
        t.column = self.column
        t.text = self.text
        return t

    property text:
        def __get__(self):
            if self._text is None:
                self._text = self.get_input_stream().get_text(self.start, self.stop)
            return self._text
        def __set__(self, str value):
            self._text = value