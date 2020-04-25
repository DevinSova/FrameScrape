import json
import re


def parse_table(content):
    moves = list()

    # Work on the left column
    left_column = content.find("th")

    move_name = None
    move_input = None

    if content.find("big"):
        move_name = content.find("big").text

    if content.find("small"):
        move_input = content.find("small").text

    # Work on the rows
    rows = content.find("td").findAll("tr")

    # Grab the headers
    headers = list()
    headers_html = rows[0].findAll("th")
    for header_html in headers_html:
        headers.append(header_html.text.replace('\n', ''))

    # Parse the rest of the rows
    new_moves = list()
    i = 1
    while i < len(rows):
        stats_or_description = rows[i].findAll(["th", "td"])

        # Skip extra header rows (Chie Page has it. Idk why)
        if stats_or_description[0].text == "Version\n":
            pass

        # Check if it's a stat row
        elif len(stats_or_description) != 1:
            stats = list()
            for stat in stats_or_description:
                stats.append(stat.text.replace('\n', ''))
            new_move = dict()
            if move_name is not None:
                new_move["Name"] = move_name
            if move_input is not None:
                new_move["Comment"] = move_input
            new_move.update(zip(headers, stats))
            new_moves.append(new_move)

        # Check if it's a description row
        else:
            for new_move in new_moves:
                # TODO: Fix \n at end and start of P4AU Descs
                new_move["Description"] = re.sub('\n\n', '', stats_or_description[0].text)
            moves.extend(new_moves)
            new_moves = list()

        i += 1

    # Flush moves that never found description
    if len(new_moves) != 0:
        for new_move in new_moves:
            new_move["Description"] = "(No Description Available)."
        moves.extend(new_moves)

    return moves
