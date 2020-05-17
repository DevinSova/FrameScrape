import json
import re


def parse_table(content):
    move = dict()

    # Work on the left column
    left_column = content.find("th")

    if content.find("big"):
        move["Name"] = content.find("big").text

    if content.find("small"):
        move["Comment"] = content.find("small").text

    move["Versions"] = list()

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
            new_move = dict(zip(headers, stats))
            new_moves.append(new_move)

        # Check if it's a description row
        # TODO: Should I just append all desc together or per version??å
        else:
            for new_move in new_moves:
                new_move["Description"] = re.sub('\n\n', '', stats_or_description[0].text).strip('\n')
            move["Versions"].extend(new_moves)
            new_moves = list()

        i += 1

    # Flush moves that never found description
    if len(new_moves) != 0:
        for new_move in new_moves:
            new_move["Description"] = "(No Description Available)"
        move["Versions"].extend(new_moves)

    return move
