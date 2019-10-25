choVal = int(input("초성값 입력 : "))
jungVal = int(input("중성값 입력 : "))
jongVal = int(input("종성값 입력 : "))
val = 0x8000

val += choVal << 10
val += jungVal << 5
val += jongVal

bytesVal = val.to_bytes((val.bit_length() + 7) // 8, 'big')
print("음절 :", str(bytesVal, encoding='cp1361'))
