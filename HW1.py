from docx import Document
import os
import pandas
import re


def get_all_docx_in_current_foleder():
    info =[]
    # go throw all the documants in the directory
    current_path =os.path.join(os.getcwd(),'docx_knesset_protocols')
    
    for file_number,filename in enumerate(os.listdir(current_path)):
        if filename.endswith('docx'):
            
            attributes = filename.split('_')# get the attributes of the file
            #then assigen it to the right variable
            info.append({})
            info[-1]['file_name'] = filename
            info[-1]['number'] = int(attributes[0])# the XX number 

            if attributes[1] == 'ptv':#committee or plenary
                info[-1]['type'] = 'committee'
            elif (attributes[1] == 'ptm'):
                info[-1]['type'] = 'plenary'

            text = Document(os.path.join(current_path,filename))
            #clear the text from B,
            '''for par_number, par in enumerate (text.paragraphs):
                if par.text != '' and par.text[0] == '<': #some the senteces begin with "<" and ends with ">" and does not appear in the document so we remvove them 
                    par.text = par.text[1:-1]
                    text.paragraphs[par_number] = par'''
            info[-1]['text'] = text
            info[-1]['debugging_number'] = attributes[2]
    return info

def clear_name(name): #input a string (name) output the cleared name

    name = name.strip()
    componints = name.split(' ')
    new_name = ""
    open_parentheses =False 
    for comp in componints:
        if '(' in comp:
             open_parentheses = False
             continue
        if open_parentheses:
            continue
        if '"' not in comp and '”' not in comp:#this means that the component is not a short cut
            if ")" in comp: #if we have open_parentheses then we should not inclut what is in it
                if "(" in comp:# if we have closing parentheses then we just dont take this comp
                    continue
                else:# else we must take the following comps until we see closing parentheses
                    open_parentheses = True
            elif comp == "-" or comp == "," or comp == '–' or comp == '-' or comp =='-':#if the name has " - " then take the first part
                break
            else:
                new_name += comp+" "
    new_name = new_name.strip()
    if new_name != "" and new_name.find(':')+1 == len(new_name):
        new_name = new_name[:-1]

    return new_name.strip()



def clean_text(text):
    if text == '':
        return ''
    pattern = re.compile('[א-ת0-9!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ ]+')

    # Find all matches in the input string
    matches = pattern.findall(text)

    # Join the matched characters to form the cleaned string
    cleaned_text = ''.join(matches)
    
    #now we have cleared all the charetars that can be like English letters ,Japanese .. 

    #now we find if there is a non hebrew letters that appears more than one time
    non_alphabetic_characters = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*',
                              '+', ',', '-', '.', '/', ':', ';', '<', '=', '>',
                              '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|',
                              '}', '~'] 
    hebrew_letters = [chr(code) for code in range(0x05D0, 0x05EA + 1)]

    new_text = ''
    i = 0 
    flag_hebrew = False # if we dont have any hebrew then this is not a text
    while i< len(cleaned_text):
        if flag_hebrew == False and cleaned_text[i] in hebrew_letters:
            flag_hebrew = True
        elif flag_hebrew == False:
            i+=1
        if flag_hebrew == True: # the first charecter must be hebrew
            delelte_last = False
            
            while i!=len(cleaned_text) and cleaned_text[i] in non_alphabetic_characters and get_the_next_index_not_space(cleaned_text,i) != len(cleaned_text) and cleaned_text[get_the_next_index_not_space(cleaned_text,i)] in non_alphabetic_characters:
                i=get_the_next_index_not_space(cleaned_text,i)
                delelte_last = True
            if delelte_last:
                i=get_the_next_index_not_space(cleaned_text,i)
            if i!= len(cleaned_text):
                new_text+=cleaned_text[i]
                i+=1

    return new_text

def get_the_next_index_not_space(text,i):
    for j in range(i+1,len(text)):
        if text[j] != ' ':
            return j
    return len(text)
    


data = get_all_docx_in_current_foleder()
possition_types =['היו"ר',]
c = 0 
c1 = 0 

