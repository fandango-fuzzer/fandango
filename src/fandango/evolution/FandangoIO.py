from fandango.evolution.algorithm import Fandango


class FandangoIO(Fandango):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def fuzz_io(self):
        pass