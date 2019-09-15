import math

# Función principal
def main():
    global message,key,mode
    message = input('Introducir Mensaje: ')
    key = int(input('Introducir Key [2-%s]: ' % (len(message) - 1)))
    mode = input('Cifrar/Decifrar [c/d]: ')

    if mode.lower().startswith('c'): # Si mode es igual a "c" se llamara a "encryptMessage"
        text = cifrarMensaje(key, message)
    elif mode.lower().startswith('d'): # De lo contrario se llamara a "decryptMessage"
        text = descifrarMensaje(key, message)

    print('Salida:\n%s' %(text + '|'))
    print("\n")
    input("")

def cifrarMensaje(key, message):

    cipherText = [''] * key
    for col in range(key):
        pointer = col
        while pointer < len(message):
            cipherText[col] += message[pointer]
            pointer += key
    return ''.join(cipherText)

def descifrarMensaje(key, message):

    numCols = math.ceil(len(message) / key)
    numRows = key
    numShadedBoxes = (numCols * numRows) - len(message)
    plainText = [""] * numCols
    col = 0; row = 0;

    for symbol in message:
        plainText[col] += symbol
        col += 1

        if (col == numCols) or (col == numCols - 1) and (row >= numRows - numShadedBoxes):
            col = 0
            row += 1

    return "".join(plainText)

if __name__ == '__main__':
    main()