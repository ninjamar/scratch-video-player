def lzw_encode(data, dictionary = None, max_dict_size = 4096):
    # Adapted from tutorials and https://rosettacode.org/wiki/LZW_compression#Python
    if dictionary == None:
        size = 256
        dictionary = {chr(i): i for i in range(size)}
    else:
        size = len(dictionary)

    compressed = []
    string = ""

    for char in data:
        temp = string + char
        if temp in dictionary:
            string = temp
        else:
            compressed.append(dictionary[string])
            if len(dictionary) < max_dict_size:  # TODO: Max length
                dictionary[temp] = size
                size += 1
            string = char

    if string:
        compressed.append(dictionary[string])
    return compressed

def lzw_decode(compressed, dictionary = None, max_dict_size = 4096):
    if dictionary == None:
        size = 256
        dictionary = {i: chr(i) for i in range(size)}
    else:
        size = len(dictionary)

    # string = chr(compressed.pop(0))
    string = ""
    decompressed = string

    for code in compressed:
        if code in dictionary:
            entry = dictionary[code]
        else:  # code == dict_size
            entry = string + string[0]

        if len(dictionary) <= max_dict_size:
            decompressed += entry
            dictionary[size] = string + entry[0]
            
        size += 1
        string = entry

    return decompressed


if __name__ == "__main__":
    chars = "abcdefghijklmnopqrstuvwxyz!@#$%&^()*1234567890|"
    d = {x: i for i, x in enumerate(chars)}
    d[""] = len(d)

    text = "tobeornottobeortobeornot"
    c = lzw_encode(text, dictionary=d)
    print(c)
    d = lzw_decode(c, dictionary={v: k for k, v in d.items()})
    print(d)
    print(text == d)
