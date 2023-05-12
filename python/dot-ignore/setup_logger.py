import logging

default_date_format = '%H:%M:%S'
debug_date_format = '%Y.%m.%d %H:%M:%S.uuu'


def setup_logging(debug_mode: bool = False):
    __setup_logger__(debug_mode, debug_date_format if debug_mode else default_date_format)


def __setup_logger__(debug_mode: bool, date_format: str):
    print('initializing logger')

    level = logging.DEBUG if debug_mode else logging.INFO

    logging.basicConfig(level=level,
                        format='%(asctime)s - %(levelname)-8s - %(name)s: %(message)s',
                        datefmt=date_format)
