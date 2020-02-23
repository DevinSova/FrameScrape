
def parse_moves_from_table(content):
    # print(content)

    for info in content.findAll(["tr", "th", "p", "b"]):
        print(info.text)

    # Needs to handle tables with 1 moves OR MORE!