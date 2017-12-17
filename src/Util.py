#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Contain  utility function such as exponentation or pgcd or read/write functions

from random import SystemRandom, getrandbits
import os
from src.Primes import *


primes = get100kPrimes()

def pgcd(a, b):
    # calcul recursif du pgcd de a et b
    if b == 0:
        return a
    else:
        r = a % b
        return pgcd(b, r)

def factorize(n):
    factors = []
    i = 2
    while i <= n / i:
        while n % i == 0:
            factors.append(i)
            n /= i
        i += 1

    if n > 1:
        factors.append(n)

    return factors

# Cette fonction teste si un nombre possède des facteurs premiers allant jusqu'à 500.
# C'est une manière rapide de vérifier si un nombre n'est pas premier pour la génération de grands nombres premiers.
def trial_division(n, B=1000):
    if n == 1:
        return True
    if n == 2:
        return False

    isDivisible = False
    for p in primes:
        if p > B:
            break
        if n % p == 0 and n != p:
            isDivisible = True
            break

    return isDivisible


# Test de primalité de Rabin-Miller, utilisé dans la génération de nombres premiers très grands
def rabin_miller(n, t = 7):
    isPrime = True
    if n < 6:
        return [not isPrime, not isPrime, isPrime, isPrime, not isPrime, isPrime][n]
    elif not n & 1:
        return not isPrime

    def check(a, s, r, n):
        x = pow(a, r, n)
        if x == 1:
            return isPrime
        for i in range(s-1):
            if x == n - 1:
                return isPrime
            x = pow(x, 2, n)
        return x == n-1

    # Find s and r such as n - 1 = 2^s * r
    s, r = 0, n - 1
    while r & 1:
        s = s + 1
        r = r >> 1

    for i in range(t):
        a = SystemRandom.choice(2, n-1)
        if not check(a, s, r, n):
            return not isPrime

    return isPrime

def int2hexa(n):
    hexk = hex(n)
    hexk = hexk.replace('\'', '')
    hexk = hexk.replace('0x', '', 1)
    hexk = str(hexk)
    return hexk


def probable_prime(k, B=1000):
    success = False
    n = 0
    while not success:
        divisible = True
        while divisible:
            # generate a k-bit random odd number
            n = SystemRandom.getrandbits(k) | 1
            divisible = trial_division(n, B)

        if rabin_miller(n):
                success = True
    return n


def safe_prime(k):
    success = False
    r, q = 0, 0
    while not success:
        q = probable_prime(k - 1)
        # We try to find p = 2 * R * q + 1 1000 times and if it fails we change q
        for r in range(1, 1000):
            p = 2 * r * q + 1
            if (not trial_division(p)) and rabin_miller(p):
                success = True
                break

    return p, q, r

# Début lecture fichier a chiffrer
# but de la fonction est de lire L_Block du fichier et de les chiffrer puis d'écrire dans un nouveau fichier
def readfile(fichier, L_block, do_padding):
    # information sur la taille du fichier
    stat = os.stat(fichier)
    tailleFich = stat.st_size
    # conversion de L_block en octets
    L_block_bytes = int(L_block / 8)
    # nbr de blocks sans padding
    nbr_block_nopad = int(tailleFich / L_block_bytes)
    # taille du dernier block
    last_bloc_length = tailleFich - L_block_bytes * nbr_block_nopad
    # last_bloc détermine l'endroit ou commence le dernier bloc
    last_bloc =  int(L_block_bytes * nbr_block_nopad)
    # list avec la valeur des int du fichier
    datalist = []

    for i in range(0, (tailleFich - last_bloc_length), L_block_bytes):
        with open(fichier, 'rb') as rfile:
            rfile.seek(i)
            # L_block bits de data stocké dans la var data
            data = rfile.read(L_block_bytes)
            data = int.from_bytes(data, byteorder='little', signed=False)
            datalist.append(data)

    # ajout de padding si tailleFich / L_block_bytes != entier sinon pas besoin de padding
    if last_bloc_length != 0:
        with open(fichier, 'rb') as rfile:
            rfile.seek(last_bloc)
            data = rfile.read(last_bloc_length)
            # méthode d'ajout de padding
            nbr_byte_pad = L_block_bytes - len(data)
            # ajout d'un dernier octet sur la fin pour préciser combien il y a d'octets de padding
            data = (nbr_byte_pad - 1) * b'0' + data + bytes([nbr_byte_pad])
            data = int.from_bytes(data, byteorder='little', signed=False)
            datalist.append(data)
    else:
        if do_padding == 1:
            pad_last_byte = bytes([L_block_bytes])
            data_pad = b'0' * (L_block_bytes - 1) + pad_last_byte
            data_pad = int.from_bytes(data_pad, byteorder='little', signed=False)
            datalist.append(data_pad)
    return datalist

