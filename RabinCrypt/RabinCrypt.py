import math
import decimal
import random

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
    print('Mp = ' + str(data_p))
    data_q = Power(data, (q + 1) / 4) % q
    print('Mq = ' + str(data_q))
       
    div, x, y = GCD(p, q)
    result = x*p + y*q
    print(str(x) + '*' + str(p) + ' + ' + 
          str(y) + '*' + str(q) + ' = ' + str(result))
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

if __name__ == "__main__":

    print('input your data: ')    
    data = int(input())
    print()

    primes = FindPrimes(0, 1000)
    print('all primes: ')
    print(primes)
    print()
    
    primesMod = FindModPrimes(primes)
    print('primes which mod 4 = 3: ')
    print(primesMod)
    print()
    
    p = ChoiceRandomPrime(primesMod)
    q = ChoiceRandomPrime(primesMod)
    # data < p*q обязательно
    # если совпали значения, то выбираем, пока не станут различными
    while p == q or p * q <= data:
        q = ChoiceRandomPrime(primesMod)
    # (p,q) - закрытый ключ системы
    print('Закрытый ключ: ' + str(p) + '; ' + str(q))
    n = p * q
    # n - открытый ключ системы
    print('Открытый ключ: ' + str(n))
    print()

    encrypt_data = Encrypt(data, n) 
    print('!!! your encrypt data !!!: ' + str(encrypt_data))
    print()

    decrypt_data1, decrypt_data2, decrypt_data3, decrypt_data4 = Decrypt(encrypt_data, p, q, n)
    print('!!! your decrypt data !!!: ' + 
          str(decrypt_data1) + ' or ' +
          str(decrypt_data2) + ' or ' +
          str(decrypt_data3) + ' or ' +
          str(decrypt_data4))
    print()