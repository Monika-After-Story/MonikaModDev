
import renpy as Renpy

from .masimport import MASImport


class MASImport_certifi(MASImport):
    """
    certifi import
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__("certifi")

    def import_try(self, renpy: Renpy = None):
        import certifi
        return True


class MASImport_ssl(MASImport):
    """
    SSL Import
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__("ssl")

    def import_try(self, renpy: Renpy = None):
        import ssl
        return True