class Shaker():
    """
    An infamous salt shaker
    """

    def __init__(self, doses=100):
        """
        Object initialization
        :param doses: the number of doses contained
        """
        self.__doses = doses

    def shake(self) -> int:
        """
        Serve a dose
        """
        if self.__doses == 0:
            return 0
        self.__doses -= 1
        return 1

    @property
    def remaining(self):
        return self.__doses