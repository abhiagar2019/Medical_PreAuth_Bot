#!/usr/bin/env python
# coding: utf-8

# In[1]:


from openai import OpenAI
import os
import time
import medical_preAuthBOT_functions 


# In[2]:


def main():
    #%run medical_preAuthBOT_functions.ipynb

    api_key = os.environ["openai_api_key"] 
    client = OpenAI(api_key=api_key) # OpenAI paid api
    
    guidelines_file  = medical_preAuthBOT_functions.upload_guideline_file(client)    ### Loading guideline document
    instruction_file = medical_preAuthBOT_functions.upload_instruction_file(client) ### Loading instructions document
    patient_file     = medical_preAuthBOT_functions.upload_patient_file(client)          ### Loading Patient document

    ### Creating assistant by passing the relevant parameters
    assistant = medical_preAuthBOT_functions.create_assistant(
        client,
        name = "Medical_PreAuthBOT",
        instructions = """You are an expert medical assistant. 
        Follow the instructions listed here to answer if the requested procedure(s) for the patient should be approved. 
        If not provide details of the additional information that may help in making decision.
        1.	Please use only the information provided to answer. 
        2.	Your goal is to approve the requested procedure only when all the required criterias are met.
        3.	Ingest patient medical record PDF (medical-record-x.pdf) where X is likely a number. 
        4.	Create a timeline of patient’s medical history on complaints, diagnostics, diagnosis, procedures, treatments, medications etc.
        5.	Extract all the CPT code(s) from this document which is usually present after the text ‘Requested Procedure’ to identify which procedure(s) have been recommended by the doctor.
        6.	Display the name of the patient, patient’s date of birth or DOB, calculate the age from the date of birth or DOB and display it. Display MRN if provided. 
        7.	Identify if any conservative treatment has already been attempted from the patient medical record PDFs whether in medical procedures, clinical procedures or notes.
        8.	If a prior conservative treatment has already been attempted and if the treatment was successful or have shown signs of improvements,
        then present evidence that conservative treatment improved the patient’s condition and disapprove the need for the Requested Procedure stating 
        the reason.
        9.	If the conservative treatment was not found or has failed then mention explicitly that ‘conservative treatment was not found or has failed’,
        and then look for the criterias present for Colorectal cancer screening, as indicated by 1 or more of the following to identify if the 
        Requested Procedure should be allowed or not. Please state which condition(s) in the guidelines were used to arrive at the answer.
        a.	Patient has average-risk or higher, if Age is 45 years or older and No colonoscopy in past 10 years 
        b.	Patient has High risk family history, as indicated by 1 or more of the following:1.	Colorectal cancer diagnosed in one or more first-degree 
        relatives of any age and Age 40 years or older and Symptomatic (eg, abdominal pain, iron deficiency anemia, rectal bleeding) 
        2.	Family member with colonic adenomatous polyposis of unknown etiology 
        c.	Juvenile polyposis syndrome diagnosis indicated by 1 or more of the following: 
        1.	Age 12 years or older and symptomatic (eg, abdominal pain, iron deficiency anemia, rectal bleeding, telangiectasia) 
        2.	Age younger than 12 years and symptomatic (eg, abdominal pain, iron deficiency anemia, rectal bleeding, telangiectasia)
        10.	Do not hallucinate or provide incorrect or incomplete information. At any point if you don’t know the answer, just say ‘I cannot arrive at the conclusion. Please provide additional information’. 
        Please request specific information that could be helpful in making a decision.
        11.	Walk me through the process with chain-of-thoughts on how you arrived at the conclusion. 
        12.	At the end, insert two blank lines, and then summarise the final conclusion with the title ‘Conclusion:’ in less than 40 words 
        if the requested procedure should be approved or not. 
        Provide the reason why it should be approved or not approved. In case of indecision, specify what further information would be 
        required to decide.""",
        tools_type = "retrieval",
        model = "gpt-4-1106-preview",
             
        instruction_file_id = instruction_file.id,
        guidelines_file_id = guidelines_file.id,
        patient_file_id = patient_file.id  
    )


    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = "user",
    content = "You are a helpful expert medical assistant. Use the information provided to answer."
    )

    run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id= assistant.id
    )

    while True:
        # Retrieve the run status
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(10)
    
        # Check the status of the run
        if run_status.status == 'completed':
            # If completed, break the loop and process messages
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            break
        elif run_status.status in ['failed', 'error']:
            # If the run fails or encounters an error, handle it appropriately
            print(f"Run encountered an error: {run_status.status}")
            break
        else:
            # If still running, continue to wait
            time.sleep(2)

    if run_status.status in ['failed', 'error']:
        print(f"Run encountered an error: {run_status.status}")
    else: 
        for message in reversed(messages.data):
          print(message.role + ":" + message.content[0].text.value)
    


# In[3]:


if __name__ == "__main__":
    main()


# In[1]:


#!pip freeze > requirements.txt


# In[ ]:




