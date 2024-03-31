# Description: Compare two files and print the differences with color coding.

# can not compare word by word, but line by line
# perhaps word by word for each line can be done
# but i cannot know what line was inserted/deleted or edited
# need something like minimum edit required to convert one file to another

# cannot print red line after green line, adjacent ones might not be related
# they are related if you edited the original line
# if you added a new line, it is not related to the previous line
# similarly, if you deleted a line, it is not related to the next line

def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.replace('\n','') for line in file]


def compare_files(file1, file2):
    """Compare two files and return the diff matrix similar to LCS dp matrix."""
    diff = [[0] * (len(file2) + 1) for _ in range(len(file1) + 1)]
    for i1, line1 in enumerate(file1):
        for i2, line2 in enumerate(file2):
            if line1 == line2:
                diff[i1 + 1][i2 + 1] = diff[i1][i2] + 1
            else:
                diff[i1 + 1][i2 + 1] = max(diff[i1 + 1][i2], diff[i1][i2 + 1])
    return diff


def build_diff_index(diff):
    """Build the list of index of differences from the diff matrix."""
    cur_len = diff[-1][-1]
    i = len(diff) - 1
    j = len(diff[0]) - 1 
    diff_index = []

    while cur_len > 0:
        if diff[i][j] == cur_len:
            if diff[i - 1][j] == cur_len:
                i -= 1
            elif diff[i][j - 1] == cur_len:
                j -= 1
            else:
                diff_index.append((i, j))
                i -= 1
                j -= 1
                cur_len -= 1
            
    return list(reversed(diff_index))


def print_colored_diff(diff_index, file1, file2):
    """Print differences with color coding."""
    lasti = lastj = 0
    for i, j in diff_index:
        while lasti < i - 1:
            print_red("- " + file1[lasti])
            lasti += 1
        while lastj < j - 1:
            print_green("+ " + file2[lastj])
            lastj += 1
        print("  " + file1[i - 1])
        lasti = i
        lastj = j


def print_colored_diff_line_by_line(diff_index, file1, file2):
    """Print differences with color coding."""
    lasti = lastj = 0
    cur_diff_index = 0

    while cur_diff_index < len(diff_index):
        curi, curj = diff_index[cur_diff_index]
        if lasti < curi-1:
            print_red("- " + file1[lasti])
            lasti += 1
        if lastj < curj-1:
            print_green("+ " + file2[lastj])
            lastj += 1
        if lasti == curi-1 and lastj == curj-1:
            print("  " + file1[curi - 1])
            lasti = curi
            lastj = curj
            cur_diff_index += 1
        

def print_red(s, end="\n"):
    print("\033[91m" + s + "\033[0m", end=end)


def print_green(s, end="\n"):
    print("\033[1;92m" + s + "\033[0m", end=end)


if __name__ == "__main__":
    file1 = read_file('./old_file.txt')
    file2 = read_file('./new_file.txt')
    diff = compare_files(file1, file2)
    # for i in range(-1,len(file2)):
    #     print(i,end="  ")
    # print()
    # for i,d in enumerate(diff):
    #     print(i,d)

    diff_index = build_diff_index(diff)
    # print(diff_index)
    
    print_colored_diff(diff_index, file1, file2)
