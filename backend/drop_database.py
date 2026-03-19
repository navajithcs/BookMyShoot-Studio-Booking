"""
drop_database.py

Utility to drop the remote MySQL/MariaDB `bookmyshoot` database.

USAGE (recommended): Set environment variable `MYSQL_PASSWORD` then run:

    python drop_database.py --user root --host localhost

The script will prompt for confirmation before dropping the database.

WARNING: This will permanently delete the database and all data.
"""
import os
import argparse
import getpass
import pymysql


def drop_db(host, user, password, db_name="bookmyshoot"):
    conn = None
    try:
        conn = pymysql.connect(host=host, user=user, password=password)
        conn.autocommit(True)
        cur = conn.cursor()
        print(f"Dropping database '{db_name}' on {host} as {user}...")
        cur.execute(f"DROP DATABASE IF EXISTS `{db_name}`;")
        print("Success: database dropped (if it existed).")
    except Exception as e:
        print("Error:", e)
    finally:
        if conn:
            conn.close()


def main():
    parser = argparse.ArgumentParser(description="Drop remote MySQL/MariaDB database")
    parser.add_argument("--host", default="localhost", help="DB host (default: localhost)")
    parser.add_argument("--user", default="root", help="DB user (default: root)")
    parser.add_argument("--db", default="bookmyshoot", help="Database name (default: bookmyshoot)")
    args = parser.parse_args()

    env_pass = os.getenv("MYSQL_PASSWORD")
    if env_pass:
        password = env_pass
    else:
        password = getpass.getpass(prompt=f"Password for {args.user}@{args.host}: ")

    confirm = input(f"Are you sure you want to DROP database '{args.db}' on {args.host}? (yes/NO): ")
    if confirm.lower() != "yes":
        print("Aborted: database will NOT be dropped.")
        return

    drop_db(args.host, args.user, password, db_name=args.db)


if __name__ == "__main__":
    main()
