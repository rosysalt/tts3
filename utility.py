import zlib

def write_result(file_name, data):
    with open(file_name, 'w') as output:
        for item in data:
            try:
                output.write("%s\t%s\n" % (item[0], item[1]))
            except IndexError:
                print "Error when writing, check the format for data"
                pass

def simhash(tokens):
    """
    return the 4-byte 32-bit simhash
    tokens : array : array of tokens
    """
    result = [0 for i in range(32)]
    for token in tokens:
        hash_value = zlib.adler32(token)

        for (i, bit) in enumerate(bin(hash_value)[2:]):
            if bit == "1":
                result[i] += 1
            else:
                result[i] -= 1

    string = ["0" for i in range(32)]
    for (index, value) in enumerate(result):
        if value > 0:
            string[index] = "1"

    return int("".join(string), 2)
