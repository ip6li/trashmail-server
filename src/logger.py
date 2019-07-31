import pwd
import getpass
import logging
import logging.config


class Logger:

    __not_found_already_sent = False

    @staticmethod
    def __send_config_msg(msg):
        if not Logger.get_notify_state():
            print(msg)
            Logger.set_notify_state(True)

    def __init__(self, name):
        log_conf_file = pwd.getpwnam(getpass.getuser()).pw_dir + "/.trashmail/logging.ini"
        try:
            logging.config.fileConfig(log_conf_file)
            Logger.__send_config_msg("using log config " + log_conf_file)
        except Exception as err:
            Logger.__send_config_msg(log_conf_file + " not found, using defaults: " + str(err))
        self.logger = logging.getLogger(name)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def crit(self, msg):
        self.logger.critical(msg)

    @staticmethod
    def get_notify_state():
        return Logger.__not_found_already_sent

    @staticmethod
    def set_notify_state(state):
        Logger.__not_found_already_sent = state
