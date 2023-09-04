import base64
import io
from matplotlib import pyplot as plt
import numpy as np
import spacy
from sympy import Symbol, symbols, Eq, solve, sympify
import sympy
from transformers import pipeline
import urllib3
from .models import *
from collections import Counter
from urllib.parse import quote
from numpy import *
import json
#Imports
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
        "invalid":0,
        "graph":1,
    }
    resps={
        "exit":[],
        "keywords":["Enter the document..."],
        "summarize":["Enter the document..."],
        "solve":["Enter a math problem..."],
        "question":["Enter a document...", "Ask me a question about the document..."],
        "invalid":["I dont understand"],
        "graph":["Enter an equation"]
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
def extract_keywords(text):
    doc = intResp.nlp(text)
    keywords = [f"<code class=\"code\">{token.text}</code>" for token in doc if not token.is_stop and token.is_alpha]
    return keywords
def solve_equation(equation_str):
    print(equation_str)
    print(eval("5+5")==eval(equation_str))
    solution=eval(equation_str)
    return solution
def answer_question(document, question):
    qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", tokenizer="distilbert-base-cased", framework="pt")
    print(f"Document: {document}\n\nQuestion: {question}")
    
    answer = qa_pipeline(question=question, context=document)
    return answer["answer"] if answer["score"] > 0.5 else "Answer not available."
def process(fff, input):
    
    resp=""
    print(f"Ins Completed: {intResp.inputsCompleted}; ")
    if(intResp.inputsCompleted==0):
        intResp.user_commands.append(input)
        input_lower = input.lower()  
        if input_lower == "exit":
            intResp.actionX = "exit"
        elif input_lower == "keywords":
            intResp.actionX = "keywords"
        elif input_lower == "summarize":
            intResp.actionX = "summarize"
        elif input_lower == "solve":
            intResp.actionX = "solve"
        elif input_lower == "question":
            intResp.actionX = "question"
        elif input_lower == "graph":
            intResp.actionX = "graph"
        else:
            if intResp.actionX.lower() == "":
                intResp.actionX = "invalid"
            else:
                intResp.actionX = ""

        print(f"Action X: '{intResp.actionX}'")
        intResp.inputsRequired=intResp.actionIns.get(intResp.actionX)
        resp = intResp.resps.get(intResp.actionX)[intResp.inputsCompleted]
    if(intResp.inputsCompleted <= intResp.inputsRequired and not intResp.user_commands==0):
        intResp.user_commands.append(input)
        print(f"Input: {input.lower()}; ActionX: {intResp.actionX}; Inputs completed: {intResp.inputsCompleted}")
        if(not intResp.inputsCompleted==intResp.inputsRequired):
            resp = intResp.resps.get(intResp.actionX)[intResp.inputsCompleted]
        
    intResp.inputsCompleted=intResp.inputsCompleted+1
    
    if(intResp.inputsCompleted>intResp.inputsRequired):
        output=gr(inpArr=intResp.user_commands)
        intResp.inputsRequired=0
        intResp.inputsCompleted=0
        resp = output
        intResp.user_commands.clear()
    return resp
def gr(inpArr):
    if inpArr[0].lower() == "exit":
        return "Goodbye! Have a great day."
        
    elif "keywords" in inpArr[0].lower():
        text = inpArr[2]
        keywords = extract_keywords(text)
        return f"The keywords in the text are: {', '.join(keywords)}"
        
    elif "summarize" in inpArr[0].lower():
        intResp.action = "summarize"
        text = inpArr[2]
        print(f"Summarizing: {text}")
        summary = summarize_text(text)
        return f"Here's a brief summary: {summary}"
        
    elif "solve" in inpArr[0].lower():
        intResp.action = "solve"
        print(f"InpArr: {inpArr[1]}")
        equation_str = inpArr[2]
        solution = solve_equation(equation_str)
        return f"The solution to the equation is: {solution}"
    
    elif "graph" in inpArr[0].lower():
        intResp.action = "graph"
        print(f"InpArr: {inpArr[2]}")
        equation_str = inpArr[2]
        sympy_eq = sympify("Eq(" + equation_str.replace("=", ",") + ")")
        solution=list(solve(sympy_eq))[0]
        
        sx=str(list(sympy.solve(sympy_eq, sympy.Symbol('y')))[0])
        print(f"Solution: {sx}")
        try:
            x = np.linspace(-20, 20, 1000)
            y = eval(f'{sx}')
            
            # Create a figure and axes
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # Create the plot
            ax.plot(x, y)
            
            # Save the plot to a BytesIO buffer
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read()).decode()  # Decode the base64 bytes to a string
            
            uri = 'data:image/png;base64,' + quote(string)  # Use urllib.parse.quote to encode the string
            html = f'<img class=\"graph\" src=\"{uri}\" />'
            return html
        except Exception as e:
            return f"Error: {e}"
    
    elif "question" in inpArr[0].lower():
        intResp.action = "question"
        document = inpArr[2]
        question = inpArr[3]
        answer = answer_question(document, question)
        print(f"answer: {answer}")
        return f"The answer to your question is: {answer}"
    
    else:
        print(json.dumps(inpArr))
        intResp.inputsCompleted=0
        return "I'm sorry. I can't understand your request."
        
        

