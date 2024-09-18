from multiprocessing import Pool, Manager
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

    # Append word counts back to the same file (optional step)
    with open(filename, 'a') as file:
        file.write("\n\nWord Count:\n")
        for word, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True):
            file.write(f"{word}: {count}\n")

    return dict(word_counts)


# Master function to aggregate word counts from workers
# Master function to aggregate word counts from workers
def aggregate_word_counts(filenames, num_processes, global_word_counts):
    with Pool(processes=num_processes) as pool:
        # Count words in each file across worker processes
        word_count_list = pool.map(count_words, filenames)

    # Update the global word count dictionary from worker nodes
    for word_counts in word_count_list:
        for word, count in word_counts.items():
            # Use .get() to safely update the count
            global_word_counts[word] = global_word_counts.get(word, 0) + count



# Main function to split the file, launch workers, and coordinate word counting
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

    # Step 3: Use a Manager dictionary to store global word counts
    with Manager() as manager:
        global_word_counts = manager.dict()  # Shared dictionary across processes

        with Pool(processes=num_processes) as pool:
            # Step 4: Write paragraphs to separate files using multiprocessing
            filenames = pool.map(write_paragraph, enumerate(paragraphs))

        # Step 5: Aggregate word counts from worker nodes
        aggregate_word_counts(filenames, num_processes, global_word_counts)

        # Print the final aggregated word counts
        print("\nAggregated Word Count: ")
        for word, count in sorted(global_word_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"{word}: {count}")

        print(f"\nFinished processing {len(paragraphs)} files.")

        # Optional: Clean up the temporary files (comment this if you want to keep the files)
        # for filename in filenames:
        #     os.remove(filename)
        # print("Temporary files have been removed.")


if __name__ == '__main__':
    # Example usage
    input_file = "paragraphs.txt"
    split_file_and_count_words(input_file)
