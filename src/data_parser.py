import json
import re
from urllib.parse import urlparse


def parse_move_table(content, domain):
    move = dict()

    # Work on the left column
    left_column = content.find("th")

    if left_column.find("big"):
        move["Name"] = left_column.find("big").text

    if left_column.find("small"):
        move["Comment"] = left_column.find("small").text

    # Work on the rows
    move["Versions"] = list()

    rows = content.find("td").findAll("tr")

    # Grab the headers
    headers = list()
    headers_html = rows[0].findAll("th")
    for header_html in headers_html:
        headers.append(header_html.find(text=True).replace('\n', ''))

    # Parse the rest of the rows
    found_versions = list()
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
            version = dict()
            version["Attributes"] = dict(zip(headers, stats))
            found_versions.append(version)

        # Check if it's a description row
        else:
            for version in found_versions:
                version["Description"] = re.sub('\n\n', '', stats_or_description[0].text).strip('\n')
            move["Versions"].extend(found_versions)
            found_versions = list()

        i += 1

    # Flush moves that never found description
    if len(found_versions) != 0:
        for version in found_versions:
            version["Description"] = "(No Description Available)"
        move["Versions"].extend(found_versions)

    # Work on images
    imageURLs = [domain + img["src"] for img in left_column.findAll("img")]

    # Safety
    if len(move["Versions"]) == 0:
        pass

    # if move count == image count map them
    elif len(imageURLs) == len(move["Versions"]):
        for i in range(len(move["Versions"])):
            move["Versions"][i]["ImageURLs"] = [imageURLs[i]]

    # else all go to last element
    else:
        move["Versions"][-1]["ImageURLs"] = imageURLs

    return move
