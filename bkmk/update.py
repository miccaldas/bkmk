"""
Command line version of the 'update' function for bkmks.
"""
import click
import snoop
from mysql.connector import Error, connect

# from snoop import pp


# def type_watch(source, value):
#     return f"type({source})", type(value)


# snoop.install(watch_extras=[type_watch])


@click.command()
@click.option("-i", "--ident", type=int)
@click.option("-c", "--column")
@click.option("-u", "--update", prompt=True)
# @snoop
def update(ident, column, update):
    """
    Called with **bkupdt**.\n
    **Options:**\n
    -i  Integer with the id value of the line we want to update.\n
    -c  String of the column's name we want to update.\n
    -u  Text that you want to change. it's a prompt. So just insert the other options and press
            *Enter* to access it.
    """

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
        cur = conn.cursor()
        query = f"UPDATE bkmks SET {column} = '{update}' WHERE id = {ident}"
        cur.execute(query)
        conn.commit()
        conn.close()
    except Error as e:
        err_msg = "Error while connecting to db", e
        print("Error while connecting to db", e)
        if err_msg:
            return query, err_msg

    return query


if __name__ == "__main__":
    update()
