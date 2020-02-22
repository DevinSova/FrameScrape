
def parse_moves_from_table(content):
    print(content)

    for move in content.findAll(["th", "p", "b"]):
        print(move.text)
