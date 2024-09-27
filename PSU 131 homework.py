primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
factors = []

numbers = int(input('Plug in a number to factor: '))


for num in primes:
    if numbers in primes:
        factors.append('This is a prime')
        break
    elif numbers % num == 0:
        factors.append(num)

print(factors)

