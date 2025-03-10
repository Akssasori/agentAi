import pdfplumber
import os

def pdf_to_structured_txt(input_pdf, output_dir):
    # Cria o diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)

    # Define o caminho do TXT de saída
    base_name = os.path.basename(input_pdf).replace(".pdf", ".txt")
    output_txt = os.path.join(output_dir, base_name)

    with pdfplumber.open(input_pdf) as pdf:
        with open(output_txt, 'w', encoding='utf-8') as txt_file:
            for page_number, page in enumerate(pdf.pages, start=1):
                print(f"Processando página {page_number}...")  # Log de progresso
                
                # Extrai texto
                text = page.extract_text()
                if text:
                    txt_file.write(f"=== Página {page_number} ===\n")
                    txt_file.write(text + "\n\n")
                    txt_file.flush()  # Força a escrita no arquivo

                # Extrai tabelas
                tables = page.extract_tables()
                for i, table in enumerate(tables, start=1):
                    txt_file.write(f"--- Tabela {i} ---\n")
                    for row in table:
                        cleaned_row = [str(cell).strip() if cell is not None else "" for cell in row]
                        txt_row = " | ".join(cleaned_row)
                        txt_file.write(txt_row + "\n")
                    txt_file.write("\n")
                    txt_file.flush()  # Força a escrita no arquivo

    print(f"Arquivo TXT gerado em: {output_txt}")

# Configuração dos caminhos
input_pdf = r"C:\teste\chatBotAi\chatbot_rag\202502_lista-precos_fev25.pdf"
output_dir = r"C:\teste\chatBotAi\clean_pdf"

# Executa a conversão
pdf_to_structured_txt(input_pdf, output_dir)
