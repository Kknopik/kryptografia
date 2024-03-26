import re

def Delete(split, txt):
    for c in split:
        txt = txt.replace(c, "")
    return txt

def SplitAgain(split, txt, result, compare):
    for i in split:
        pattern = i.replace(chr(92), "")
        
        matches = re.finditer(pattern, txt)
        
        for match in matches:
            start_index = match.start()
            end_index = match.end()
            if compare[start_index] == None:
                result[start_index] = i
                compare[start_index:end_index] = [1] * (end_index - start_index)
            
    return result

def Split(txt):
    split1 = re.findall(r'\\x..', txt)
    split3 = Delete(split1, txt)
    split2 = re.findall(r'\\(?!x)\w', txt)
    split3 = Delete(split2, split3)
    split3 = list(split3)
     
    split = [None] * len(txt)
    compare = [None] * len(txt)
    split = SplitAgain(split1, txt, split, compare)
    split = SplitAgain(split2, txt, split, compare)
    split = SplitAgain(split3, txt, split, compare)
    
    while None in split:
        split.remove(None)
        
    print(split)
    
txt1 = r"\x05:\x10s"
txt2 = r"o\no\x07"
ascii1 = Split(txt1)