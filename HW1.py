from docx import Document
import os

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
        if open_parentheses:
            continue
        if '"' not in comp:#this means that the component is not a short cut
            if ")" in comp: #if we have open_parentheses then we should not inclut what is in it
                if "(" in comp:# if we have closing parentheses then we just dont take this comp
                    continue
                else:# else we must take the following comps until we see closing parentheses
                    open_parentheses = True
            elif comp == "-" or comp == "," or comp == '–' or comp == '-' or comp =='-':#if the name has " - " then take the first part
                break
            else:
                new_name += comp+" "

    return new_name.strip()



def clean_text(text):
    return text

data = get_all_docx_in_current_foleder()
possition_types =['היו"ר',]
c = 0 
c1 = 0 

for docx in data:
    if docx["debugging_number"] == '232326.docx':
        for par in docx["text"].paragraphs:
            if par.text != '' and par.text[0] == '<':
                par.text = par.text[1:-1]
            print(par.text[::-1])



for docx_number,docx in enumerate(data):


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
            if first_subject_counter>0 and 'יו"ר' in par.text and ":" in par.text:
                first_subject_counter = 0
            if first_subject_counter>0 and len(set(par.text.split(' ')).intersection(first_subject.split(' ')))>3:# if we have more than 3 word intersection this is probably the first subject 
                first_subject_counter -=1
            if first_subject_counter ==0:
                symbol_index = par.text.strip().find(":")
                if symbol_index>=0 and symbol_index== len(par.text.strip()) -1:
                    speaker_name = clear_name(par.text.strip())
                    if speaker_name not in list(speaker_text.keys()):
                        speaker_text[speaker_name] = []
                elif speaker_name!='':
                    text = clean_text(par.text.strip())
                    if text != '':

                        speaker_text[speaker_name].append(text)
        data[docx_number]['speaker_data'] = speaker_text

                    

        #end of new code
        print('documant number = '+docx['debugging_number'])
        print(first_subject[::-1])

            
        #if first_subject =='':
            #print (docx['debugging_number'])
print('c = '+str(c))

            