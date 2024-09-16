import threading
import os
import re
from collections import Counter


# Function to count words in a small file
def count_words_in_file(filename):
    with open(filename, 'r') as file:
        text = file.read().lower()
        # Tokenize the text into words
        words = re.findall(r'\w+', text)
        # Count the occurrences of each word
        word_counts = Counter(words)
    return dict(word_counts)


# Worker thread function
def thread_worker(item):
    i, paragraph = item
    part_filename = f"part_{i + 1}.txt"

    # Step 1: Write the paragraph to the respective part file
    with open(part_filename, 'w') as part_file:
        part_file.write(paragraph)

    # Step 2: Count words in the file
    word_counts = count_words_in_file(part_filename)

    # Step 3: Write the word count back into the same file
    with open(part_filename, 'a') as part_file:
        part_file.write("\n\nWord Count:\n")
        for word, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True):
            part_file.write(f"{word}: {count}\n")


# Main function to split and count words using threads
def split_file_and_count_words_threading(input_file):
    # Step 1: Read the content of the input file
    with open(input_file, 'r') as file:
        text = file.read()
        paragraphs = text.split('\n')
        # Filter out empty paragraphs (optional)
        paragraphs = [p for p in paragraphs if p.strip()]

    # Step 2: Create threads for each paragraph
    threads = []
    for i, paragraph in enumerate(paragraphs):
        thread = threading.Thread(target=thread_worker, args=((i, paragraph),))
        threads.append(thread)
        thread.start()

    # Step 3: Wait for all threads to finish
    for thread in threads:
        thread.join()

    print(f"\nFinished processing {len(paragraphs)} files.")


# Example usage
if __name__ == '__main__':
    input_file = "paragraphs.txt"
    split_file_and_count_words_threading(input_file)
