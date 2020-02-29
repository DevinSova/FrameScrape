import json


def parse_table(content):
    moves = list()

    # images = content[0].find("th")
    move_info = content.find("td")

    print(move_info.text)

    rows = move_info.findAll("tr")

    headers = list()
    headers_html = rows[0].findAll("th")
    for header_html in headers_html:
        headers.append(header_html.text.replace('\n', ''))

    print("Rows = {}".format(len(rows)))
    for i in range(1, len(rows), 2):
        print("i = {}".format(i))
        values = list()
        values_html = rows[i].findAll(["th", "td"])
        for value_html in values_html:
            values.append(value_html.text.replace('\n', ''))

        #description = rows[i+1].text.replace('\n', '')
        #headers.append("Description")
        #values.append(description)

        moves.append(dict(zip(headers, values)))

    print(moves)
    return moves

    # Rows list
    # [0] Header Row
    # --------------------
    # [1] Move 1 Values
    # [2] Move 1 Desc
    # --------------------
    # [3] Move 2 Values
    # [4] Move 2 Desc
    # --------------------
    # ...

    # First th is the picture column
    # Then set of ths is the Header Row
    # Then 1 th for the move name
    # Then set of tds for the move properties
