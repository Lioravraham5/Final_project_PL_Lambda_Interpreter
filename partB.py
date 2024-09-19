from functools import reduce

# Q1: Fibonacci Sequence Generator
fibonacci = lambda n: reduce(lambda x, _: x + [x[-1] + x[-2]], range(n-2), [0, 1])[:n]
# Test:
print(fibonacci(30))

# Q2: Strings concatenation
concatStr = lambda lst: reduce(lambda x, y: x + " " + y, lst)
# Test:
print(concatStr(["hello", "good", "world"]))

# Q3: Square list
def cumulative_sum_of_squares(lst):
    return list(map(
        lambda sublist: reduce(
            lambda accumulator , x: accumulator + x,
            map(
                lambda y: y**2,
                filter(
                    lambda z: z % 2 == 0,
                    sublist
                )
            ),
            0
        ),
        lst
    ))

# Test:
lists = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
print(cumulative_sum_of_squares(lists))

# Q4: Higher-Order Function for Cumulative Operations
def cumulative_operation(op):
    return lambda seq: reduce(op, seq)

# Binary operation for multiplication
multiply = lambda x, y: x * y
# Factorial function using cumulative_operation
factorial = lambda n: cumulative_operation(multiply)(range(1, n + 1))
# Binary operation for exponentiation (repeated multiplication)
exponentiate = lambda x, y: x * y
# Exponentiation function using cumulative_operation
exponentiation = lambda base, exp: cumulative_operation(exponentiate)([base] * exp)

def test_cumulative_factorial_and_exp_operations(n, base, exp):
    fact_result = factorial(n)
    expo_result = exponentiation(base, exp)
    print(f"Factorial result: {fact_result}")
    print(f"Exponentiation result: {expo_result}")

# Test
test_cumulative_factorial_and_exp_operations(5, 2,3)

# Q5
sum_squared = lambda nums: reduce(lambda x, y: x + y, map(lambda x: x**2, filter(lambda x: x % 2 == 0, nums)))

# Test:
print(sum_squared([1, 2, 3, 4, 5, 6]))

# Q6 Return a list of numbers of the palindromes strings:
count_palindromes = lambda lst: list(map(lambda sublist: reduce(lambda x, y: x + (1 if y == y[::-1] else 0), sublist, 0), lst))

# Test:
string_lists = [["level", "world", "radar"], ["hello", "racecar", "python"], ["abc", "def"]]
print(count_palindromes(string_lists))

# Q7 Lazy Evaluation:
# the answer for this question present in the word file

# Q8 Prime numbers list:
get_primes_desc = lambda nums: sorted([n for n in nums if n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))], reverse=True)

# Test:
numbers = [10, 15, 3, 7, 2, 11, 5]
primes_desc = get_primes_desc(numbers)
print(primes_desc)
