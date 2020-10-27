import datetime
import sqlite3
import argparse
import time
from collections import ChainMap
from typing import Dict
from multiprocessing import Pool

from _fast import check, check_range


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

    return dict(cur.execute('SELECT iterations, number FROM results;'))


def load_last_number(conn: sqlite3.Connection) -> int:
    cur = conn.cursor()

    result = cur.execute('SELECT max(last_number) AS last_number FROM meta;').fetchone()[0]

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
    parser = argparse.ArgumentParser(description='Utility for search of the most delayed palindromes')
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
        help='number of numbers to check in one thread'
    )
    parser.add_argument(
        '--start', '-s',
        dest='start',
        type=int,
        action='store',
        default=None,
        help='overrides starting number'
    )
    parser.add_argument(
        '--quiet', '-q',
        dest='quiet',
        action='store_const',
        const=True,
        default=False,
        help='quiet mode'
    )
    parser.add_argument(
        '--results', '-r',
        dest='results',
        action='store_const',
        const=True,
        default=False,
        help='show results and exit'
    )
    parser.add_argument(
        '--benchmark', '-b',
        dest='benchmark',
        action='store_const',
        const=True,
        default=False,
        help='run benchmark while computing and display results'
    )

    args = parser.parse_args()

    assert args.threads > 0
    assert args.numbers > 0
    assert args.start >= 0 if args.start is not None else True

    conn = sqlite3.connect(args.database)

    prepare_db(conn)

    old_results = load_results(conn)

    if args.results:
        for iterations, result in sorted(old_results.items()):
            print(f'{iterations:8d} : {result:16d}')

        return

    new_results = {}
    all_results = ChainMap(old_results, new_results)

    start = args.start if args.start is not None else load_last_number(conn)

    ranges = []
    end = start
    for _ in range(args.threads):
        ranges.append((end, end + args.numbers))
        end += args.numbers

    if not args.quiet:
        print(f'Start: {start}')
        print(f'End: {end - 1}')
        print(f'Number of threads: {args.threads}')

    with Pool(args.threads) as pool:
        start_time = time.time()
        for res in pool.starmap(check_range, ranges, chunksize=1):
            for key, value in res.items():
                if key not in all_results:
                    new_results[key] = value
                    continue

                if value < all_results[key]:
                    new_results[key] = value
        elapsed_time = time.time() - start_time

    if args.benchmark:
        numbers_per_second = args.numbers / elapsed_time
        numbers_per_second_per_thread = numbers_per_second / args.threads
        print('Benchmark results:')
        print(f'    Total time: {elapsed_time:.3f} seconds')
        print(f'    Numbers per second: {int(numbers_per_second):d}')
        print(f'    Numbers per second per thread: {int(numbers_per_second_per_thread):d}')

    for key, value in new_results.items():
        insert_result(conn, key, value)

    insert_last_number(conn, end)

    if not args.quiet:
        print(f'Found new numbers: {len(new_results)}')

    conn.commit()
    conn.close()

    if not args.quiet:
        print('Bye')


if __name__ == '__main__':
    main()
