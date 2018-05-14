class SlimleafException(Exception):
    """Base exception class for all Slimleaf Exceptions

    A customized exception highlights the fact that a particular exception arose from
    the test framework, and is therefore less likely to indicate an actual problem with
    the product under test.
    """

    pass
