# Define the 2D array
array = [
    [
        "-----\n" +
        "|   |\n" +
        "|   |\n" +
        "-----",
        "-----\n" +
        "|   |\n" +
        "|   |\n" +
        "-----"
    ],
    [
        "-----\n" +
        "|   |\n" +
        "|   |\n" +
        "-----",
        "-----\n" +
        "|   |\n" +
        "|   |\n" +
        "-----"
    ]
]

# Print the array
for row in array:
    # Split each string into lines
    lines = [string.split('\n') for string in row]

    # Get the maximum number of lines
    max_lines = max(len(line) for line in lines)

    # Print each line side by side
    for i in range(max_lines):
        for line in lines:
            # Print the line if it exists, otherwise print spaces
            print(line[i] if i < len(line) else '     ', end='   ')
        print()
