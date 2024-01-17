import logging
import pathlib
import sys
from contextlib import ContextDecorator


def create_log_file_path(file_path,
                         # root_dir='trcsvyt',
                         log_dir='log'):
    path_parts = list(pathlib.Path(file_path).parts)
    # relative_path_parts = path_parts[path_parts.index(root_dir) + 1:]
    # log_file_path = pathlib.Path(log_dir, *relative_path_parts)
    log_file_path = pathlib.Path(log_dir, *path_parts)
    log_file_path = log_file_path.with_suffix('.log')
    # Create the directories and the file itself
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    log_file_path.touch(exist_ok=True)
    return log_file_path


def config_logging(file_handle, file_path, mode='a', stream=sys.stdout,
                   level=logging.INFO, name='root'):
    logging_handlers = [OpenedFileHandler(file_handle, file_path, mode),
                        logging.StreamHandler(stream)]
    logging.basicConfig(
        handlers=logging_handlers,
        format='%(asctime)s %(name)s %(levelname)s %(message)s',
        level=level
    )
    logging.getLogger().root.name = name


class OpenedFileHandler(logging.FileHandler):

    def __init__(self, file_handle, filename, mode):
        self.file_handle = file_handle
        super(OpenedFileHandler, self).__init__(filename, mode)

    def _open(self):
        return self.file_handle


class StandardError:
    def __init__(self, buffer_stderr, buffer_file):
        self.buffer_stderr = buffer_stderr
        self.buffer_file = buffer_file

    def write(self, message):
        self.buffer_stderr.write(message)
        self.buffer_stderr.flush()
        self.buffer_file.write(message)
        self.buffer_file.flush()

    def writelines(self, messages):
        self.buffer_stderr.writelines(messages)
        self.buffer_stderr.flush()
        self.buffer_file.writelines(messages)
        self.buffer_file.flush()

    def flush(self):
        self.buffer_stderr.flush()
        self.buffer_file.flush()


class StandardOutput:
    def __init__(self, buffer_stdout, buffer_file):
        self.buffer_stdout = buffer_stdout
        self.buffer_file = buffer_file

    def write(self, message):
        self.buffer_stdout.write(message)
        self.buffer_stdout.flush()
        self.buffer_file.write(message)
        self.buffer_file.flush()

    def writelines(self, messages):
        self.buffer_stdout.writelines(messages)
        self.buffer_stdout.flush()
        self.buffer_file.writelines(messages)
        self.buffer_file.flush()

    def flush(self):
        self.buffer_stdout.flush()
        self.buffer_file.flush()


class Logger(ContextDecorator):
    def __init__(self, module_path, mode='a',
                 level=logging.INFO, name=None):
        self.module_path = module_path
        self.mode = mode
        self.level = level
        self.name = module_path if not name else name

        self.stdout_ = sys.stdout
        self.stderr_ = sys.stderr
        self.log_file_path = create_log_file_path(self.module_path)
        self.file_ = open(self.log_file_path, self.mode)
        config_logging(self.file_, self.log_file_path, self.mode, self.stdout_,
                       self.level, self.name)

    def __enter__(self):
        sys.stdout = StandardOutput(self.stdout_, self.file_)
        sys.stderr = StandardError(self.stderr_, self.file_)

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.stdout_
        sys.stderr = self.stderr_
        # self.file_.close()  # Leave closing unhandled intentionally
