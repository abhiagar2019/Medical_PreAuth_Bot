#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


def upload_instruction_file(client):
    
    instruction_file = client.files.create(
                                file=open("instructions/instructions.docx", 'rb'),
                                purpose="assistants"
                                          )
    return instruction_file


# In[ ]:


def upload_guideline_file(client):
    guidelines_file =  client.files.create(
                                file=open("instructions/colonoscopy-guidelines.pdf", 'rb'),
                                purpose="assistants"
                                          )
    return guidelines_file


# In[ ]:


# Function to open file dialog and get file path
import tkinter as tk
from tkinter import filedialog

def capturing_patient_file_path():
    #print("Welcome to the File Uploader")
    print("Please select the Patient Medical Record for pre-authorization check: ")

    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename()
    if file_path:  # Check if a file was selected
        print("Selected file path:", file_path)    
    else:
        print("No file was selected.")
    root.destroy()
    
    return file_path


# In[ ]:


def upload_patient_file(client):
    patient_file=client.files.create(
                                    file=open(capturing_patient_file_path(), 'rb'),    
                                    purpose="assistants"
    )
                                
    return patient_file


# In[ ]:


def create_assistant(client, name, instructions, tools_type, model, patient_file_id, guidelines_file_id, instruction_file_id):
    
    assistant = client.beta.assistants.create(
    name = name,
    instructions = instructions,
    tools = [{"type":tools_type}],
    model = model,
    file_ids = [patient_file_id]# , instruction_file_id ] #guidelines_file_id
    )

    return assistant


# In[ ]:


#jupyter nbconvert --to script 'medical_preAuthBOT_functions.ipynb'

