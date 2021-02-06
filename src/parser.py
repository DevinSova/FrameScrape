import json
import re
from urllib.parse import urlparse


def parse_move_table(content, domain, name):
    move = dict()

    move["Name"] = name
    # TODO Move Input move["Input"] = None

    attack_gallery = content.find("div", {"class": "attack-gallery"})
    attack_info = content.find("div", {"class": "attack-info"})

    # ------------------------------------------------------------------------
    # attack_data_rows
    # ------------------------------------------------------------------------
    attack_data_rows = attack_info.findAll("tr")
    move["Versions"] = list()

    # Safety
    if attack_data_rows:

        # Grab the headers (first row is always header)
        headers = list()
        headers_html = attack_data_rows[0].findAll("th")
        for header_html in headers_html:
            headers.append(header_html.find(text=True).replace('\n', '').strip())

        # Parse the data (everything after first row)
        versions = list()
        i = 1
        while i < len(attack_data_rows):
            version = dict()
            stats = list()
            attack_data_cells = attack_data_rows[i].findAll(["th", "td"])
            for stat in attack_data_cells:
                stats.append(stat.text.replace('\n', '').strip())
            version["Attributes"] = dict(zip(headers, stats))
            move["Versions"].append(version)
            i += 1

    # ------------------------------------------------------------------------
    # attack_data_descriptions
    # ------------------------------------------------------------------------
    attack_data_descriptions = [attack.text for attack in attack_info.findAll("p")]

    # TODO: Fix by looking at <br> tag

    # Safety
    if len(move["Versions"]) == 0:
        pass

    # if move count == description count map them
    elif len(attack_data_descriptions) == len(move["Versions"]):
        for i in range(len(move["Versions"])):
            move["Versions"][i]["Description"] = attack_data_descriptions[i]

    # else all go to last element
    else:
        move["Versions"][-1]["Description"] = "\n".join(attack_data_descriptions)

    # ------------------------------------------------------------------------
    # attack_gallery
    # ------------------------------------------------------------------------
    imageURLs = [domain + img["src"] for img in attack_gallery.findAll("img")]

    # TODO: Grab Text

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


# Move Name <b> (Could be input name)
# Input Name <b> (optional)
# ------------------------------------------------------------------
# | Img 1    | Version | Damage | Guard | Startup | Active | Recov.| headers (attack_data_rows[0])
# |          |------------------------------------------------------
# |          | 5A      | 100    | All   | 5       | 3      | 5     | attack_data_rows[1]
# |          |------------------------------------------------------
# | Img 2    | 5AA     | 120    | All   | 6       | 4      | 6     | attack_data_rows[2]
# |          |------------------------------------------------------
# |          |                                                     |
# |          | Description for 5A                                  | attack_data_descriptions[0]
# | Img 3    |                                                     |
# |          | Description for 5AA                                 | attack_data_descriptions[1]
# |          |                                                     |
# |          |                                                     |
# ------------------------------------------------------------------
#   ^attack_gallery              ^attack_info
#   <div class="attack-gallery"> <div class="attack-info">
