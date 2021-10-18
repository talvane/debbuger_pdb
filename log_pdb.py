import functools
from logging import getLogger, basicConfig, DEBUG
import sys
from pdb import post_mortem

basicConfig(filename='test.log',
            filemode='w',
            level=DEBUG)

log = getLogger(__name__)


def debug():
    def tail_log(func):
        @functools.wraps(func)
        def execute_func(*args):
            try:
                func(*args)
            except Exception as error:
                log.info('{} args:{} error:{}'.format(func.__name__,
                                                      args,
                                                      error))
                for line in open('test.log'):
                    print(line)

                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno

                print("\nException type: ", exception_type)
                print("File name: ", filename)
                print("Line number: ", line_number)

                print("Line origin: ", exception_traceback.tb_next.tb_lineno)
                print("Parameters: ", exception_traceback.tb_next.tb_frame.f_locals)
                
                post_mortem(sys.exc_info()[2])
        return execute_func
    return tail_log


@debug()
def div(x, y):
    log.info('Entrei na função {}'.format(div.__name__))
    return x / y


div(2, 0)
