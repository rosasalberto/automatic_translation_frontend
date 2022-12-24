import requests
import json
import time

import streamlit as st

from config import domain

def list_to_string(lst, separator=', '):
    str1 = ""
    for ele in lst:
        str1 += ele + separator
    return str1[:-1]

def mark_toxic_words(text_list, toxic_words_list):
    copy_ = text_list.copy()

    for i in range(len(text_list)):
        for toxic_word in toxic_words_list[i]:
            copy_[i] = copy_[i].replace(toxic_word, "<span style='color:red'>**{}**</span>".format(toxic_word))
            #copy_[i] = copy_[i].replace(toxic_word, '***{}***'.format(toxic_word))
    return copy_

def get_input_lang(text_list, lang_detected_list, scores_list):
    str_lang = ""
    for i in range(len(lang_detected_list)):
        str_lang += "**{} (Confidence: {})**: <br/>{}<br/><br/>".format(lang_detected_list[i], round(scores_list[i],2), text_list[i])
    return str_lang  

def format_markdown(d):
    str_mkdown = ""

    str_mkdown += "# Input text\n"

    # getting input
    input_text_list = d['text']
    toxic_words_input = [[] for i in range(len(input_text_list))]

    # formatting input string
    input_text_list = mark_toxic_words(input_text_list, toxic_words_input)
    input_text_str = list_to_string(input_text_list, separator='. ')

    # adding to the string
    str_mkdown += "{}\n".format(input_text_str) # (replace text of input, if toxic word in x then add **word**)

    str_mkdown += "### Languages Detected\n"
    # languages detected
    lang_detected_list = d['lid']['lang']
    scores_list = d['lid']['scores']
    lang_str = get_input_lang(input_text_list, lang_detected_list, scores_list)
    str_mkdown += "{}\n".format(lang_str)
    return str_mkdown

endpoint = 'lid/'

st.title('Language detection')

text_input = st.text_area('Type text to translate ...', value="Attention is all you need. Vaya dia de mierda que hace. But no lo se with certeza",
                          height=80, placeholder="Attention is all you need")

button_col, inp_lang_col, col_exec = st.columns([1,2,2])
button = button_col.button('Detect')

if button:
    start_time = time.time()

    # do query
    text_input = text_input.replace('\n','')
    resp = requests.post(domain+endpoint, json=text_input)

    # print response
    d = json.loads(resp.text)
    st.write(d)

    # print execution time
    time_lapsed = time.time() - start_time
    col_exec.write("Execution time: {}s".format(round(time_lapsed,2)))

    # markdown response
    str_mkdown = format_markdown(d)
    st.markdown(str_mkdown, unsafe_allow_html=True)