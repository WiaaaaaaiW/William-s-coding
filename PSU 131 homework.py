primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
factors = []

numbers = int(input('Plug in a number to factor: '))
a = numbers


for each in primes:
    if a % each == 0:
        factors.append(each)

print(factors)
