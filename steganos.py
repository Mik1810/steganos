from PIL import Image
import random
import json

# Credits: https://www.geeksforgeeks.org/image-based-steganography-using-python/

keys = {'c': '10000000', 'i': '01000000', 'a': '00100000', 'o': '00010000'}

# Crea una chiave randomica per criptare il messaggio servendosi dei caratteri del messaggio stesso
def generate_dictionary(data):
    global keys
    keys = {}

    listData = [*data]
    for i in listData:
        binary = format(random.randrange(0, 256), '08b')
        while bin in keys.values():
            binary = format(random.randrange(0, 256), '08b')
        keys[i] = binary

    # Salvataggio del dizionario in un file JSON
    with open('keys.json', 'w') as file:
        json.dump(keys, file)


# Converto il messaggio attraverso un dizionario interno
def convert(data):
    newd = []

    for i in data:
        if i not in keys.keys():
            raise ValueError("Chiave non presente nel dizionario")

        newd.append(keys[i])
    return newd


def modPix(pix, data):
    datalist = convert(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Estraggo 3 pixel alla volta
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        # I primi 8 valori dei 3 pixel sono modificati sottraendo 1 al valore se
        # è presente un 1 nella posizione j-esima del carattere convertito
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if (pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1

        # L'ultimo valore dei 3 pixel dice al programma  se fermarsi o meno,
        # Se è presente un valore pari continua, altrimenti termina la lettura
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if (pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1


# Cripto il messaggio
def encode(image_path, text_to_encode, keys_to_use):
    image = Image.open(image_path, 'r')

    data = text_to_encode
    if len(data) == 0:
        raise ValueError('Il messaggio è vuoto')

    if keys_to_use == 2:
        generate_dictionary(data)

    newimg = image.copy()
    encode_enc(newimg, data)

    new_img_name = str(image_path).split("/")[-1].split(".")[0]
    new_img_name = new_img_name + "Encoded.png"
    newimg.save(new_img_name)


# Decodifico il messaggio
def decode(image_path, keys_path=None):
    keys_to_decode = {}
    if keys_path is not None:
        with open(keys_path, "r") as file:
            keys_to_decode = json.load(file)

    keys_to_decode = {v: k for k, v in keys_to_decode.items()}
    image = Image.open(image_path, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while True:
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        if binstr not in keys_to_decode.keys():
            raise ValueError("Chiave non presente nel dizionario")
        data += keys_to_decode[binstr]
        if (pixels[-1] % 2 != 0):
            return data
