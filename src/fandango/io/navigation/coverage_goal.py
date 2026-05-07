import enum


class CoverageGoal(enum.Enum):
    INPUTS = 0
    STATE_INPUTS = 1
    STATE_INPUTS_OUTPUTS = 2
    SINGLE_DERIVATION = 4
