"""
Command line version of the delete function bookmarks.
"""
import click
import snoop
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


@click.command()
@click.argument("dlt")
# @snoop
def delete(dlt):
    """
    Function that deletes one, several or
    range of entries in the 'bkmks' database.\n
    You can call it with **bkdlt**, and use it in the following form:\n
    1. **Delete non sequential entries**. Surround the ids with quotation
       marks and separate them with a comma::

           bkdlt '435,436'

    2. **Delete sequential entries**. Envelop first and last ids with quotation
       marks and separate them with a dash::

           bkdlt '437-439'

       You may include spaces, but they'll be deleted by the application.\n
    3. **Delete single entry**. Write the id surrounded by quotation marks::

          bkdlt 66
    """

    split_lst = []
    if "," in dlt:
        # When inputing id strings to delete as a sole string, as it is convenient, MySQL
        # creates an error, since it expects a tuple of strings in the query. First we have
        # to split the id's at the comma. Splitting with space or space + comma doesn't work.
        lst = dlt.split(",")
        # Splitting creates empty spaces inside the strings. This eliminates them.
        nlst = [i.strip() for i in lst]
        # Finally we turn the list to tuple, the desired format by MySQL.
        nt = tuple(nlst)
        query = f"DELETE FROM bkmks WHERE id IN {nt}"
    if "-" in dlt:
        if " - " in dlt:
            answers = dlt.replace(" ", "")
            split_lst = answers.split("-")
        else:
            split_lst = dlt.split("-")
        query = f"DELETE FROM bkmks WHERE id BETWEEN {split_lst[0]} AND {split_lst[1]}"
    if "," not in dlt and "-" not in dlt:
        query = f"DELETE FROM bkmks WHERE id = {dlt}"

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    delete()
