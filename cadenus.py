from typing import List
from copy import deepcopy

def remove_repeated_letters(original: str) -> str:
  result = ""
  for letter in original:
    if letter not in result:
      result += letter
  return result

def clean_text(original: str) -> str:
  return original.replace(" ", "").replace("\n", "")

def roll_column(rows: List[str], column_number: int, no_of_steps: int):
  print("STEPS",no_of_steps)
  temp = deepcopy(rows)
  for row_number in range(25):
    rows[row_number][column_number] = temp[(row_number - no_of_steps) % 25][column_number]

def create_permutation(key: str) -> List[int]:
  key_sorted = [letter for letter in sorted(key)]

  permutation = []
  for letter in key:
    index = [position+1 for position, l in enumerate(key_sorted) if l == letter and position+1 not in permutation][0]
    permutation.append(index)  
  return permutation

def transpose(original:str, permutation: List[int]) -> str:
  result = ""
  for ind in range(len(permutation)):
    target = permutation.index(ind+1)
    if target < len(original):
      result += original[target]
  return result



def encrypt(plain_text: str, key: str) -> str:
  plain_text = clean_text(plain_text)
  key = remove_repeated_letters(key)
  plain_text_len = len(plain_text)
  key_len = len(key)
  block_size = key_len * 25
  number_of_blocks = plain_text_len // block_size

  ciphertext = ""
  for block in range(number_of_blocks):
    block = plain_text[block * block_size: (block+1) * block_size]

    i = 0
    rows = []
    while i < block_size:
      rows.append(list(block[i:i+key_len]))
      i+=key_len

    for column_number in range(key_len):
      no_of_steps = ord(key[column_number]) - ord('A')
      roll_column(rows, column_number, no_of_steps)

    permuatation = create_permutation(key)

    for row in rows:
      ciphertext += transpose("".join(row), permuatation)
  return ciphertext


plain_text = """TO BE OR NOT TO BE THAT IS THE QUESTION WHETHER TIS NOBLER
IN THE MIND TO SUFFER THE SLINGS AND ARROWS OF OUTRAGEOUS
FORTUNE OR TO TAKE ARMS AGAINST A SEA OF TROUBLES AND BY
OPPOSING END THEM TO DIE TO SLEEP NO MORE AND BY A SLEEP TO
SAY WE END THE HEARTACHE AND THE THOUSAND NATURAL SHOCKS
THAT FLESH IS HEIR TO TIS A CONSUMMATION DEVOUTLY TO BE
WISHD TO DIE TO SLEEP TO SLEEP PERCHANCE TO DREAM AY THERES
THE RUB FOR IN THAT SLEEP OF DEATH WHAT DREAMS MAY COME
WUTEVUH"""
key = "ORATIO"

print(encrypt(plain_text, key))
