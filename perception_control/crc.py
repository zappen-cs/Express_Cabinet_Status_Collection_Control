def crc16(x, invert):
    wCRCin = 0x0000
    wCPoly = 0x1021
    for byte in x:
        if type(byte) is str:
            wCRCin ^= (ord(byte) << 8)
        else:
            wCRCin ^= ((byte) << 8)
        for i in range(8):
            if wCRCin & 0x8000:
                wCRCin = (wCRCin << 1) ^ wCPoly
            else:
                wCRCin = (wCRCin << 1)

    # wCRCin = wCRCin & 0xffff
    s = hex(wCRCin).upper()
    # return s
    return s[-2:] + s[-4:-2] if invert == True else s[-4:-2] + s[-2:]


if __name__ == '__main__':
    # var = [0x0A,0x79,0x7F,0x01]
    #print(var,True)
    data1 = bytearray.fromhex("0206000300FE")  # 将hexstring 转化为 字节数组。
    data2 = bytearray.fromhex("0B76010201")

    # result=crc16(var1,False)
    crc1 = crc16(data1, True)
    print(type(crc1))
    print(crc1)

    crc2 = crc16(data2, True)
    print(crc2)
