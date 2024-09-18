
def split_file(input_file): # defining splitFile function
    with open(input_file, 'r') as file:
        text = file.read()
        paragraphs = text.split('\n')
        paragraphs = [p for p in paragraphs if p.strip()]
        paragraph_count = len(paragraphs)

    for i in range(paragraph_count):
        part_filename = f"part_{i + 1}.txt" # Create part filename
        with open(part_filename, 'w') as part_file:
            part_file.write(paragraphs[i])  # Write the chunk to a smaller file

        print(f"Created: {part_filename}")

if __name__ == '__main__':
    inputFile = "paragraphs.txt"
    split_file(inputFile)
    