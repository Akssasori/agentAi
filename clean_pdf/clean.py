import fitz  # PyMuPDF
import io
from pathlib import Path
import os
import time

def extract_text_from_pdf(input_pdf_path, output_pdf_path=None):
    """
    Extrai o texto de um PDF, removendo as imagens.
    
    Args:
        input_pdf_path (str): Caminho para o arquivo PDF de entrada
        output_pdf_path (str, opcional): Caminho para salvar o PDF sem imagens
                                         Se não for fornecido, apenas retorna o texto
    
    Returns:
        str: Texto extraído do PDF
    """
    print(f"Abrindo o arquivo PDF: {input_pdf_path}")
    start_time = time.time()
    
    # Abre o documento PDF
    try:
        pdf_document = fitz.open(input_pdf_path)
        print(f"PDF aberto com sucesso. Total de {len(pdf_document)} páginas.")
    except Exception as e:
        print(f"Erro ao abrir o PDF: {e}")
        return ""
    
    all_text = ""
    
    # Se um caminho de saída for fornecido, cria um novo PDF apenas com texto
    if output_pdf_path:
        print("Criando novo PDF sem imagens...")
        output_pdf = fitz.open()
        
        # Processa cada página
        for page_num in range(len(pdf_document)):
            print(f"Processando página {page_num+1}/{len(pdf_document)}...")
            page = pdf_document[page_num]
            
            # Extrai o texto da página
            text = page.get_text()
            all_text += text + "\n\n"
            
            # Cria uma nova página no PDF de saída
            new_page = output_pdf.new_page(width=page.rect.width, height=page.rect.height)
            
            # Insere apenas o texto na nova página
            new_page.insert_text((50, 50), text)
            
            # Mostra porcentagem de conclusão a cada página
            percent_done = ((page_num + 1) / len(pdf_document)) * 100
            print(f"Progresso: {percent_done:.1f}% concluído")
        
        # Cria o diretório de saída se não existir
        os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
        
        # Salva o novo PDF sem imagens
        print(f"Salvando PDF sem imagens em: {output_pdf_path}")
        output_pdf.save(output_pdf_path)
        output_pdf.close()
        print("PDF sem imagens salvo com sucesso!")
    else:
        # Se não precisar criar um novo PDF, apenas extrai o texto
        print("Extraindo apenas o texto do PDF...")
        for page_num in range(len(pdf_document)):
            print(f"Extraindo texto da página {page_num+1}/{len(pdf_document)}...")
            page = pdf_document[page_num]
            text = page.get_text()
            all_text += text + "\n\n"
            
            # Mostra porcentagem de conclusão a cada página
            percent_done = ((page_num + 1) / len(pdf_document)) * 100
            print(f"Progresso: {percent_done:.1f}% concluído")
    
    # Fecha o documento original
    pdf_document.close()
    
    elapsed_time = time.time() - start_time
    print(f"Extração concluída em {elapsed_time:.2f} segundos.")
    
    return all_text

def save_text_to_file(text, output_text_path):
    """
    Salva o texto extraído em um arquivo de texto.
    
    Args:
        text (str): Texto a ser salvo
        output_text_path (str): Caminho para o arquivo de texto de saída
    """
    print(f"Preparando para salvar texto em: {output_text_path}")
    
    # Cria o diretório de saída se não existir
    os.makedirs(os.path.dirname(output_text_path), exist_ok=True)
    
    # Conta o número de caracteres para mostrar estatísticas
    char_count = len(text)
    line_count = text.count('\n') + 1
    
    # Salva o texto no arquivo
    try:
        with open(output_text_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Texto salvo com sucesso! ({char_count} caracteres, {line_count} linhas)")
    except Exception as e:
        print(f"Erro ao salvar o texto: {e}")

# Exemplo de uso com os caminhos específicos do Windows
if __name__ == "__main__":
    print("Iniciando processamento do PDF...")
    
    # Use barras normais ou barras duplas para caminhos no Windows
    input_pdf = r"C:\teste\chatBotAi\chatbot_rag\202502_lista-precos_fev25.pdf"
    output_dir = r"C:\teste\chatBotAi\clean_pdf"
    
    # Verifica se o arquivo de entrada existe
    if not os.path.exists(input_pdf):
        print(f"ERRO: O arquivo de entrada não existe: {input_pdf}")
        print("Verifique se o caminho está correto e tente novamente.")
        exit(1)
        
    output_pdf = os.path.join(output_dir, "lista-precos_fev25_sem_imagens.pdf")
    output_text = os.path.join(output_dir, "lista-precos_fev25_texto.txt")
    
    print("="*50)
    print(f"Arquivo de entrada: {input_pdf}")
    print(f"Diretório de saída: {output_dir}")
    print("="*50)
    
    # Extrai o texto e cria um novo PDF sem imagens
    print("Iniciando extração de texto...")
    extracted_text = extract_text_from_pdf(input_pdf, output_pdf)
    
    # Salva o texto extraído em um arquivo de texto
    print("Salvando texto extraído...")
    save_text_to_file(extracted_text, output_text)
    
    print("="*50)
    print(f"PROCESSAMENTO CONCLUÍDO!")
    print(f"Texto extraído salvo em: {output_text}")
    print(f"PDF sem imagens salvo em: {output_pdf}")
    print("="*50)