import math
import decimal
import random

from tkinter import *
import os

# проверяем число на простоту
def IsPrime(number):
    if number % 2 == 0:
        return number == 2
    d = 3
    while d * d <= number and number % d != 0:
        d += 2
    return d * d > number

# находим простые числа в указанном диапазоне
def FindPrimes(start, stop):
    primes = []
    for i in range(start, stop):
        if IsPrime(i):
            primes.append(i)
    return primes

# находим те простые, у которых % 4 = 3
def FindModPrimes(primes):
    primesMod = []
    for i in range(0, len(primes)):
        if primes[i] % 4 == 3:
            primesMod.append(primes[i])
    return primesMod

# случайный выбор простого числа из указанного списка
def ChoiceRandomPrime(primesMod):
    secure_random = random.SystemRandom()
    result = secure_random.choice(primesMod)
    return result

# выполняем сложение по модулю
def AdditingByMod(first, second, mod):
    answer = (first % mod + second % mod) % mod   
    return answer

# выполняем умножение по модулю
def MultiplicateByMod(first, second, mod):
    answer = (first % mod * second % mod) % mod 
    return answer

# выполняем кодирование
def Encrypt(data, n):    
    answer = MultiplicateByMod(data, data, n)     
    return answer  

# находим коэффициенты x, у 
# (где x - мультипликативная инверсия p по модулю q)
def GCD(num1, num2):
    # расширенный алгоритм Евклида
    # gcd(a, m) = ax + my = 1
    if num1 == 0:
        return (num2, 0, 1)
    else:
        div, x, y = GCD(num2 % num1, num1)
    return (div, y - (num2 // num1) * x, x)

# выполняем вычитание по модулю
def SubstractByMod(first, second, mod):
    answer = (first % mod - second % mod) % mod   
    return answer

# быстрое возведение в степень
def Power(a, n):
    if n == 0:
        return 1
    elif n == 1:
        return a
    elif n % 2 != 0:
        return a * Power(a, n-1)
    elif n % 2 == 0:
        return Power(a*a, n/2)

# выполняем декодирование 
# (получаем 4 числа, т.к. система недетерминирована)
def Decrypt(data, p, q, n):    
    # символ Лежандра 
    # (считаем квадратный корень из data)
    data_p = Power(data, (p + 1) / 4) % p
    data_q = Power(data, (q + 1) / 4) % q
       
    div, x, y = GCD(p, q)
    print()
    # китайская теорема об остатках
    r1 = AdditingByMod(
         MultiplicateByMod(x, MultiplicateByMod(p, data_q, n), n),
         MultiplicateByMod(y, MultiplicateByMod(q, data_p, n), n),
                       n)
    r2 = n - r1
    r3 = SubstractByMod(
         MultiplicateByMod(x, MultiplicateByMod(p, data_q, n), n),
         MultiplicateByMod(y, MultiplicateByMod(q, data_p, n), n),
                        n)
    r4 = n - r3
    return r1, r2, r3, r4

# зашифруем данные
def ClickEncrypt():
    input_file = open('source/input.txt', 'r')
    data = int(input_file.read())
    # границы регулируем относительно величины введённого нами числа
    primes = FindPrimes(0, 100000)    
    primesMod = FindModPrimes(primes)
    # (p,q) - закрытый ключ системы
    p = ChoiceRandomPrime(primesMod)
    q = ChoiceRandomPrime(primesMod)
    # data < p*q обязательно
    # если совпали значения, то выбираем, пока не станут различными
    while p == q or p * q <= data:
        q = ChoiceRandomPrime(primesMod)           
    # n - открытый ключ системы
    n = p * q 
    # сохраним все вычисленные значения
    output_file = open('source/output.txt', 'w')
    output_file.write(str(p) + '\n')
    output_file.write(str(q) + '\n')
    output_file.write(str(n) + '\n')
    encrypt_data = Encrypt(data, n)
    output_file.write(str(encrypt_data) + '\n' + '\n')
    output_file.close

# расшифруем зашифрованные данные
def ClickDecrypt():
    output_file = open('source/output.txt', 'r+')
    if os.stat('source/output.txt').st_size != 0:
        # сохраним все прочитанные строки без '\n'
        all_data = output_file.read().splitlines()
        p = (int)(all_data[0])
        q = (int)(all_data[1])   
        n = (int)(all_data[2])
        data = (int)(all_data[3])
        r1, r2, r3, r4 = Decrypt(data, p, q, n)
        output_file.write(str(r1) + '\n' +
                          str(r2) + '\n' +
                          str(r3) + '\n' +
                          str(r4) + '\n')
    else:
        print('Сначала зашифруйте данные!')
    output_file.close

window = Tk()
window.title("Криптографическая система Рабина")

btn1 = Button(window, text = "Зашифровать", 
              bg = "yellow", fg = "black", command = ClickEncrypt)
btn1.grid(column = 0, row = 0)   
btn2 = Button(window, text = "Расшифровать", 
              bg = "orange", fg = "black", command = ClickDecrypt)
btn2.grid(column = 1, row = 0)

window.mainloop()