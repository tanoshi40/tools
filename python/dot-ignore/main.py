import argparse
import enum
import logging
import os

import setup_logger
from excluder import Excluder

logger = None


def main(args):
    logger.info('validating parameters')

    path = args.path
    template_path = args.ignore
    mode = args.mode

    if not os.path.exists(path):
        logger.error(f'path "{path}" does not exist')

    if not os.path.exists(template_path):
        logger.error(f'ignore file "{template_path}" does not exist')

    ex = Excluder.build(template_path, os.path.basename(template_path))

    if mode == Mode.LIST:
        logger.info(f'excluded files in "{path}" for "{template_path}"')
        for excluded in ex.find_excluded(path):
            logger.info(f'- {excluded}')

    # elif mode == Mode.ERASE:
    #     pass

    else:
        logger.error(f'Mode {mode} not supported yet')

    return 0


class Mode(enum.Enum):
    LIST = 'list',
    ERASE = 'erase'


def cli():
    print('initializing arguments')

    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--path', type=str, default='./',
                        help='The target path')
    parser.add_argument('-i', '--ignore', type=str, default='.gitignore',
                        help='The ignore file. (follows .gitignore rules)')
    parser.add_argument('-m', '--mode', type=lambda mode: Mode[mode], choices=list(Mode), default=Mode.LIST,
                        help='LIST -> lists all ignored dirs and files'
                             '\nERASE -> deletes all ignored dirs and files')

    parser.add_argument('-d', '--debug', action='store_true', default=False,
                        help='If enabled some debugging steps including debug log-level for this application will be '
                             'enabled')

    return parser.parse_args()


if __name__ == '__main__':
    cli_args = cli()

    setup_logger.setup_logging(cli_args.debug)
    logger = logging.getLogger('main')
    exit_code = main(cli_args)

    logger.info(f'Finished script with exit_code: {exit_code}')

    exit(exit_code)
