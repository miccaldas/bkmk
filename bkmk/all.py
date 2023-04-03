"""
Shows all content on the bkmks database.
"""
import click
import snoop
from blessed import Terminal
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


@click.command()
@click.option("-n", "--number", type=int)
# @snoop
def all(number):
    """
    Invoked as **bkall**. With no arguments, it prints all
    content on the database.\n
    **Options:**\n
    -n  Number of latest entries to show. Prints 'n' amount of new entries, thusly:\n
    **bkall -n 4**
    """

    term = Terminal()

    query = "SELECT * FROM bkmks"
    if number:
        query = f"SELECT * FROM bkmks ORDER BY id DESC LIMIT {number}"
    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
        cur = conn.cursor()
        cur.execute(query)
        records = cur.fetchall()
    except Error as e:
        print("Error while connecting to the db", e)
    finally:
        if conn:
            conn.close()

    for record in records:
        record = (
            term.bold(str(record[0])),
            term.bold(record[1]),
            term.bold(record[2]),
            term.red_bold(record[3]),
            term.bold(record[4]),
            term.bold(record[5]),
            term.bold(record[6]),
            term.bold(record[7].strftime("%d-%m-%Y_%H:%M")),
            term.bold("--------------------------------------------------------------------"),
        )

        for line in record:
            print("\n".join(term.wrap(line, width=145, initial_indent=" " * 40)))


if __name__ == "__main__":
    all()
