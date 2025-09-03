import requests
import json

import gradio_client
from openai import OpenAI

class RequestLLM:
    def __init__(self, api_url, file_name) -> None:
        self._api_url = api_url
        self._file_name = file_name
        
        self._input_csv = f"vm_utils/sistematic_review/{file_name}.csv"
        self._output_csv = f"vm_utils/sistematic_review/{file_name}_output.csv"


    def call_prisma_rag(self):
        prisma_rag = gradio_client.Client(self._api_url)
        
        current_mode = "Basic" 
        context_structure = ""
        upload_File = []
        
        csv_line = [
            """Analysis and identification of dermatological diseases using Gaussian mixture modeling,Gupta C.; Gondhi N.K.; Lehana P.K.,2019,0,1,0,0,0,Unique,0,,,,,,,"Skin diseases are common and are mainly caused by virus, bacteria, fungus, or chemical disturbances. Timely analysis and identification are of utmost importance in order to control the further spread of these diseases. Control of these diseases is even more difficult in rural and resource-poor environments due to a lack of expertise in primary health centers. Hence, there is a need for providing self-assisting and innovative measures for the appropriate diagnosis of skin diseases. Use of mobile applications may provide inexpensive, simple, and efficient solutions for early diagnosis and treatment. This paper investigates the application of the Gaussian mixture model (GMM) based on the analysis and classification of skin diseases from their visual images using a Mahalanobis distance measure. The GMM has been preferred over the convolution neural network (CNN) because of limited resources available within the mobile device. Gray-level co-occurrence matrix (GLCM) parameters contrast, correlation, energy, and homogeneity derived from skin images have been used as the input data for the GMM. The analysis of the results showed that the proposed method is able to predict the classification of skin diseases with satisfactory efficiency. It was also observed that different diseases occupy distinct spatial positions in multidimensional space clustered using the Mahalanobis distance measure. © 2019 Institute of Electrical and Electronics Engineers Inc.. All rights reserved.",10.1109/ACCESS.2019.2929857,Artificial neural network; Convolution neural network; Dermatology; Dermoscopy; Euclidean distance; Gaussian mixture model; Gray level co-occurrence matrix; Mahalanobis distance; Melanoma; Support vector machine; Teledermoscopy; Ultra-violet radiations,21,https://www.scopus.com/inward/record.uri?eid=2-s2.0-85083878180&doi=10.1109%2fACCESS.2019.2929857&partnerID=40&md5=267ef28eb6b976dc0c76aec53a79162e""",
            """Skin lesion detection using adaptive regularized kernel based fuzzy algorithm,Tamije Selvy P.; Shabarish N.; Anitha M.,2019,1,1,0,0,0,Unique,0,,,,,,,"Skin cancer is found to be the worst type of cancer which is generally difficult to predict in early stages. In recent days, it has been proved that Computer Aided Diagnosis (CAD) System provides best result in automatic diagnosis of lesions in skin. The purpose of this research paper is early and automatic diagnosis of lesions in skin. Preprocessing, Segmentation by Adaptive Regularized Kernel Based Fuzzy and feature extraction is done in order to achieve a rapid and reliable diagnosis. This proposed work is implemented on 232 images obtained from International Skin Imaging Collaboration (ISIC) archive. © IJSTR 2019.",,Adaptive Regularized Kernel Based Fuzzy; Computer Aided Diagnosis; Melanoma; Region of Interest; Skin Cancer,0,https://www.scopus.com/inward/record.uri?eid=2-s2.0-85077341582&partnerID=40&md5=f5192b42cef65464ec50527c9c1ed4c9"""
        ]

        try:
            
            for i, input_row in enumerate(csv_line): 
                print(f"input_row: {input_row}")
                
                response = prisma_rag.predict(
                    message=input_row,
                    mode=current_mode,
                    param_3=upload_File,
                    param_4=context_structure,
                    api_name="/chat"
                )
            
                print(f"\n\nfinal response: {response}\n\n")

            self._llm_response = response #json.loads(str(response)) # Converter a string JSON em um dicionário Python
            self._llm_status = 200
            
            print("prisma_rag executado com sucesso!")
        except requests.exceptions.RequestException as e:
            print("Erro ao executar prisma_rag. Código de status:", e)
            self._llm_response = e

    def return_llm(self):
        self.call_prisma_rag()

        return self._llm_response, self._llm_status
    
if __name__ == "__main__":
    api_url = "http://localhost:8001/"
    file_name = "3_survey_systematic_review_02_09_2025"
    
    request_llm = RequestLLM(api_url, file_name)
    response = request_llm.return_llm()
