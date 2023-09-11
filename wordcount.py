import numpy as np
import matplotlib.pyplot as plt
import statistics
input_text = input("Give me some words and I will count them for you:\n")
words = input_text.split()
word_count = []
for word in words :
        word_count.append(len(word))
print(f"Total characters in the text: {len(input_text)}")
print(f"Total words in the text: {word_count}")
print(f"Length of word {len(word_count)}")
if len(word_count) > 1:
    stdev = statistics.stdev(word_count)
    mean = statistics.mean(word_count)
    normal = statistics.NormalDist(mean,stdev)
    print(f"Average of word lengths: {mean:.2f}")
    print(f"Variance of word lengths: {stdev:.2f}")
else:
    print("Standard Deviation cannot be calculated with fewer than 2 words.")
x = np.linspace(-3 * stdev, 3 * stdev, 1000)
pdf_values = [normal.pdf(val) for val in x]
plt.figure(figsize=(8, 6))
plt.plot(x, pdf_values, label='PDF')
plt.title('Normal Distribution PDF')
plt.xlabel('X')
plt.ylabel('Probability Density')
plt.grid(True)
plt.legend()
plt.show()