import db.files
from ed_logging.logger import defaultLogger as log


class EDCommandHandler(object):
    @staticmethod
    def handle_list_files_cmd():
        log.debug("Handling list all files command")
        files = db.files.get_all()
        for file in files:
            log.info(file)
