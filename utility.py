import zlib
import hashlib
import re
import time
import pdb

def write_result(file_name, data):
    with open(file_name, 'w') as output:
        for item in data:
            try:
                num_1 = int(item[0][1:])
                num_2 = int(item[1][1:])

                if num_1 < num_2:
                    output.write("%s %s\n" % (item[0], item[1]))
                else:
                    output.write("%s %s\n" % (item[1], item[0]))
            except IndexError:
                print "Error when writing, check the format for data"
                pass

def read_result(file_name):
    set_result = set()
    with open(file_name) as f:
        for line in f:
            items = re.split('[\W]', line.strip())
            try:
                set_result.add((items[0], items[1]))
            except:
                print "Error in reading result file to compare"
                pass

    return set_result

def _string_hash(v, hashbits=32):
        "A variable-length version of Python's builtin hash. Neat!"
        if v == "":
            return 0
        else:
            x = ord(v[0])<<7
            m = 1000003
            mask = 2**hashbits-1
            for c in v:
                x = ((x*m)^ord(c)) & mask
            x ^= len(v)
            if x == -1:
                x = -2
            return x

hash_cache = dict()

def simhash(tokens):
    """
    return the 4-byte 32-bit simhash
    tokens : array : array of tokens
    """
    hashbits = 128
    result = [0 for i in range(hashbits)]
    for token in tokens:
        try:
            hash_value = hash_cache[token]
        except KeyError:
            hash_value = long(hashlib.md5(token).hexdigest(), 16)
            # hash_value = zlib.adler32(token)
            # hash_value = _string_hash(token, hashbits=hashbits)
            hash_cache[token] = hash_value
        for (i, bit) in enumerate(bin(hash_value)[2:]):
            if bit == "1":
                result[i] += 1
            else:
                result[i] -= 1

    string = ["0" for i in range(hashbits)]
    for (index, value) in enumerate(result):
        if value > 0:
            string[index] = "1"

    return long("".join(string), 2)

def checksum(content):
    return long(hashlib.md5(content).hexdigest(), 16)

def rotate_left(val, r_bits, max_bits):
    """
    http://www.falatic.com/index.php/108/python-and-bitwise-rotation
    """
    return (val << r_bits%max_bits) & (2**max_bits-1) | ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

def get_fingerprints_for_file(input_file, max_line = 10000):
    print "Loading news & calculating its fingerprints"

    t = time.time()

    ids                 = []
    fingerprint_values  = []
    checksum_values     = []
    regex = '[\W]+'

    count = 0
    with open(input_file) as f:
        for line in f:
            if count < max_line:
                separator_pos   = line.find(" ")
                _id             = line[:separator_pos]
                content         = line[separator_pos + 1:].lower()
                _news           = re.split(regex, content)

                ids.append(_id)
                fingerprint_values.append(simhash(_news))
                checksum_values.append(checksum(content))
                count += 1
            else:
                break

        print "**** Finish read_news: %f" % (time.time() - t)

    return ids, fingerprint_values, checksum_values