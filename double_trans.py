from math import ceil
from typing import List

def transpose(original:str, mapping: List[int]) -> str:
  result = ""
  for ind in range(len(mapping)):
    target = mapping.index(ind+1)
    if target < len(original):
      result += original[target]
  return result

def create_mapping(key: str) -> List[int]:
  key_sorted = [letter for letter in sorted(key)]

  mapping = []
  for letter in key:
    index = [position+1 for position, l in enumerate(key_sorted) if l == letter and position+1 not in mapping][0]
    mapping.append(index)  
  return mapping

def inverse_mapping(key: str) -> List[int]:
  forward_mapping = create_mapping(key)
  inverse = []
  for i in range(len(forward_mapping)):
    inverse.append(forward_mapping.index(i+1)+1)
  return inverse

def encrypt(plain_text, key):
  plain_text = plain_text.replace(" ", "")
  key_length = len(key)
  padding = (key_length - (len(plain_text) % key_length) ) * "$"
  plain_text += padding
  mapping = create_mapping(key)
  rows = []
  i = 0
  while i < len(plain_text):
    row = plain_text[i:i+key_length]
    rows.append(row)
    i+=key_length

  for i in range(len(rows)):
    rows[i] = transpose(rows[i], mapping)

  cipher_text = ""
  for col in range(key_length):
    for row in rows:
      if row[col] != "$":
        cipher_text += row[col]
  return make_into_groups(cipher_text)

def make_into_groups(cipher_text):
  parts = [cipher_text[i:i+5] for i in range(0, len(cipher_text), 5)]
  return " ".join(parts)

def decrypt(cipher_text, key):
  cipher_text = cipher_text.replace(" ", "")
  key_length = len(key)
  mapping = inverse_mapping(key)

  number_of_rows = ceil(len(cipher_text) / key_length)
  rows = ["" for _ in range(number_of_rows)]

  overrun = len(cipher_text) - (len(cipher_text) // key_length) * key_length
  column_heights = [number_of_rows if (mapping[i] <= overrun) else number_of_rows-1 for i in range(len(mapping))]

  i = 0
  column_number = 0
  while i < len(cipher_text):
    for row in range(column_heights[column_number]):
      rows[row] += cipher_text[i]
      i+=1
    if (column_heights[column_number]) < number_of_rows:
      rows[number_of_rows-1] += " "
    column_number+=1

  for i in range(len(rows)):
    rows[i] = transpose(rows[i], mapping)

  plain_text = "".join(rows)
  return make_into_groups(plain_text)
  


plain_text = "YOUR MOTHER WAS A HAMSTER AND YOUR FATHER SMELT OF ELDERBERRIES"
round1 = encrypt(plain_text, "DESCRIBE")

round2 = encrypt(round1, "COASTLINE")
assert round2 == "NDODR WTRFH ASEER AERMR OFLBE OERSA YEAEI HMRAL UTERH MTTYS OSU"

round3 = decrypt(round2,"COASTLINE")
round4 = decrypt(round3,"DESCRIBE")
assert round4.replace(" ", "") == plain_text.replace(" ", "")
print(round4)
