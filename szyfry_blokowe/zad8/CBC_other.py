from PIL import Image

def IR(binary, permutation):
    result = ""
    for num in permutation:
        result += binary[num]
        
    return result

def IKey(key, i):
    return key[i % len(key):] + key[:i % len(key)]

def Xor(bin1, bin2):
    num1 = int(bin1, 2)
    num2 = int(bin2, 2)
    
    result = num1 ^ num2
    
    return format(result, '08b')

def CBC(binary_data, IV):
    key = "10101010"
    permutation = [0, 1, 3, 2, 3, 2, 4, 5]
    Sbox_1 = ["101", "010", "001", "110", "011", "100", "111", "000", "001", "100", "110", "010", "000", "111", "101", "011"]
    Sbox_2 = ["100", "000", "110", "101", "111", "001", "011", "010", "101", "011", "000", "111", "110", "010", "001", "100"]
    rounds = 8
    L, R = [], []
    
    L.append(IV)
    R.append(binary_data[:6])
    
    for i in range(1, rounds):
        i_R = IR(R[i - 1], permutation)
        i_key = IKey(key, i)
        xor1 = Xor(i_R, i_key)
        
        xor1_bin1, xor1_bin2 = xor1[:4], xor1[4:]
        str1 = Sbox_1[int(xor1_bin1, 2)]
        str2 = Sbox_2[int(xor1_bin2, 2)]
        
        sbox_connect = str1 + str2
        
        RL = Xor(L[i-1], sbox_connect)[2:]
        R.append(RL)
        L.append(R[i - 1])

    return R[-1] + L[-1]

image = Image.open("zad8/obraz.png")
#image = Image.open("zad8/obraz.jpg")
#image = Image.open("zad8/obraz.gif")
image = image.convert("L")
binary_data = ''.join(format(pixel, '08b') for pixel in image.tobytes())

while len(binary_data) % 12 != 0:
    binary_data += '0'

IV = '110011'
encrypted_data = ""
    
for i in range(0, len(binary_data), 12):
    block = binary_data[i:i+12]
    encrypted_block = CBC(block, IV)
    IV = encrypted_block
    encrypted_data += encrypted_block

encrypted_image = Image.frombytes("L", image.size, bytes(int(encrypted_data[i:i+8], 2) for i in range(0, len(encrypted_data), 8)))
encrypted_image.show()