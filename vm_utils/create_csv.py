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
        self._batch_size = 100  # número de linhas antes de salvar no CSV

    def read_csv_lines(self):
        """Lê todas as linhas do CSV de entrada, separando cabeçalho e conteúdo"""
        with open(self._input_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            header = rows[0]  # cabeçalho
            lines = rows[1:]  # conteúdo
        return header, lines
    
    def save_jsons_to_csv(self, json_list):
        """Converte a lista de JSONs em linhas CSV e faz append no arquivo de saída"""
        if not json_list:
            return

        # Pegando as chaves do primeiro JSON para o header
        fieldnames = list(json_list[0].keys())

        # Abrindo o CSV no modo append, usando aspas duplas
        with open(self._output_csv, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            
            # Se arquivo está vazio, escreve o header
            if f.tell() == 0:
                writer.writeheader()
            
            for json_obj in json_list:
                writer.writerow(json_obj)

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
                
                # Converte string JSON para dict apenas se necessário
                if isinstance(response, str):
                    try:
                        response = json.loads(response)
                    except json.JSONDecodeError:
                        print(f"Atenção: resposta não é JSON válido: {response}")
                        response = {"raw_response": response}
                
                # Adiciona o campo "Document Title" ao JSON
                response["Document Title"] = document_title
                
                print(f"response {i} processado:\n\n{response}\n")

                all_responses.append(response)
                batch_responses.append(response)

                # A cada batch de 100, salva no CSV e limpa o batch
                if i % self._batch_size == 0:
                    self.save_jsons_to_csv(batch_responses)
                    batch_responses = []
                    print(f"{i} linhas processadas e salvas no CSV.")

            except requests.exceptions.RequestException as e:
                print(f"Erro ao processar a linha {i}: {e}")

        # Salva as linhas restantes que não completaram o batch
        if batch_responses:
            self.save_jsons_to_csv(batch_responses)

        print(f"Processamento concluído! Tempo total: {time.time() - start_time:.2f} segundos")
        return all_responses
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Processa CSV com Prisma RAG e salva respostas em CSV.")
    parser.add_argument("file_name", type=str, help="Nome do arquivo CSV (sem extensão)")
    parser.add_argument("--path", type=str, default=os.getcwd(), help="Caminho do diretório onde está o CSV (default: diretório atual)")
    parser.add_argument("--api_url", type=str, default="http://localhost:8001/", help="URL da API Gradio")

    args = parser.parse_args()

    request_llm = RequestLLM(args.api_url, args.file_name, args.path)
    responses = request_llm.call_prisma_rag()
    
    print(f"Total de respostas recebidas: {len(responses)}")
