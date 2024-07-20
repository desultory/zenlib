__author__ = "desultory"
__version__ = "1.0.0"


class DictCheck:
    """
    Expects the class has self.logger and is a dict.
    Mixin class for checking dict keys.
    """

    def _return_check(self, message, raise_exception, log_level, return_val=None):
        if raise_exception:
            raise ValueError(message)
        self.logger.log(log_level, message)
        return return_val

    def _dict_contains(self, key, message=None, is_set=True, raise_exception=False, log_level=10, debug_level=5):
        """
        Checks if the dict contains a key.
        if is_set is true, checks that the key is to something other than None.
        """
        self.logger.log(debug_level, "[%s] Checking dict key: %s" % (self.__class__.__name__, key))
        if key not in self:
            return self._return_check(message or "[%s] Unable to find key: %s." % (self.__class__.__name__, key), raise_exception, log_level)

        if is_set and not self[key]:
            return self._return_check(message or "[%s] Key is not set: %s." % (self.__class__.__name__, key), raise_exception, log_level)

