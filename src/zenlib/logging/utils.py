# Common function for checking if a logger has a handler already
def _logger_has_handler(logger):
    while logger:
        if logger.handlers:
            return True
        logger = logger.parent
    return False