'''
for docx in data:
    if docx["debugging_number"] == '232326.docx':
        for par in docx["text"].paragraphs:
            if par.text != '' and par.text[0] == '<':
                par.text = par.text[1:-1]
            print(par.text[::-1])
'''


temp_data = data
for docx_number,docx in enumerate(temp_data):


    if docx['type'] == 'committee':
        for par_number, par in enumerate (docx['text'].paragraphs):
            if par.text != '' and par.text[0] == '<': #some the senteces begin with "<" and ends with ">" and does not appear in the document so we remvove them 
                par.text = par.text[1:-1]
        first_subject = ''#the first subject the document is talking about
        take_names = 0#a flag to list anither name or not
        i = -1
        c1+=1
        for par in docx['text'].paragraphs:
            i+=1


            #find the first_subject this helps us to get all the people how are in the documant
            if first_subject =='' and  par.text.strip().find('סדר') in [0,1] and par.text.find('יום')>=0 :
                '''print("length = "+str(len(par.text)))
                print('documant number = '+docx['debugging_number'])
                print(par.text.strip())'''

                if len(par.text)>=12: #if this happens then we have the first subject in the same line as the current par
                    if par.text.find(':יום')>=0:# if it has ":" then split with : other wise split with " "
                        first_subject = par.text.split(":", 2)[1]  
                    else:
                        first_subject = par.text.split(" ", 2)[2]
                    first_subject = first_subject.split(',')[0]#if the sentence has more than one subject take the first
                else:# the subject not in the paragraph
                    current_i = i+1
                    while docx['text'].paragraphs[current_i].text == '':
                        current_i+=1
                    first_subject = docx['text'].paragraphs[current_i].text
                    first_subject = first_subject.split(',')[0].strip()#if the sentence has more than one subject take the first 
            
                
                #else:
                    
        #new code
        speaker_name =''
        speaker_text = {}
        first_subject_counter = 2
        for par_number, par in enumerate (docx['text'].paragraphs):
            # some times the chairman opens before the fire subject apear
            if first_subject_counter>0 and 'יו"ר' in par.text and ":" in par.text:
                first_subject_counter = 0
            if first_subject_counter>0 and len(set(par.text.split(' ')).intersection(first_subject.split(' ')))>=(3*len(first_subject.split(' ')))/4:# if we have more than 3/4 of the words interact this is probably the first subject 
                first_subject_counter -=1
            if first_subject_counter ==0:
                #begin to read each speaker data
                symbol_index = par.text.strip().find(":")
                if symbol_index>=0 and symbol_index== len(par.text.strip()) -1 and all(run.underline == True for run in par.runs):# f we arrive at a sentence that has ':' in the end then this is a speaker
                    speaker_name = clear_name(par.text.strip())
                    if speaker_name not in list(speaker_text.keys()):
                        speaker_text[speaker_name] = []

                elif speaker_name!='':
                    text = clean_text(par.text.strip()).strip()
                    # add the text to the speaker after making sure it is not empty and clean
                    if text != '':
                        
                        speaker_text[speaker_name].append(text)
        
        data[docx_number]['speaker_data'] = speaker_text

                    
        
        #end of new code
        #print('documant number = '+docx['debugging_number'])
        #print(first_subject[::-1])


    #creating the csv
columns_name = {'protocol_name':[],'knesset_number':[],'protocol_type':[],'speaker_name':[],'sentence_text':[]}
list_of_speakers = []
df = pandas.DataFrame(columns_name)
for row in data:
    if row['type'] == 'plenary':
        continue
    new_row = {'protocol_name':row['file_name'],'knesset_number':row['number'],'protocol_type':row['type']}
    for speaker in row['speaker_data'].keys():
        list_of_speakers.append(speaker)
        for text in row['speaker_data'][speaker]:
            new_row ['speaker_name'] = speaker
            new_row ['sentence_text'] = text
            df.loc[len(df)] = new_row

speaker_set = set(list_of_speakers)
df.to_csv('our_data.csv',index = False ,encoding='utf-8')
df.to_excel('our_data.xlsx',index = False)    

print('c = '+str(c))

            