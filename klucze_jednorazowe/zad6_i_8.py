def ToAscii(txt):
    if chr(92) in txt:    
        split_txt = txt.split("\\")
        if split_txt[0] == "":
            split_txt.pop(0)
        print(split_txt)    
        fixed_split = []
        for i in split_txt:
            if i[0] == "x":
                fixed_split.append(i[0:3])
                fixed_split += list(i[3:])
            else:
                fixed_split += i
        print(fixed_split)
        chars = []
        for i in fixed_split:
            if i[0] == "x":
                chars += (chr(int(i[1:3], 16)))
            else:
                chars += i
        print(chars)        
    else:
        chars = list(txt)      
            
    ascii = [ord(i) for i in chars]
    
    return ascii
    

def Xor(ascii1, ascii2):
    xor = ""
    for i in range(len(ascii1)):
        xor_num = ascii1[i] ^ ascii2[i]
        if 32 < xor_num < 127:
            xor += chr(xor_num)
        else:
            xor += "\\x{:02x}".format([xor_num][0])            
        
    return xor    
    
txt1 = r"\x05:\x10s"
txt2 = r"o\no\x07"
ascii1 = ToAscii(txt1)
ascii2 = ToAscii(txt2)
print(ascii2)
print(ascii1)

result = Xor(ascii1, ascii2)
print(result)