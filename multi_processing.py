from multiprocessing import Pool
import multiprocessing
import os
import re
from collections import Counter


# Function to write each paragraph to a separate file
def write_paragraph(item):
    i, paragraph = item
    part_filename = f"part_{i + 1}.txt"
    with open(part_filename, 'w') as part_file:
        part_file.write(paragraph)
    return part_filename


# Function to count words in a file and append the word counts into the file
def count_words(filename):
    with open(filename, 'r') as file:
        text = file.read().lower()
        # Tokenize the text into words
        words = re.findall(r'\w+', text)
        # Count the occurrences of each word
        word_counts = Counter(words)

    # Append word counts back to the same file
    with open(filename, 'a') as file:
        file.write("\n\nWord Count:\n")
        for word, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True):
            file.write(f"{word}: {count}\n")

    return filename


# Main function to split the file and process word counting with multiprocessing
def split_file_and_count_words(input_file, num_processes=None):
    # Step 1: Read the content of the input file
    with open(input_file, 'r') as file:
        text = file.read()
        paragraphs = text.split('\n')
        # Filter out any empty paragraphs (optional)
        paragraphs = [p for p in paragraphs if p.strip()]

    # Step 2: Set the number of processes to use
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()  # Use all available CPU cores

    with Pool(processes=num_processes) as pool:
        # Step 3: Write paragraphs to separate files using multiprocessing
        filenames = pool.map(write_paragraph, enumerate(paragraphs))

        # Step 4: Count words and append word counts in each file
        pool.map(count_words, filenames)

    print(f"\nFinished processing {len(paragraphs)} files.")

    # Optional: Clean up the temporary files (comment this if you want to keep the files)
    # for filename in filenames:
    #     os.remove(filename)
    # print("Temporary files have been removed.")


if __name__ == '__main__':  # Corrected line here
    # Example usage
    input_file = "paragraphs.txt"
    split_file_and_count_words(input_file)
