import json
import csv
import argparse
import os

class JsonlToCsvMapper:
    def __init__(self, file_name, path) -> None:
        self._file_name = file_name

        # Arquivos de entrada/saída
        self._input_csv = f"{path}/sistematic_review/{file_name}.csv"
        self._jsonl_file = f"{path}/sistematic_review/response/{file_name}_errors.jsonl"
        self._output_csv = f"{path}/sistematic_review/{file_name}_errors.csv"

    def read_csv_as_dict(self):
        """Lê o CSV de entrada e cria um dict indexado pelo título (primeira coluna)."""
        with open(self._input_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            header = rows[0]
            data = rows[1:]
        # cria índice: título -> linha
        index = {row[0]: row for row in data if row}
        return header, index

    def process_jsonl(self, header, index):
        """Lê o JSONL, encontra correspondência no CSV e salva no novo CSV."""
        mapped_rows = []

        with open(self._jsonl_file, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, start=1):
                try:
                    js = json.loads(line.strip())
                except json.JSONDecodeError:
                    print(f"Linha {line_number}: JSON inválido -> {line}")
                    continue

                title = js.get("Document Title")
                if not title:
                    print(f"Linha {line_number}: sem campo 'Document Title'")
                    continue

                row = index.get(title)
                if row:
                    mapped_rows.append(row)
                else:
                    print(f"Título não encontrado no CSV: {title}")

        # salva CSV de saída
        if mapped_rows:
            with open(self._output_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerow(header)
                writer.writerows(mapped_rows)

        print(f"Arquivo salvo em: {self._output_csv}")
        print(f"Total de linhas mapeadas: {len(mapped_rows)}")

    def run(self):
        header, index = self.read_csv_as_dict()
        self.process_jsonl(header, index)


if __name__ == "__main__":
    #python3 create_csv.py 3_survey_systematic_review_02_09_2025_bkp --path "$(pwd)"
    
    parser = argparse.ArgumentParser(description="Mapeia títulos do JSONL para linhas do CSV original.")
    parser.add_argument("file_name", type=str, help="Nome base do arquivo CSV (sem extensão)")
    parser.add_argument("--path", type=str, default=os.getcwd(), help="Caminho base dos arquivos")
    
    args = parser.parse_args()

    mapper = JsonlToCsvMapper(args.file_name, args.path)
    mapper.run()
