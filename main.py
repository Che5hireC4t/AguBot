#!/bin/env python3

from os import mkdir
from time import time, sleep
from argparse import ArgumentParser
from Code import Poster, AguSession, Database


def main(mail: str, password: str, directory: str = None) -> None:
    agu_session = AguSession(mail, password)
    agu_session.connect()
    poster_data = agu_session.enumerate_posters()
    if not directory:
        directory = f"Posters_{round(time())}"
    mkdir(directory)
    db = Database(f"{directory}/database.csv")
    for data in poster_data:
        poster = Poster.hydrate(data)
        section = poster.metadata.section
        if not section:
            section = 'Orphaned'
        section_directory = f"{directory}/{section}"
        try:
            mkdir(section_directory)
        except FileExistsError:
            pass
        # Dirty, but I am in rush and no time for clean code. To be improved.
        try:
            agu_session.download_poster(poster, section_directory)
        except Exception:
            sleep(60)
            try:
                agu_session.download_poster(poster, section_directory)
            except Exception:
                sleep(60)
                try:
                    agu_session.download_poster(poster, section_directory)
                except Exception:
                    continue
        db.write_database(poster.get_csv_data())
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
