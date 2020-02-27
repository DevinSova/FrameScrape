
def parse_moves_from_table(content):
    # print(content.text)

    images = content.find("th")
    move_info = content.find("td")

    print(move_info.text)

    rows = move_info.findAll("tr")

    headers = list()

    headers_html = rows[0].findAll("th")

    for header_html in headers_html:
        headers.append(header_html.text.replace('\n', ''))

    print(headers)

    # Needs to handle tables with 1 moves OR MORE!

    # First th is the picture column
    # Then set of ths is the Header Row
    # Then 1 th for the move name
    # Then set of tds for the move properties
