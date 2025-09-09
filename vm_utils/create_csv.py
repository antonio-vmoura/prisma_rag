import requests
import json
import csv
import time
import gradio_client
import argparse
import os

class RequestLLM:
    def __init__(self, api_url, file_name, path) -> None:
        self._api_url = api_url
        self._file_name = file_name
        
        self._input_csv = f"{path}/sistematic_review/{file_name}.csv"
        self._output_csv = f"{path}/sistematic_review/response/{file_name}_output.csv"
        self._error_csv = f"{path}/sistematic_review/response/{file_name}_errors.csv"
        
        # Cria a pasta 'response' se não existir
        os.makedirs(os.path.dirname(self._output_csv), exist_ok=True)
        os.makedirs(os.path.dirname(self._error_csv), exist_ok=True)
        
        # self._batch_size = 5  # número de linhas antes de salvar no CSV

    def read_csv_lines(self):
        """Lê todas as linhas do CSV de entrada, separando cabeçalho e conteúdo"""
        with open(self._input_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            header = rows[0]  # cabeçalho
            lines = rows[1:]  # conteúdo
        return header, lines
    
    def save_successful_rows_to_csv(self, json_list):
        """Converte a lista de JSONs de sucesso em linhas CSV e faz append no arquivo de saída"""
        if not json_list:
            return

        # Assume que todos os JSONs aqui são válidos e bem-sucedidos
        fieldnames = [
            "Proposed_Model", "Skin_Task", "Architecture_Type", "Combines_Methods", "Main_Objective",
            "Feature_Extraction", "Cancer_Type", "Database_Used", "Number_Images", "Balanced_Dataset",
            "Image_Preprocessing", "Validation_Type", "Transfer_Learning", "Data_Augmentation", "Compared_Baselines", 
            "Evaluation_Metrics", "Best_Result", "Compared_SOTA", "Tested_Different_Datasets", "Limitations", "Document Title"
        ]
        
        # Verifica se o arquivo já existe para decidir se escreve o cabeçalho
        file_exists = os.path.isfile(self._output_csv)

        with open(self._output_csv, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            if not file_exists or f.tell() == 0:
                writer.writeheader()
            for json_obj in json_list:
                writer.writerow(json_obj)
                
    def save_error_row_to_csv(self, header, row):
        """Salva a linha original do CSV que causou erro em um arquivo de erros"""
        # Verifica se o arquivo de erro já existe para decidir se escreve o cabeçalho
        file_exists = os.path.isfile(self._error_csv)
        
        with open(self._error_csv, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            if not file_exists or f.tell() == 0:
                writer.writerow(header) # Escreve o cabeçalho do arquivo original
            writer.writerow(row) # Escreve a linha que deu erro

    def call_prisma_rag(self):
        prisma_rag = gradio_client.Client(self._api_url)
        current_mode = "Basic"
        context_structure = ""
        upload_File = []

        header, lines = self.read_csv_lines()
        all_responses = []
        batch_responses = []

        start_time = time.time()

        for i, row in enumerate(lines, start=1):
            
            # Ignora linhas vazias
            if not row or all(cell.strip() == "" for cell in row):
                print(f"Linha {i} ignorada (vazia).")
                continue
            
            input_row = ','.join(row)
            document_title = row[0]  # primeira coluna do CSV
            
            try:
                response = prisma_rag.predict(
                    message=input_row,
                    mode=current_mode,
                    param_3=upload_File,
                    param_4=context_structure,
                    api_name="/chat"
                )
                
                print(f"response {i} processado:\n\n{response}\n")
                
                try: # Tenta converter a resposta para JSON
                    # Converte string JSON para dict
                    response_json = json.loads(response)
                except (json.JSONDecodeError, TypeError):
                    print(f"Atenção: resposta da linha {i} não é um JSON válido. Salvando linha no arquivo de erros.")
                    self.save_error_row_to_csv(header, row)
                    continue # Pula para a próxima linha

                # Se a conversão foi bem-sucedida, processa o JSON
                response_json["Document Title"] = document_title
                
                all_responses.append(response_json)
                batch_responses.append(response_json)                
                    
                try:
                    self.save_successful_rows_to_csv(batch_responses)
                    print(f"{i} linhas processadas e salvas no CSV.\n")
                except Exception as e:
                    print(f"Um erro ocorreu ao salvar a linha {i}: {e}. Salvando linha no arquivo de erros.")
                    self.save_error_row_to_csv(header, row)
                finally:
                    batch_responses = []

            except requests.exceptions.RequestException as e:
                print(f"Erro de conexão ao processar a linha {i}: {e}. Salvando linha no arquivo de erros.")
                self.save_error_row_to_csv(header, row)
            except Exception as e:
                print(f"Um erro inesperado ocorreu na linha {i}: {e}. Salvando linha no arquivo de erros.")
                self.save_error_row_to_csv(header, row)

        # Salva as linhas restantes que não completaram o batch
        if batch_responses:
            self.save_successful_rows_to_csv(batch_responses)

        print(f"Processamento concluído! Tempo total: {time.time() - start_time:.2f} segundos")
        
        return all_responses
    
if __name__ == "__main__":
    #python3 create_csv.py 3_survey_systematic_review_02_09_2025 --path "$(pwd)" --api_url "http://localhost:8001/"
    #python3 create_csv.py 3_survey_systematic_review_02_09_2025_errors --path "$(pwd)" --api_url "http://localhost:8001/"
    #python3 create_csv.py test_systematic_review_1 --path "$(pwd)" --api_url "http://localhost:8001/"
    
    parser = argparse.ArgumentParser(description="Processa CSV com Prisma RAG e salva respostas em CSV.")
    parser.add_argument("file_name", type=str, help="Nome do arquivo CSV (sem extensão)")
    parser.add_argument("--path", type=str, default=os.getcwd(), help="Caminho do diretório onde está o CSV (default: diretório atual)")
    parser.add_argument("--api_url", type=str, default="http://localhost:8001/", help="URL da API Gradio")

    args = parser.parse_args()

    request_llm = RequestLLM(args.api_url, args.file_name, args.path)
    responses = request_llm.call_prisma_rag()
    
    print(f"Total de respostas recebidas: {len(responses)}")
