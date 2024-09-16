def split_file(input_file):
    # Step 1: Read the content of the input file
    with open(input_file, 'r') as file:
        text = file.read()
        paragraphs = text.split('\n')

        # Filter out any empty paragraphs (optional)
        paragraphs = [p for p in paragraphs if p.strip()]

        # Count the paragraphs
        paragraph_count = len(paragraphs)

    # Step 3: Split the content and write to separate files
    for i in range(paragraph_count):
        # # Create part filename
        part_filename = f"part_{i + 1}.txt"

        # Write the chunk to a smaller file
        with open(part_filename, 'w') as part_file:
            part_file.write(paragraphs[i])

        print(f"Created: {part_filename}")


# Example usage
input_file = "paragraphs.txt"
split_file(input_file)

