#!/bin/env python3

from os import mkdir
from time import time
from argparse import ArgumentParser
from Code import Poster, AguSession


def main(mail: str, password: str, directory: str = None) -> None:
    agu_session = AguSession(mail, password)
    agu_session.connect()
    poster_data = agu_session.enumerate_posters()
    posters = [Poster.hydrate(data) for data in poster_data]
    if not directory:
        directory = f"Posters_{round(time())}"
    mkdir(directory)
    [agu_session.download_poster(p, directory) for p in posters]
    return


def setup_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('-m', '--mail', required=True, type=str, help='The mail address used for the AGU account.')
    parser.add_argument('-p', '--password', required=True, type=str, help='Your AGU account password.')
    parser.add_argument('-d', '--directory', required=False, type=str,
                        help='A directory where to download posters. If not specified, a default one will be created.')
    return parser


if __name__ == '__main__':
    try:
        parser = setup_parser()
        args = parser.parse_args()
        main(args.mail, args.password, args.directory)
    except KeyboardInterrupt:
        pass
    exit(0)
