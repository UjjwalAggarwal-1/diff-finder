# Description: Compare two files and print the differences with color coding.

def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line for line in file]


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
        cur_missing = []
        cur_added = []
        while lasti < i - 1:
            cur_missing.append(file1[lasti])
            lasti += 1
        while lastj < j - 1:
            cur_added.append(file2[lastj])
            lastj += 1
        

        print_2(cur_missing, cur_added)

        print(file1[i - 1], end = "")
        lasti = i
        lastj = j

    if lasti < len(file1):
        print_red("-",end="")
    while lasti < len(file1):
        print_red(file1[lasti])
        lasti+=1
    if lastj < len(file2):
        print_green("+", end="")
    while lastj < len(file2):
        print_green(file2[lastj])
        lastj+=1

def print_2(cur_missing, cur_added):
    cur_missing_words = [char for line in cur_missing for char in line]
    cur_added_words = [word for line in cur_added for word in line]
    diff_index = build_diff_index(compare_files(cur_missing_words, cur_added_words))
    lasti = lastj = 0
    for i, j in diff_index:
        if lasti< i-1:
            print_red("-", end="")
        while lasti < i - 1:
            print_red(cur_missing_words[lasti], end="")
            lasti += 1
        if lastj<j-1:
            print_green("+", end="")
        while lastj < j - 1:
            print_green(cur_added_words[lastj], end="")
            lastj += 1

        print(cur_missing_words[i-1], end = "")
        lasti = i
        lastj = j

    if lasti< len(cur_missing_words):
        print_red("-", end="")
    while lasti < len(cur_missing_words):
        print_red(cur_missing_words[lasti], end="")
        lasti += 1
    if lastj< len(cur_added_words):
        print_green("+", end="")
    while lastj < len(cur_added_words):
        print_green(cur_added_words[lastj], end="")
        lastj += 1
        

def print_red(s, end="\n"):
    print("\033[41m" + s + "\033[0m", end=end)


def print_green(s, end="\n"):
    print("\033[1;42m" + s + "\033[0m", end=end)


if __name__ == "__main__":
    file1 = read_file('./old_file.txt')
    file2 = read_file('./new_file.txt')
    diff = compare_files(file1, file2)
   
    diff_index = build_diff_index(diff)
    
    print_colored_diff(diff_index, file1, file2)
