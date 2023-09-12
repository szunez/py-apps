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
words = input_text.split()
word_count = []
for word in words :
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
initial_guess = [2, 1] # Initial guess for parameters (you can adjust this)
result = minimize(neg_log_likelihood, initial_guess, args=(word_count,), method='L-BFGS-B')
k_estimated, theta_estimated = result.x
x = np.linspace(0, 20, 1000)
pdf_values = gamma.pdf(x, k_estimated, loc=0, scale=theta_estimated)
textbox = f"Mean: {mean:.2f}\nStd Dev: {stdev:.2f}\nK: {k_estimated:.2f}\nTheta: {theta_estimated:.2f}"
plt.figure(figsize=(8, 6))
plt.plot(x, pdf_values, 'r-', lw=2, label='Gamma PDF')
plt.title('Distribution of word length')
plt.xlabel('Word length')
plt.ylabel('Probability Density')
plt.xlim(0,20)
plt.grid(True)
plt.legend()
plt.text(16, 0.15, textbox, bbox=dict(facecolor='white', alpha=0.5))
plt.show()