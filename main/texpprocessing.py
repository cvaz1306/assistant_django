import base64
import io
import traceback
from matplotlib import pyplot as plt
import numpy as np
import spacy
from sympy import Symbol, symbols, Eq, solve, sympify
import sympy
from transformers import pipeline
import os
from filemanager.models import *
import os
from filemanager.models import *
from .models import *
from collections import Counter
from urllib.parse import quote
from numpy import *
import docx
from filemanager.views import readFile
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import requests
from bs4 import BeautifulSoup
from transformers import T5ForConditionalGeneration, T5Tokenizer

class docxprocessor():
    def processDocx(docx_file):
        doc = docx.Document(docx_file)
        #
        document_text = ""
        for para in doc.paragraphs:
            document_text += para.text + "\n    "
        return document_text
from filemanager.views import readFile
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class intResp():
    # Load spaCy model
    sq=""
    file_obj=File()
    user_commands = []
    inputsRequired=0
    inputsCompleted=0
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    tokenizerX = T5Tokenizer.from_pretrained("google/flan-t5-large")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
    modelX = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large")
    actionIns={
        "exit":0,
        "keywords":1,
        "summarize":1,
        "solve":1,
        "question":2,
        "question_about":1,
        "question_about":1,
        "invalid":0,
        "graph":1,
        "search":0,
    }
    resps={
        "exit":[],
        "keywords":["Enter the document..."],
        "summarize":["Enter the document..."],
        "solve":["Enter a math problem..."],
        "question":["Enter a document...", "Ask me a question about the document..."],
        "question_about":["Ask me a question about the document..."],
        "question_about":["Ask me a question about the document..."],
        "invalid":["I dont understand"],
        "graph":["Enter an equation"],
        "search":[""],
    }
    actionX=""
    nlp = spacy.load("en_core_web_sm")
    new_user_input_ids = tokenizer.encode("" + tokenizer.eos_token, return_tensors='pt')
    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat([tokenizer.encode("" + tokenizer.eos_token, return_tensors='pt'), new_user_input_ids], dim=-1) if 1 > 0 else new_user_input_ids
    # generated a response while limiting the total chat history to 1000 tokens, 
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    # pretty print last ouput tokens from bot



    
def search_question(question):
    url = f"https://www.google.com/search?q={question}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = soup.find_all('div', class_='BNeawe')
    srz=""
    for resu in search_results:
        srz=srz+"\n"+resu.get_text()
    return srz#search_results[0].get_text()

def summarize_textX(text):
    tokenizerX = T5Tokenizer.from_pretrained("google/flan-t5-large")
    inputs = tokenizerX.encode("summarize, excluding any links, urls, or questions. Please use normal english and write authoritatively: " + text, return_tensors="pt", max_length=512, truncation=True)
    outputs = intResp.modelX.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizerX.decode(outputs[0])
    
    return summary
def readDocx(reqId):
    file_obj = get_object_or_404(models.File, id=reqId)

    try:
        # Check if the file exists
        if os.path.exists(file_obj.file.path):
            with open(file_obj.file.path, 'rb') as file:
                if(file_obj.file.path.endswith('.docx')):
                    print('File is a document')
                    filecontent=docxprocessor.processDocx(file)
                    print(f"File Content: {filecontent}")
                return filecontent
    except Exception as e:
        print(f"Error: {e}")
        return "Error"
    
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
    return answer["answer"]# if answer["score"] > 0.5 else "Answer not available."
def process(fff, input):
    
    resp=""
    print(f"Ins Completed: {intResp.inputsCompleted}; ")
    if intResp.inputsCompleted == 0:
        intResp.user_commands.append(input)
        input_lower = input.lower()

        if "exit" in input_lower:
            intResp.actionX = "exit"
        elif "keywords" in input_lower:
            intResp.actionX = "keywords"
        elif "summarize" in input_lower:
            intResp.actionX = "summarize"
        elif "solve" in input_lower:
            intResp.actionX = "solve"
        elif "question" in input_lower:
            intResp.actionX = "question"

            # Check if there's a document filename specified in the user's message
            document_name = None
            if "question about" in input_lower:
                document_name = input_lower.split("question about", 1)[1].strip()
                print(f"File: {intResp.file_obj.file}")
                try:
                    # Query the database to find the File object with a matching name
                    intResp.file_ob = File.objects.all().filter(name=document_name).first()

                    # Now you have the File object, and you can handle it accordingly
                    print(f"User wants to ask a question about {document_name}")
                    print(f"File object: {intResp.file_obj}")
                    
                    intResp.actionX = "question_about"
                    # You can further process or use the file_object her
                except File.DoesNotExist:
                    # Handle the case when the specified file does not exist in the database
                    print(f"File '{document_name}' not found in the database.")
        elif "graph" in input_lower:
            intResp.actionX = "graph"
        elif "search" in input_lower:
            intResp.actionX="search"
            intResp.sq = input_lower.split("search", 1)[1].strip()
            print(f"Search Query: {intResp.sq}")
            
        else:
            if intResp.actionX.lower() == "":
                intResp.actionX = "invalid"
            else:
                intResp.actionX = ""

        print(f"Action X: '{intResp.actionX}'")
        intResp.inputsRequired=intResp.actionIns.get(intResp.actionX, 0)
        resp = intResp.resps.get(intResp.actionX, ["Hello"])[intResp.inputsCompleted]
    if(intResp.inputsCompleted <= intResp.inputsRequired and not intResp.user_commands==0):
        intResp.user_commands.append(input)
        print(f"Input: {input.lower()}; ActionX: {intResp.actionX}; Inputs completed: {intResp.inputsCompleted}")
        if(not intResp.inputsCompleted==intResp.inputsRequired):
            resp = intResp.resps.get(intResp.actionX, ["Hello"])[intResp.inputsCompleted]
        
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
        print(f"InpArr: {inpArr}")
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
            string = base64.b64encode(buf.read()).decode()
            uri = 'data:image/png;base64,' + quote(string)  # Use urllib.parse.quote to encode the string
            html = """<img class='graph' src='"""+uri+"""' />"""
            return html
        except Exception as e:
            return f"Error: {e}"
    elif "question_about"==intResp.actionX:
        intResp.action = "question_about"
        responseX=""
        responseX=readFile(20)
        document = responseX
        question = inpArr[2]
        answer = answer_question(document, question)
        print(f"answer: {answer}")
        return f"The answer to your question is: {answer}"
    elif "question" in inpArr[0].lower():
        intResp.action = "question_about"
        document = inpArr[2]
        question = inpArr[3]
        answer = answer_question(document, question)
        print(f"answer: {answer}")
        return f"The answer to your question is: {answer}"
    elif "search" in inpArr[0].lower():
        res=summarize_textX(search_question(intResp.sq))
        print(res)
        return res
    else:
        
        inputs = intResp.tokenizerX.encode(f"Assume you are a helpful AI assistant that uses the transformers library written by HuggingFace with a model trained BY google on a large amount of data. You are based on the django web framework. You can do anything that requires only text input and/or output. Follow the following instructions meticuluously: Answer with good grammar while remaining honest, age appropriate, and useful for any user: {inpArr[0]}", return_tensors="pt", max_length=512, truncation=True)
        outputs = intResp.modelX.generate(inputs, max_length=150, min_length=20, length_penalty=2.0, num_beams=4, early_stopping=True)
        op = intResp.tokenizerX.decode(outputs[0])
        return op