import datetime
import sqlite3
import argparse
from typing import Dict
from multiprocessing import Pool

from _fast import check


def prepare_db(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS results(
            date text,
            iterations integer UNIQUE NOT NULL,
            number integer
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS meta (
            date text,
            last_number integer
        )
        """
    )

    conn.commit()


def load_results(conn: sqlite3.Connection) -> Dict[int, int]:
    cur = conn.cursor()

    return dict(
        cur.execute("""
            SELECT iterations, number FROM results;
        """)
    )


def load_last_number(conn: sqlite3.Connection) -> int:
    cur = conn.cursor()

    result = cur.execute("""
        SELECT max(last_number) AS last_number FROM meta;
    """).fetchone()[0]

    return 1 if result is None else result


def insert_result(conn: sqlite3.Connection, iterations: int, number: int) -> None:
    cur = conn.cursor()

    cur.execute(
        'INSERT INTO results (date, iterations, number) VALUES (?, ?, ?)',
        (datetime.datetime.now(), iterations, number)
    )


def insert_last_number(conn: sqlite3.Connection, last_number: int) -> None:
    cur = conn.cursor()

    cur.execute(
        'INSERT INTO meta (date, last_number) VALUES (?, ?)',
        (datetime.datetime.now(), last_number)
    )


def main():
    parser = argparse.ArgumentParser(description='Finds most delayed palindromes')
    parser.add_argument(
        '--database', '-d',
        dest='database',
        action='store',
        default='db.sqlite',
        help='path to the database file'
    )
    parser.add_argument(
        '--threads', '-t',
        dest='threads',
        type=int,
        action='store',
        default=1,
        help='number of threads'
    )
    parser.add_argument(
        '--numbers', '-n',
        dest='numbers',
        type=int,
        action='store',
        default=100000,
        help='number to check'
    )
    parser.add_argument(
        '--chunk-size', '-c',
        dest='chunk_size',
        type=int,
        action='store',
        default=1000,
        help='multiprocessing chunk size'
    )
    parser.add_argument(
        '--quiet', '-q',
        dest='quiet',
        action='store_const',
        const=True,
        default=False,
        help='quiet mode'
    )

    args = parser.parse_args()

    conn = sqlite3.connect(args.database)

    prepare_db(conn)

    results = load_results(conn)
    start = load_last_number(conn)
    end = start + args.numbers

    if not args.quiet:
        print(f'Start: {start}')
        print(f'End: {end}')
        print(f'Number of processes: {args.threads}')

    n_found = 0

    with Pool(args.threads) as pool:
        for number, iterations in zip(
                range(start, end),
                pool.imap(check, range(start, end), chunksize=args.chunk_size)
        ):
            if iterations == -1:
                continue

            if iterations not in results:
                results[iterations] = number
                n_found += 1
                insert_result(conn, iterations, number)

    insert_last_number(conn, end - 1)

    if not args.quiet:
        print(f'Found new numbers: {n_found}')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
