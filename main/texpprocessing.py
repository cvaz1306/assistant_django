import spacy
from sympy import symbols, Eq, solve
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import spacy
from collections import Counter
from sympy import symbols, Eq, solve, sympify
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def summarize_text(text, num_sentences=3):
    # Parse the input text with spaCy
    doc = nlp(text)
    
    # Tokenize the text and count word frequencies
    word_freq = Counter()
    for token in doc:
        word_freq[token.text] += 1

    # Get a list of sentences sorted by their position in the document
    sentences = list(doc.sents)
    
    # Rank sentences by word frequency
    ranked_sentences = sorted(sentences, key=lambda s: sum(word_freq[token.text] for token in s), reverse=True)
    
    # Select the top N sentences as the summary
    summary_sentences = ranked_sentences[:num_sentences]
    
    # Combine the selected sentences into a single string
    summary = " ".join(str(sentence) for sentence in summary_sentences)
    
    return summary


# Text Processing
def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.text for token in doc if not token.is_stop and token.is_alpha]
    return keywords

# Math Assistance
def solve_equation(equation_str, variable):
    x = symbols(variable)
    equation = sympify(equation_str)  # Convert string to SymPy expression
    solution = solve(equation, x)
    return solution

# Question Answering
def answer_question(document, question):
    qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", tokenizer="distilbert-base-cased", framework="pt")
    answer = qa_pipeline(question=question, context=document)
    return answer["answer"] if answer["score"] > 0.5 else "Answer not available."


def generate_response(user_input):
    if user_input.lower() == "exit":
        return "Goodbye! Have a great day."
        
    elif "keywords" in user_input.lower():
        text = input("Enter the text: ")
        keywords = extract_keywords(text)
        return f"The keywords in the text are: {', '.join(keywords)}"
        
    elif "summarize" in user_input.lower():
        text = input("Enter the text: ")
        summary = summarize_text(text)
        return f"Here's a brief summary: {summary}"
        
    elif "solve" in user_input.lower():
        equation_str = input("Enter the equation (in terms of x): ")
        variable = input("Enter the variable: ")
        solution = solve_equation(equation_str, variable)
        return f"The solution to the equation is: {solution}"
        
    elif "question" in user_input.lower():
        document = input("Enter the document: ")
        question = input("Ask your question: ")
        answer = answer_question(document, question)
        return f"The answer to your question is: {answer}"
        
    else:
        input_ids = tokenizer.encode(user_input, return_tensors="pt")
        generated_ids = model.generate(input_ids, max_length=100, num_return_sequences=1)
        generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        return generated_text

if __name__ == "__main__":
    main()