def answer(str):
    words = str.split('+')
    polish_words = []
    for word in words:
        letters = word.split("*")
        polish_words.append(letters)
        polish_words.append(["*" for i in range(len(letters)-1)])
    polish_answer = ""
    for word in polish_words:
        for letter in word:
            polish_answer = polish_answer + letter
    for i in range(len(words)-1):
        polish_answer = polish_answer + "+"
    return polish_answer
