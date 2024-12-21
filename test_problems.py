# Test problems for brain cognitive processing

# 1. Simple arithmetic calculator
calc_problem = """
Write a function that takes two numbers and an operator (+, -, *, /) 
and returns the result of the operation.

Example:
calculate(4, 2, '+') should return 6
calculate(4, 2, '-') should return 2
calculate(4, 2, '*') should return 8
calculate(4, 2, '/') should return 2
"""

# 2. FizzBuzz implementation
fizzbuzz_problem = """
Write a function that takes a number n and prints:
- 'Fizz' if the number is divisible by 3
- 'Buzz' if the number is divisible by 5
- 'FizzBuzz' if the number is divisible by both 3 and 5
- The number itself if none of the above conditions are true

Example:
fizzbuzz(15) should print numbers from 1 to 15 with appropriate substitutions
"""

# 3. Array manipulation
array_problem = """
Write a function that finds the second largest number in an array.
If there is no second largest number, return the largest number.

Example:
find_second_largest([1, 3, 4, 5, 0, 2]) should return 4
find_second_largest([1, 1, 1]) should return 1
"""

# Test inputs for the brain
test_inputs = [
    (calc_problem, "programming"),
    (fizzbuzz_problem, "programming"),
    (array_problem, "programming")
]