import json
import os
from copy import deepcopy


# fis = open("C:\\Users\\MrSpV\\Desktop\\OutWit scraped export - American_Cars_on_Instagram_“Looks_fearless_Credit_@cthellcat.txt")
# lista = fis.readlines()
# string = '{"id":"17859059584785204","text":"Now that\u2019s what I call a hot car","created_at":1584715921,"did_report_as_spam":false,"owner":{"id":"1480502591","is_verified":false,"profile_pic_url":"https://instagram.fotp1-2.fna.fbcdn.net/v/t51.2885-19/s150x150/89715405_689538435122112_2850194439983333376_n.jpg?_nc_ht=instagram.fotp1-2.fna.fbcdn.net\u0026_nc_ohc=OTrUX0FFjdMAX8635EJ\u0026oh=17c450ed0801e92a4a78d4ff6fd995aa\u0026oe=5EADFBA8","username":"tjsmith6916"}}'
# dictionar = json.loads(string)
def determinare_utilizator(dictionar):
    return dictionar['owner']['username']


def determinare_comentariu(dictionar):
    return dictionar['text']


def reported_spam(dictionar):
    return dictionar['did_report_as_spam']


def number_of_comms(lista):
    number_comm = {}
    for linie in lista:
        dictionar = json.loads(linie + "}")
        nume = determinare_utilizator(dictionar)
        marked = reported_spam(dictionar)
        aduna = 0
        if marked == 'false':
            aduna = 2
        else:
            aduna = 1
        if nume not in number_comm.keys():
            number_comm[nume] = aduna
        else:
            number_comm[nume] += aduna
    return number_comm


def posibile(dictionar):
    eliminare = []
    for i in dictionar:
        if dictionar[i] >= 6:
            eliminare += [i]
    return eliminare


def comentarii_utilizatori(utilizator, lista):
    comentarii = []
    for linie in lista:
        dictionar = json.loads(linie + '}')
        nume = determinare_utilizator(dictionar)
        if nume == utilizator:
            comentarii += [determinare_comentariu(dictionar)]
    return comentarii


def determinare_mean(comentarii):
    lungime = 0
    for comentariu in comentarii:
        lungime += len(comentariu)
    return lungime / len(comentarii)


def determinare_median(comentarii):
    if len(comentarii) == 0:
        return None
    if len(comentarii) == 1:
        return len(comentarii[0])
    if len(comentarii) == 2:
        return (len(comentarii[0]) + len(comentarii[1])) / 2
    if len(comentarii) % 2 == 1:
        return len(comentarii[len(comentarii) // 2 + 1])
    else:
        return (len(comentarii[len(comentarii) // 2]) + len(comentarii[len(comentarii) // 2 + 1])) / 2


def determinare_iqr(comentarii):
    comentarii = list(sorted(comentarii, key=lambda x: len(x)))
    q1 = determinare_median(comentarii[:len(comentarii) // 2])
    q3 = determinare_median(comentarii[len(comentarii) // 2 + 1:])
    return q3 - q1, q3, q1


def determinare_outliners(comentarii):
    iqr, q3, q1 = determinare_iqr(comentarii)
    outliners = []
    for comentariu in comentarii:
        if len(comentariu) < q1 - 1.5 * q1 or len(comentariu) > q3 + 1.5 * q3:
            outliners += [comentariu]
    for i in outliners:
        x = comentarii.pop(comentarii.index(i))
    return comentarii


def determinare_similaritate(comentarii):
    dictionar = {}
    for comentariu in comentarii:
        if comentariu not in dictionar.keys():
            dictionar[comentariu] = 1
        else:
            dictionar[comentariu] += 1
    for i in dictionar:
        if dictionar[i] > len(comentarii) // 2:
            return 1
    return 0


def lungime_similara(comentarii):
    mean = determinare_mean(comentarii)
    count = 0
    for comentariu in comentarii:
        if mean - 1 < len(comentariu) < mean + 1:
            count += 1
    if count > len(comentarii) // 2:
        return 1
    else:
        return 0


def cuvinte_similare(comentarii):
    dictionar = {}
    for comentariu in comentarii:
        cuvinte = comentariu.split(" ")
        for cuvant in cuvinte:
            if cuvant not in dictionar.keys():
                dictionar[cuvant] = 1
            else:
                dictionar[cuvant] += 1
    count = 0
    for i in dictionar:
        if count == 2:
            return 1
        if dictionar[i] > len(comentarii) // 2 + 1:
            count += 1
    return 0


def determinare_utilizatori(lista):
    utilizatori = []
    for element in lista:
        utilizatori += [determinare_utilizator(element)]
    return list(set(utilizatori))


def verificare_spam(fisier):
    fis = open(fisier)
    lista = fis.readlines()
    lista1 = deepcopy(lista)
    fis.close()
    for i in range(0, len(lista)):
        lista[i] = json.loads(lista[i] + "}")
    utilizatori = determinare_utilizatori(lista)
    for utilizator in utilizatori:
        comms = comentarii_utilizatori(utilizator, lista1)
        if len(comms) < 6:
            continue
        comms = determinare_outliners(comms)
        if determinare_similaritate(comms) == 1 and lungime_similara(comms) and cuvinte_similare(comms):
            return 1
    return 0


print(verificare_spam(
    "C:\\Users\\MrSpV\\Desktop\\OutWit scraped export - American_Cars_on_Instagram_“Looks_fearless_Credit_@cthellcat.txt"))

# comms = comentarii_utilizatori('muscle_car_dealer', lista)
# print(lungime_similara(comms))
