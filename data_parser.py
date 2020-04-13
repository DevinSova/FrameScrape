import json


def parse_table(content):
    moves = list()

    # images = content[0].find("th")

    move_info = content.find("td")

    rows = move_info.findAll("tr")

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
            new_moves.append(dict(zip(headers, stats)))

        # Check if it's a description row
        else:
            for new_move in new_moves:
                new_move["Description"] = stats_or_description[0].text  # TODO: Fix \n at start and end of Description
            moves.extend(new_moves)
            new_moves = list()

        i += 1

    # Flush moves that never found description
    if len(new_moves) != 0:
        for new_move in new_moves:
            new_move["Description"] = "(No Description Available)."
        moves.extend(new_moves)

    return moves
