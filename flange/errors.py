class ActionFailureError(RuntimeError):
    "Inidicates rule action was taken BUT the test still fails"
    pass

class NoValidChoice(RuntimeError):
    "Indicates that a search returned zero valid options."
    pass
