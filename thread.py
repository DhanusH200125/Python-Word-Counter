import threading
import re
from collections import Counter

def count_words_in_file(filename): # Fn to count words in a small file
    with open(filename, 'r') as file:
        text = file.read().lower()
        words = re.findall(r'\w+', text)
        word_counts = Counter(words)
    return dict(word_counts) # returning the dictionary of word count

def thread_worker(item): # Worker thread function
    i, paragraph = item
    part_filename = f"part_{i + 1}.txt"
    with open(part_filename, 'w') as part_file:
        part_file.write(paragraph)

    word_counts = count_words_in_file(part_filename)
    print(f"Part-{i + 1}: {word_counts}\n")

    with open(part_filename, 'a') as part_file:
        part_file.write("\n\nWord Count:\n")
        for word, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True):
            part_file.write(f"{word}: {count}\n") # Writing the word count back into the same file

# Main function to split and count words using threads
def split_file_and_count_words_threading(input_file):
    with open(input_file, 'r') as file:
        text = file.read()
        paragraphs = text.split('\n')
        paragraphs = [p for p in paragraphs if p.strip()]

    threads = []
    for i, paragraph in enumerate(paragraphs):
        thread = threading.Thread(target=thread_worker, args=((i, paragraph),))
        threads.append(thread) # Create threads for each paragraph
        thread.start()

    for thread in threads:
        thread.join()

    print(f"\nFinished processing {len(paragraphs)} files.")

if __name__ == '__main__':
    input_file = "paragraphs.txt"
    split_file_and_count_words_threading(input_file)
