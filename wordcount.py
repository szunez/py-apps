import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import scipy.stats as stats
from scipy.optimize import minimize
from scipy.stats import gamma

def neg_log_likelihood(params, word_count):
    k, theta = params
    if k <= 0 or theta <= 0:
        return np.inf  # Ensure positive parameters
    return -np.sum(gamma.logpdf(word_count, k, loc=0, scale=theta))

input_text = input("Give me some words and I will count them for you:\n")
input_label = input("\nThanks! If you would like to label this text you can enter that here:\n")
if input_label != "" :
    label = ": ["+input_label+" ]"
words = input_text.split()
word_count = []
for word in words:
    word_count.append(len(word))
print(f"Total characters in the text: {len(input_text)}")
print(f"Total words in the text: {word_count}")
print(f"Length of word {len(word_count)}")
if len(word_count) > 1:
    stdev = np.std(word_count)
    mean = np.mean(word_count)
    normal = norm(loc=mean, scale=stdev)
    print(f"Average of word lengths: {mean:.2f}")
    print(f"Variance of word lengths: {stdev:.2f}")
else:
    print("Standard Deviation cannot be calculated with fewer than 2 words.")
initial_guess = [2, 1]  # Initial guess for parameters (you can adjust this)
result = minimize(neg_log_likelihood, initial_guess, args=(word_count,), method='L-BFGS-B')
k_estimated, theta_estimated = result.x

# Calculate the word lengths and their frequencies
word_lengths = list(range(1, max(word_count) + 1))
word_length_counts = [word_count.count(length) for length in word_lengths]

x = np.arange(1, max(word_count) + 1)  # Word lengths as x-axis
x_gamma = np.linspace(0, 20, 1000)

# Calculate the predicted frequency using the gamma PDF
pdf_values = gamma.pdf(x_gamma, k_estimated, loc=0, scale=theta_estimated)
predicted_frequency = pdf_values * len(word_count)  # Scale PDF by total word count

textbox = f"Mean: {mean:.2f}\nStd dev: {stdev:.2f}\nK: {k_estimated:.2f}\nTheta: {theta_estimated:.2f}"

# Plot the gamma PDF
plt.figure(figsize=(8, 6))
plt.plot(x_gamma, predicted_frequency, 'r-', lw=2, label='Gamma fit')
plt.title('Distribution of word length'+label)
plt.xlabel('Word length [ characters ]')
plt.ylabel('Actual frequency [ count ]')
plt.grid(True)
plt.xlim(0, 20)

# Plot the bar chart for frequency of word lengths
plt.bar(x, word_length_counts, alpha=0.5, label='Actual data')

# Legend and textbox positioning
plt.legend(loc='upper right')
plt.text(15.8, max(predicted_frequency)*0.8, textbox, bbox=dict(facecolor='white', alpha=0.5))

plt.show()
