from PIL import Image

def Xor(bin1, bin2):
    num1 = int(bin1, 2)
    num2 = int(bin2, 2)
    result = num1 ^ num2
    return format(result, '08b')

def MiniDes(binary, key):
    key = "10101010"
    permutation = [0, 1, 3, 2, 3, 2, 4, 5]
    Sbox_1 = ["101", "010", "001", "110", "011", "100", "111", "000", "001", "100", "110", "010", "000", "111", "101", "011"]
    Sbox_2 = ["100", "000", "110", "101", "111", "001", "011", "010", "101", "011", "000", "111", "110", "010", "001", "100"]
    rounds = 8
    L, R = [], []
    
    L.append('0')
    L.append(binary[:6])
    R.append(binary[6:])
    
    for i in range(1, rounds):
        i_R = ''.join(R[i - 1][num % len(R[i - 1])] for num in permutation)
        length = len(key)
        i_key = key[i % len(key):] + key[:i % length]
        xor1 = Xor(i_R, i_key)
        
        xor1_bin1, xor1_bin2 = xor1[:4], xor1[4:]
        str1 = Sbox_1[int(xor1_bin1, 2)]
        str2 = Sbox_2[int(xor1_bin2, 2)]
        
        sbox_connect = str1 + str2
        
        RL = Xor(L[i], sbox_connect)[2:]
        R.append(RL)
        L.append(R[i - 1])

    return R[-1] + L[-1]

def CBC(plaintext, IV):
    key = "10101010"
    ciphertext = ''
    previous_block = IV

    blocks = [plaintext[i:i+6] for i in range(0, len(plaintext), 6)]
    for block in blocks:
        block_xor = Xor(block, previous_block)
        encrypted_block = MiniDes(block_xor, key)
        previous_block = encrypted_block
        ciphertext += encrypted_block

    return ciphertext

IV = '111011010010'
image = Image.open("zad8/obraz.pbm")
image_data = image.tobytes()
plaintext = ''.join(format(byte, '08b') for byte in image_data)

encoded_data = CBC(plaintext, IV)

encoded_bytes = bytes(int(encoded_data[i:i+8], 2) for i in range(0, len(encoded_data), 8))
encoded_image = Image.frombytes(image.mode, image.size, encoded_bytes)

encoded_image.show()