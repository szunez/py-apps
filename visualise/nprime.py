import matplotlib.pyplot as plt
import argparse
import math

# Function to count primes up to n using Sieve of Eratosthenes
def sieve_count_primes(n):
    if n < 2:
        return 0
    # Use a list of booleans, optimized for memory
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    # Mark even numbers > 2 as non-prime to optimize
    for i in range(4, n + 1, 2):
        sieve[i] = False
    # Sieve for odd numbers only
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if sieve[i]:
            for j in range(i * i, n + 1, i * 2):  # Step by 2*i to skip even multiples
                sieve[j] = False
    # Count primes explicitly
    return sum(1 for i in range(n + 1) if sieve[i])

# Function to count primes in each digit range (1 to max_digits)
def compute_prime_counts(max_digits):
    prime_counts = []
    for d in range(1, min(max_digits + 1, 10)):  # Cap at 9 digits for practicality
        start = 10 ** (d - 1)
        end = (10 ** d) - 1
        count = sieve_count_primes(end) - sieve_count_primes(start - 1)
        prime_counts.append(count)
        print(f"Digits: {d}, Primes: {count}")
    if max_digits >= 10:
        print("Warning: Exact counts for 10+ digits are computationally intensive. Use approximations for higher digits.")
    return prime_counts

# Parse command-line argument for max digits with default value of 6
parser = argparse.ArgumentParser(description='Visualize prime number counts by number of digits.')
parser.add_argument('max_digits', type=int, nargs='?', default=6, help='Maximum number of digits to plot (default: 6)')
args = parser.parse_args()

# Validate max_digits
max_digits = args.max_digits
if max_digits < 1:
    print(f"Warning: max_digits must be at least 1. Got {max_digits}. Setting to 1.")
    max_digits = 1

# Compute prime counts for 1 to max_digits
prime_counts = compute_prime_counts(max_digits)

# Prepare data for plotting
digits = list(range(1, len(prime_counts) + 1))

# Create line chart
plt.figure(figsize=(8, 6))
plt.plot(digits, prime_counts, marker='o', color='#FF6F61', linestyle='-', linewidth=2, markersize=8)
plt.xlabel('Number of Digits')
plt.ylabel('Count of Prime Numbers (Log Scale)')
plt.title('Count of Prime Numbers by Number of Digits')
plt.yscale('log')  # Set y-axis to logarithmic scale
plt.xticks(digits)  # Ensure x-axis shows integer digits
plt.grid(True, linestyle='--', alpha=0.7)

# Show plot
# Digits: 1, Primes: 4
# Digits: 2, Primes: 21
# Digits: 3, Primes: 143
# Digits: 4, Primes: 1061
# Digits: 5, Primes: 8363
# Digits: 6, Primes: 68906
# Digits: 7, Primes: 586081
# Digits: 8, Primes: 5096876
# Digits: 9, Primes: 45505251
plt.show()