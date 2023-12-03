import re

#filename = "2023_PV_impresso_D1_CD1_Original.txt"
filename = "2023_PV_impresso_D2_CD7_original.txt"

dia = "D1" if "D1" in filename else "D2"

# Read and print the content of the file
with open(filename, 'r', encoding='utf-8') as file:
    text = file.read()

# Define a regex pattern to match the start of a question (e.g., "QUESTÃO 12")
question_start_pattern = re.compile(r'QUESTÃO (\d+)')

# Define a regex pattern to match the end of a question (e.g., "QUESTÃO 13")
question_end_pattern = re.compile(r'QUESTÃO (\d+)')

# Find all matches of question starts in the text
question_starts = [match.start() for match in question_start_pattern.finditer(text)]

# Find all matches of question ends in the text
question_ends = [match.start() for match in question_end_pattern.finditer(text)]

inicio = 91 # 1
total = 180 #90 + 5
cinco_primeiras = False
# Iterate through question numbers 1 to 45
for question_number in range(inicio, total + 2):
    print("")
    # Find the index of the question start and end
    try:
        start = question_starts[question_number - 1 - 90]
        if question_number < total:
            end = question_ends[question_number - 90] if question_number < total else len(text)
    except IndexError:
        # Handle the case where there is no match for a specific question
        print(f"Question {question_number} not found")
        continue

    # Extract the question content between start and end
    question_content = text[start:end].strip()
    if question_number == total:
        question_content = text[start:].strip()



    # Replace the extracted content with an empty string in the original text
    #text = text[:start] + text[end:]

    if dia == "D1":
        if cinco_primeiras is False:
            # Generate the filename
            filename = f"{dia}_questao_{question_number:02d}_eng.txt"
        else:
            filename = f"{dia}_questao_{(question_number - 5):02d}.txt"
    else:
        filename = f"{dia}_questao_{(question_number):02d}.txt"
    print(question_content)


    # Save the question content to the file
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(question_content)

    print(f"Question {question_number} saved to {filename}")
    if question_number == 5 and cinco_primeiras is False and dia == "D1":
        cinco_primeiras = True
        #question_number = 1