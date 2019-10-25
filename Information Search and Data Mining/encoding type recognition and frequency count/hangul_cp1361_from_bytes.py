syllable = input("음절 입력 : ")
bytesofSyl = int.from_bytes((bytes(syllable, encoding="cp1361")), 'big')
byteofCho = (bytesofSyl & (b'\x1f'[0] << 10)) >> 10
byteofJung = (bytesofSyl & (b'\x1f'[0] << 5)) >> 5
byteofJong = bytesofSyl & b'\x1f'[0]

print("초성 :", byteofCho)
print("중성 :", byteofJung)
print("종성 :", byteofJong)
