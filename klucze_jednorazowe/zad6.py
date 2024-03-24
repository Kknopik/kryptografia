def Xor(txt1, txt2):
    ascii1 = [ord(i) for i in txt1]
    ascii2 = [ord(i) for i in txt2]
    
    xor = ""
    for i in range(len(ascii1)):
        xor_num = ascii1[i] ^ ascii2[i]
        if 32 < xor_num < 127:
            xor += chr(xor_num)
        else:
            xor += "\\x{:02x}".format([xor_num][0])            
        
    return xor    
    
txt1 = input()
txt2 = input()

result = Xor(txt1, txt2)
print(result)