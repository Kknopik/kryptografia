import re
import requests
from collections import Counter
from itertools import combinations

def Read():
    original = input()
    txt = re.sub(r'[^a-zA-Z]', '', original.lower())
    return original, txt

def Distances(txt):
    repeated = list(set(re.findall(r'(?=(.{3,}).*?\1)', txt)))
    distances = []
    pairs = set()
    
    for repeat in repeated:
        ind = [m.start() for m in re.finditer(repeat, txt)]
        for x in ind:
            for y in ind:
                if x != y:
                    pairs.add((max(x, y), min(x, y)))
                    
    for nums in pairs:
        distances.append(nums[0] - nums[1])
        
    return set(distances)

def CommonDivisors(distances):
    divisors = []
    for num in distances:
        for i in range(2, 17):
            if num % i == 0:
                divisors.append(i)           
    common = dict(Counter(divisors).most_common())
    biggest = max(common.values())
    
    common_divisors = []
    for key, val in common.items():
        if val == biggest:
            common_divisors.append(key)
    common_divisors.sort()
    
    return common_divisors   

def FindLetters(txt, distance, num):
    letters = ""
    for i in range(num, len(txt)):
        if i + 1 % num == 0:
            letters += txt[i]
    
    return letters

def Generate(code, txt):
    letters = sum(1 for c in txt if re.search(r"[a-zA-Z]+", c))
    key = code * (letters // len(code)) + code[:letters % len(code)]
    
    return key
    
def Vigenere(txt, key):
    decrypted = ""
    i = 0
    
    for c in txt:
        if re.search(r"[a-zA-Z]+", c) :
            offset = ord('a') if c.islower() else ord('A')
            key_char = key[i % len(key)]
            key_offset = ord('a') if key_char.islower() else ord('A')
            
            res = chr((ord(c) - ord(key_char) + key_offset - offset) % 26 + offset)
            decrypted += res
            i += 1
        else:
            decrypted += c
    return decrypted

def Frequency(txt):
    txt2 = re.findall(r"[a-z]", txt)
    count = dict(Counter(txt2).most_common())
    
    key_list = list(count.keys())
    common = key_list[:6]
    key_list = key_list[6:]
    uncommon = key_list[-6:]
    
    result = 0
    for i in range(5):
        if common[i] in "etaoin":
            result += 1
        elif uncommon and uncommon[i] in "vkjxqz":
            result += 1
            
    return result

def GenerateSubset(arr, length):
    subsets = combinations(arr, length)
    
    return [''.join(subset) for subset in subsets]
    
           
def Kasiski(txt, original, divisors):
    letters = "abcdefghijklmnopqrstuvwxyz"
    r = requests.get("https://stepik.org/media/attachments/lesson/668860/dictionary.txt")
    common_keys = {}
    key_num = 1
    
    for distance in divisors:
        subkeys = {i: FindLetters(txt, distance, i) for i in range(distance)}
        decrypted_keys = {}
        decrypted_frequency = {}
        for subkey in subkeys.values():
            for letter in letters:
                decrypted_keys[letter] = Vigenere(subkey, letter)
            for key in decrypted_keys.values():
                decrypted_frequency[key] = Frequency(key)
            max_val = max(decrypted_frequency.values())
            common_keys[subkey] = [key for key, value in decrypted_frequency.items() if value == max_val]
            for values in common_keys:
                key_num *= len(values)
            arr = [val for val in common_keys.values()]    
            keys = GenerateSubset(arr, distance)
            
            for key in keys:
                result = Vigenere(original, key)
                words = result.split()
                if words[0] in r:
                    return result                
                
original, txt = Read()
distances = Distances(txt)
common_divisors = CommonDivisors(distances)
result = Kasiski(txt, original, common_divisors)

print(result)
