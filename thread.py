import threading
from queue import Queue
from typing import Dict, List


def process_paragraph(paragraph: str) -> Dict[str, int]:
    """
    Count word occurrences in a paragraph.

    Args:
    paragraph (str): The paragraph to process.

    Returns:
    Dict[str, int]: A dictionary with words as keys and their counts as values.
    """
    word_counts = {}
    words = paragraph.split()
    for word in words:
        word = word.lower()  # Convert to lowercase for case-insensitive counting
        word_counts[word] = word_counts.get(word, 0) + 1
    return word_counts


def worker(queue: Queue, results: List[Dict[str, int]]):
    """
    Worker function for threads. Processes paragraphs from the queue and stores results.

    Args:
    queue (Queue): A queue of paragraphs to process.
    results (List[Dict[str, int]]): A list to store the word count dictionaries.
    """
    while True:
        paragraph = queue.get()
        if paragraph is None:
            break
        word_counts = process_paragraph(paragraph)
        results.append(word_counts)
        queue.task_done()


def main(filename: str = 'paragraphs.txt', num_threads: int = 4):
    """
    Main function to coordinate the threaded word count process.

    Args:
    filename (str): The name of the file to process (default is 'paragraphs.txt').
    num_threads (int): The number of threads to use (default is 4).
    """
    queue = Queue()
    results = []

    # Start worker threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(queue, results))
        thread.start()
        threads.append(thread)

    # Read file and add paragraphs to the queue
    with open(filename, 'r') as file:
        for paragraph in file:
            if paragraph.strip():  # Ignore empty paragraphs
                queue.put(paragraph)

    # Add sentinel values to signal threads to exit
    for _ in range(num_threads):
        queue.put(None)

    # Wait for all tasks to complete
    queue.join()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Combine results from all threads
    total_counts = {}
    for result in results:
        for word, count in result.items():
            total_counts[word] = total_counts.get(word, 0) + count

    # Print the combined word counts
    print("Combined word counts:")
    for word, count in sorted(total_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()