def organize_data_list(data_list, L_bloc):
    # permet de mettre les données dans un tableau de list de n mots de 64bits
    l = int(L_bloc / 64)
    datalistorder = []
    for i in range(0, len(data_list), l):
        datalistorder.append(data_list[i:(i + l)])
    return datalistorder

def ajout_padding(datalistorder, Length_chif_bloc):
    last_list = datalistorder[len(datalistorder) - 1]
    # si la dernière liste ne fais pas la bonne taille N(4, 8 ou 16) alors do padding
    if len(last_list) == int(Length_chif_bloc / 64):
        # ajout d'une liste de N(4, 8, 16) - 1 mot random de 64bits
        new_last_list = []
        for i in range(0, int(Length_chif_bloc / 64) - 1):
            new_last_list.append(getrandbits(64))
        pad_info = getrandbits(56)
        # Si 4, 8 ou 16 mots on été ajoutés
        nbr_pad = int(Length_chif_bloc / 64)
        # convertion en byte du randint de 56 bits
        pad_info = pad_info.to_bytes(7, byteorder='little', signed=False)
        pad_info = pad_info + bytes([nbr_pad])
        pad_info = int.from_bytes(pad_info, byteorder='little', signed=False)
        # ajout de l'info dans la new list
        new_last_list.append(pad_info)
        # ajout de la new list dans le datalistorder
        datalistorder.append(new_last_list)
    else:
        # S'il ne faut ajouter q'un seul mot d'information a la dernière liste
        if len(last_list) + 1 == int(Length_chif_bloc / 64):
            nbr_rand = getrandbits(56)
            pad_info = nbr_rand.to_bytes(7, byteorder='little', signed=False)
            pad_info = pad_info + bytes([1])
            pad_info = int.from_bytes(pad_info, byteorder='little', signed=False)
            # ajout du mot dans la dernière list
            last_list.append(pad_info)
        else:
            lenght_last_list = int(Length_chif_bloc / 64) - len(last_list)
            for i in range(0, (int(Length_chif_bloc / 64) - len(last_list)) - 1):
                last_list.append(getrandbits(64))
            nbr_rand = getrandbits(56)
            pad_info = nbr_rand.to_bytes(7, byteorder='little', signed=False)
            pad_info = pad_info + bytes([lenght_last_list])
            pad_info = int.from_bytes(pad_info, byteorder='little', signed=False)
            last_list.append(pad_info)
    return datalistorder

def remove_padding_list(data, Length_chif_bloc):
    # dernière liste du tableau
    data_pad_list = data[len(data) - 1]
    # dernier élément de la dernière liste du tableau
    data_pad = data_pad_list[len(data_pad_list) - 1]
    # conversion du last element en byte
    data_pad = data_pad.to_bytes(8, byteorder='little', signed=False)
    # valeur du pading
    data_pad_nbr = int(data_pad[7])
    # Si le padding est la dernière liste complète alors on la supprime
    if data_pad_nbr == int(Length_chif_bloc / 64):
        del data[len(data) - 1]
    else:
        data_pad = data_pad_list[:len(data_pad_list) - data_pad_nbr]
        del data[len(data) - 1]
        data.append(data_pad)
    return data

def remove_padding_data(data, L_bloc):
    L_bloc_byte = int(L_bloc / 8)
    # dernière liste du tableau
    data_pad_list = data[len(data) - 1]
    # dernier élément de la dernière liste du tableau
    data_pad = data_pad_list[len(data_pad_list) - 1]
    # conversion du last element en byte
    data_pad = data_pad.to_bytes(L_bloc_byte, byteorder='little', signed=False)
    # valeur du pading
    data_pad_nbr = int(data_pad[7])
    if data_pad_nbr == L_bloc_byte:
        # suppression du dernier élément de la dernière liste
        del data_pad_list[len(data_pad_list) - 1]
    else:
        # remove padding
        data_pad_remove = data_pad[(data_pad_nbr - 1):(L_bloc_byte - 1)]
        # convertion de la nouvelle data en int
        new_data = int.from_bytes(data_pad_remove, byteorder='little', signed=False)
        # suppression du dernier élément de la dernière liste
        del data_pad_list[len(data_pad_list) - 1]
        # insertion du dernier élément de la dernière liste
        data_pad_list.append(new_data)
    return data, data_pad_nbr

