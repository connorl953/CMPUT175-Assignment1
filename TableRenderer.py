class TableRenderer:
    def __init__(self, table, chunk_width, chunk_height):
        self.table = table
        self.pretty_table = self.create_pretty_table(chunk_width, chunk_height)

    """
    Renders the timetable to the console,
    
    self.table is a 2D list of strings, 5 across and 18 down.
    Each string is a course name and location, or an empty string.
    
    """

    def render_table(self):

        print(self.pretty_table)
        self.print_pretty_table()

        pass

    def create_top_cell(self, class_name, class_location, chunk_width):

        string_builder = []

        string_builder.append("" + class_name.center(chunk_width) + "|\n")
        string_builder.append(class_location.center(chunk_width) + "|\n")
        string_builder.append("".center(chunk_width) + "|\n|")
        return ''.join(string_builder)

    def create_empty_cell(self, chunk_width):
        string_builder = []

        string_builder.append(" ".center(chunk_width) + "|\n")
        string_builder.append(" ".center(chunk_width) + "|\n")
        string_builder.append(" ".center(chunk_width) + "|\n")

        return ''.join(string_builder)

    def create_bottom_cell(self, chunk_width):
        string_builder = []
        string_builder.append(" ".center(chunk_width) + "|\n")
        string_builder.append(" ".center(chunk_width) + "|\n")
        string_builder.append(("-" * chunk_width).center(chunk_width) + "|\n")

        return ''.join(string_builder)

    def create_special_bottom_cell(self, chunk_width):
        string_builder = []
        string_builder.append(" ".center(chunk_width) + "|\n")
        string_builder.append(" ".center(chunk_width) + "|\n")
        string_builder.append(("-" * chunk_width).center(chunk_width) + "+\n")

        return ''.join(string_builder)

    def create_pretty_table(self, chunk_width, chunk_height):
        pretty_table = [["" for _ in range(5)] for _ in range(18)]
        table = self.table
        for y in range(len(self.table)):  # foreach row in table, but with indexes.
            for x in range(len(table[y])):  # foreach block in row, but with indexes.
                block = table[y][x]
                if block != "":
                    if x % 2 == 0:  # if x is even, then it must be monday wednesday or friday
                        pretty_table[y][x] = self.create_top_cell(block.split(" ")[0] + " " + block.split(" ")[1],
                                                                  block.split(" ")[2], chunk_width)
                        pretty_table[y + 1][x] = self.create_bottom_cell(chunk_width)
                    elif x % 2 == 1:  # if not, then it must be tuesday or thursday
                        pretty_table[y][x] = self.create_top_cell(block.split(" ")[0] + " " + block.split(" ")[1],
                                                                  block.split(" ")[2], chunk_width)
                        pretty_table[y + 1][x] = self.create_empty_cell(chunk_width)

                        # TODO: add a check to see if adjacent MWF blocks meet requirements for full line across

                        pretty_table[y + 2][x] = self.create_bottom_cell(chunk_width)
                    if y > 0:
                        pretty_table[y - 1][x] = self.create_bottom_cell(chunk_width)
                else:
                    if (pretty_table[y][x]) == "":
                        pretty_table[y][x] = self.create_empty_cell(chunk_width)

        return pretty_table

    def print_pretty_table(self):

        # TODO: Add times and dates to table

        print("+----------+----------+----------+----------+----------+")
        row = 0
        line = 0
        while line < len(self.pretty_table) * 3:
            print("|", end="")
            for string in self.pretty_table[row]:
                print(string.split("\n")[line - (row * 3)], end="")
            line += 1
            print()
            if (line % 3 == 0):
                row += 1

        print("+----------+----------+----------+----------+----------+")
        pass
