from src.ThreeFish import *

# test de la fonction permute
def test_permute():
    list_test = [12, 26, 57, 89]
    list_test_permute = [89, 57, 26, 12]
    a = permute(list_test)
    assert a == list_test_permute

# test de la fonction mixcolumn
def test_mix():
    liste = [6869182828364843105, 5685451262666598955, 6869182828364843105, 5685451262666598955]
    liste_mix = [12554634091031442060, 14834149863215961599, 12554634091031442060, 14834149863215961599]
    liste_mix_fct = mixcolumn(liste)
    assert liste_mix == liste_mix_fct


def test_unmix():
    liste = [6869182828364843105, 14834149863215961599, 6869182828364843105, 5685451262666598955]
    mix = mixcolumn(liste)
    unmix = inv_mixcolumn(mix)
    assert unmix == liste

def test_inv_ECB():
    liste1 = [[18, 24, 52, 96], [65, 98, 98, 751], [652, 64, 894, 64], [64, 654, 65, 651], [6551, 61, 51, 51], [561, 651, 651, 61]]
    liste2keys = [[654, 5, 54, 54], [654, 654, 654, 5], [65, 54, 54, 54], [54, 54, 654, 654], [987, 987, 84, 84], [6884, 684, 654, 64], [18, 24, 52, 96], [65, 98, 98, 751], [652, 64, 894, 64], [64, 654, 65, 651], [6551, 61, 51, 51], [561, 651, 651, 61], [18, 24, 52, 96], [65, 98, 98, 751], [652, 64, 894, 64], [64, 654, 65, 651], [6551, 61, 51, 51], [561, 651, 651, 61], [6551, 61, 51, 51], [561, 651, 651, 61]]
    a = ECB_threefish_cipher(liste1, liste2keys)
    b = ECB_threefish_decipher(a, liste2keys)
    assert liste1 == b

def test_inv_CBC():
    liste1 = [[18, 24, 52, 96], [65, 98, 98, 751], [652, 64, 894, 64], [64, 654, 65, 651], [6551, 61, 51, 51], [561, 651, 651, 61]]
    liste2keys = [[654, 5, 54, 54], [654, 654, 654, 5], [65, 54, 54, 54], [54, 54, 654, 654], [987, 987, 84, 84], [6884, 684, 654, 64], [18, 24, 52, 96], [65, 98, 98, 751], [652, 64, 894, 64], [64, 654, 65, 651], [6551, 61, 51, 51], [561, 651, 651, 61], [18, 24, 52, 96], [65, 98, 98, 751], [652, 64, 894, 64], [64, 654, 65, 651], [6551, 61, 51, 51], [561, 651, 651, 61], [6551, 61, 51, 51], [561, 651, 651, 61]]
    a = CBC_threefish_cipher(liste1, liste2keys, 256)
    b = CBC_threefish_decipher(a, liste2keys, 256)
    assert liste1 == b

def test_ROTD_ROTG():
    a = "1101111101011110011001001110111011001111000101101011100110000010"
    x = strToInt(a)
    for i in range(76):
        b = ROTD(a)
    b = intToByteArray(b)
    for i in range(76):
        c = ROTG(b)
    assert str(c) == str(x)