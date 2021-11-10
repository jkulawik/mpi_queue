import random
import math


# Poniższa funkcja generuje liczbę z rozkładem wykładniczym na podstawie zadanej średniej
def exp(mean):
    losowa = random.random()  # należy do [0,1]
    # Dla 0 dostaniemy -inf więc losujemy ponownie # TODO skąd to się wzieło i czy konieczne
    while losowa == 0:
        losowa = random.random()
    # Na podstawie wzoru odwrotnej dystrybuanty rozkładu wykładniczego, tzn.
    # F^(-1)(u)=(-1/Lambda)*ln(w), gdzie w - liczba z przedzialu (0,1) (losowa) o rozkladzie jednostajnym:
    return float(-1.0) * float(mean) * math.log(losowa)
