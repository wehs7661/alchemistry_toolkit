class ParameterError(Exception):
    """
    An error due to improperly specified parameters has been deteced.
    """
    pass

class SimulationTypeError(Exception):
    """
    A simulation type that the method is not applicable to has been detected.
    """
    pass

class InputFileError(Exception):
    """
    An error indicating that the input file was not properly specified.
    """
    pass