# Takes a bytearray as input and write it in a file
def writefile(fichier, data):
    with open(fichier, 'w') as wfile:
        wfile.write(data)

def writefilelist(fichier, data):
    with open(fichier, 'wb') as wfile:
        for i in data:
            for j in i:
                j = j.to_bytes(8, byteorder='little', signed=False)
                wfile.write(j)

def write_file_list_pad(fichier, data, val_last_data):
    with open(fichier, 'wb') as wfile:
        # ecriture de tout sauf de la dernière liste de data, celle qui contient la valeur sans padding
        for i in range(0, len(data) - 1):
            for j in data[i]:
                j = j.to_bytes(8, byteorder='little', signed=False)
                wfile.write(j)
        # dernière liste
        last_list = data[len(data) - 1]
        # écriture de tout sauf du dernier mot
        for i in range(0, len(last_list) - 1):
            wdata = last_list[i].to_bytes(8, byteorder='little', signed=False)
            wfile.write(wdata)
        if val_last_data == 8:
            wdata = last_list[len(last_list) - 1].to_bytes(8, byteorder='little', signed=False)
            wfile.write(wdata)
        else:
            wdata = last_list[len(last_list) - 1].to_bytes((8 - val_last_data), byteorder='little', signed=False)
            wfile.write(wdata)

def readkey(fichier):
    with open(fichier, 'r') as rfile:
        data = rfile.read()
        return data

def intToByteArray(to_convert):
    to_convert = int(to_convert)
    output = []
    result = []
    intByte = 8
    mask = 0xFF

    for i in range(0, intByte):
        output.insert(0, to_convert & mask)
        to_convert >>= 8

    for i in output:
        i = bin(i)[2:].zfill(8)
        result.append(i)
    result = "".join(result)
    result = str(result)
    return result

def strToInt(to_convert):
    return (int(to_convert, 2))

def xor_function(Barray0, Barray1):
    result = str(bin(int(Barray0, 2) ^ int(Barray1, 2)))
    result = result.replace('0b', '', 1)
    if len(result) < 64:
        result = "0" * (64 - len(result)) + result
    return result

def additionMod(Barray0, Barray1):
    result = str(bin((int(Barray0, 2) + int(Barray1, 2)) % 2**64))
    result = result.replace('0b', '', 1)
    return result

def soustracMod(Barray0, Barray1):
    result = str(bin((int(Barray0, 2) - int(Barray1, 2)) % 2**64))
    result = result.replace('0b', '', 1)
    if len(result) < 64:
        result = "0" * (64 - len(result)) + result
    return result

def bytearrayToInt(to_convert):
    convert = "".join(to_convert)
    convert = int(convert, 2)
    return convert

def addition_modulaire_listes(data_list, tab_keys):
    output = []
    for i in range(0, len(data_list)):
        result = (data_list[i] + tab_keys[i]) % 2**64
        output. append(result)
    return output

def soustraction_modulaire_listes(data_list, tab_keys):
    output = []
    for i in range(0, len(data_list)):
        result = (data_list[i] - tab_keys[i]) % 2 ** 64
        output.append(result)
    return output

def xor_2_lists(list1, list2):
    output = []
    for i in range(0, len(list1)):
        result = list1[i] ^ list2[i]
        output.append(result)
    return output

def rename_fichier(path_fichier, option):
    rep = path_fichier.split("/")
    fichier = rep[len(rep) - 1]
    if option == 0:
        enc = ".encrypt"
        fichier = fichier + enc
        rep[len(rep) - 1] = fichier
        new_fichier = "/".join(rep)
    else:
        fichier = fichier[:(len(fichier) - 8)]
        rep[len(rep) - 1] = fichier
        new_fichier = "/".join(rep)
    os.rename(path_fichier, new_fichier)
