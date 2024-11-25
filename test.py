import random
import os

def generate_random_numbers(count, max_value):
    """Generate and return a list of random numbers."""
    return [random.randint(1, max_value) for _ in range(count)]

def calculate_sum(numbers):
    """Calculate the sum of a list of numbers."""
    return sum(numbers)

def find_max(numbers):
    """Find the maximum number in a list."""
    return max(numbers)

# Main program
if __name__ == "__main__":
    # Generate 10 random numbers between 1 and 100
    random_numbers = generate_random_numbers(10, 100)

    # Print the generated numbers
    print("Generated Random Numbers:")
    print(random_numbers)

    # Calculate sum of the numbers
    total_sum = calculate_sum(random_numbers)
    print(f"\nSum of the numbers: {total_sum}")

    # Find the maximum number
    max_num = find_max(random_numbers)
    print(f"\nMaximum number: {max_num}")

    # Loop through the numbers and print each one
    for num in random_numbers:
        print(f"{num} squared is {num ** 2}")
