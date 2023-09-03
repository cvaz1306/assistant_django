import spacy
from sympy import symbols, Eq, solve, sympify
from transformers import pipeline
from .models import *
from collections import Counter
class intResp():
    # Load spaCy model
    user_commands = []
    inputsRequired=0
    inputsCompleted=0
    actionIns={
        "exit":0,
        "keywords":1,
        "summarize":1,
        "solve":1,
        "question":2,
        "invalid":0
    }
    resps={
        "exit":[],
        "keywords":["Enter the document..."],
        "summarize":["Enter the document..."],
        "solve":["Enter a math problem..."],
        "question":["Enter a document...", "Ask me a question about the document..."],
        "invalid":["I dont understand"],
    }
    actionX=""
    nlp = spacy.load("en_core_web_sm")
def summarize_text(text, num_sentences=3):
    # Parse the input text with spaCy
    doc = intResp.nlp(text)
    
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
    doc = intResp.nlp(text)
    keywords = [token.text for token in doc if not token.is_stop and token.is_alpha]
    return keywords

# Math Assistance
def solve_equation(equation_str):
    equation = sympify(equation_str)  # Convert string to SymPy expression
    solution = solve(equation, x)
    return solution

# Question Answering
def answer_question(document, question):
    qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", tokenizer="distilbert-base-cased", framework="pt")
    answer = qa_pipeline(question=question, context=document)
    return answer["answer"] if answer["score"] > 0.5 else "Answer not available."

    # Initialize a variable to store the user's commands

    
def process(fff, input):
    if(intResp.inputsCompleted==0):
        intResp.user_commands.append(input)
        actionX=""
        actionX+="exit" if input.lower() == "exit" else ""
        actionX+="keywords" if input.lower() == "keywords" else ""
        actionX+="summarize" if input.lower() == "summarize" else ""
        actionX+="solve" if input.lower() == "solve" else ""
        actionX+="question" if input.lower() == "question" else ""
        actionX+="invalid" if actionX.lower() =="" else ""
        intResp.inputsRequired=intResp.actionIns.get(actionX)
        return intResp.resps.get(actionX)[intResp.inputsCompleted]
    if(intResp.inputsCompleted < intResp.inputsRequired and not intResp.user_commands==0):
        intResp.user_commands.append(input)
        return intResp.resps.get(actionX)[intResp.inputsCompleted]
        
    intResp.inputsCompleted=intResp.inputsCompleted+1
    if(intResp.inputsCompleted==intResp.inputsRequired):
        output=gr(inpArr=intResp.user_commands)
        intResp.inputsRequired=0
        intResp.inputsCompleted=0
        return output
def gr(inpArr):
    if inpArr[0].lower() == "exit":
        return "Goodbye! Have a great day."
        
    elif "keywords" in inpArr[0].lower():
        text = inpArr[1]
        keywords = extract_keywords(text)
        return f"The keywords in the text are: {', '.join(keywords)}"
        
    elif "summarize" in inpArr[0].lower():
        intResp.action="summarize"
        text = inpArr[1]
        summary = summarize_text(text)
        return f"Here's a brief summary: {summary}"
        
    elif "solve" in inpArr[0].lower():
        intResp.action="solve"
        equation_str = inpArr[1]
        solution = solve_equation(equation_str)
        return f"The solution to the equation is: {solution}"
        
    elif "question" in inpArr[0].lower():
        intResp.action="question"
        document = inpArr[1]
        question = inpArr[2]
        answer = answer_question(document, question)
        return f"The answer to your question is: {answer}"
        
    else:
        return "I'm sorry. I can't understand your request."
        

def generate_response(user_input):
    if(action == ""):
        if user_input.lower() == "exit":
            return "Goodbye! Have a great day."
            
        elif "keywords" in user_input.lower():
            action="keywords"
            text = input("Enter the text: ")
            keywords = extract_keywords(text)
            return f"The keywords in the text are: {', '.join(keywords)}"
            
        elif "summarize" in user_input.lower():
            action="summarize"
            text = input("Enter the text: ")
            summary = summarize_text(text)
            return f"Here's a brief summary: {summary}"
            
        elif "solve" in user_input.lower():
            action="solve"
            equation_str = input("Enter the equation (in terms of x): ")
            variable = input("Enter the variable: ")
            solution = solve_equation(equation_str, variable)
            return f"The solution to the equation is: {solution}"
            
        elif "question" in user_input.lower():
            action="question"
            document = input("Enter the document: ")
            question = input("Ask your question: ")
            answer = answer_question(document, question)
            return f"The answer to your question is: {answer}"
            
        else:
            return "I'm sorry. I can't understand your request."
    else:
        if(action=="keywords"):
            action=""
        if(action=="keywords"):
            action=""
        if(action=="keywords"):
            action=""
        if(action=="keywords"):
            action=""
        if(action=="keywords"):
            action=""