import pandas as pd
from fpdf import FPDF
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def processar_dados(caminho_planilha):
    # Carregar os dados da planilha
    dados = pd.read_csv(caminho_planilha, encoding='utf-8')

    # Verificar as colunas carregadas
    print("Colunas carregadas:", dados.columns)

    # Garantir que os nomes estejam padronizados
    if 'Início do atendimento' not in dados.columns or 'Final do atendimento' not in dados.columns:
        raise ValueError("As colunas necessárias não estão presentes no arquivo CSV.")

    # Converter as colunas de data/hora
    dados['Início do atendimento'] = pd.to_datetime(dados['Início do atendimento'], format='%H:%M:%S', errors='coerce')
    dados['Final do atendimento'] = pd.to_datetime(dados['Final do atendimento'], format='%H:%M:%S', errors='coerce')

    # Calcular o tempo gasto
    dados['Tempo gasto'] = (dados['Final do atendimento'] - dados['Início do atendimento']).dt.total_seconds() / 60

    # Calcular as métricas
    demandas_por_atendente = dados['Atendente'].value_counts()
    tempo_medio_por_atendente = dados.groupby('Atendente')['Tempo gasto'].mean()
    demandas_abertas = dados[dados['Final do atendimento'].isna()]

    return demandas_por_atendente, tempo_medio_por_atendente, demandas_abertas

def gerar_relatorio_pdf(atendente, demandas, tempo_medio, gestor_email, arquivo_saida):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Relatório do Atendente: {atendente}", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Gestor Responsável: {gestor_email}", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Quantidade de demandas: {demandas}", ln=True)
    pdf.cell(200, 10, txt=f"Tempo médio gasto: {tempo_medio:.2f} minutos", ln=True)
    pdf.output(arquivo_saida)


def enviar_email(destinatario, assunto, corpo, anexo):
    remetente = "henriquecaio898@gmail.com"  # Substitua pelo seu e-mail
    senha = "gish gwsh irhq zyby"  # Substitua pela sua senha

    # Configuração do e-mail
    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = assunto

    mensagem.attach(MIMEText(corpo, 'plain'))

    # Anexar o arquivo PDF
    with open(anexo, "rb") as f:
        parte = MIMEBase('application', 'octet-stream')
        parte.set_payload(f.read())
        encoders.encode_base64(parte)
        parte.add_header('Content-Disposition', f"attachment; filename={anexo}")
        mensagem.attach(parte)

    # Enviar o e-mail
    with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, destinatario, mensagem.as_string())

# Exemplo de uso
if __name__ == "__main__":
    caminho_planilha = "atendimentos.csv"  # Substitua pelo caminho correto
    demandas_por_atendente, tempo_medio_por_atendente, demandas_abertas = processar_dados(caminho_planilha)

    for atendente in demandas_por_atendente.index:
        demandas = demandas_por_atendente[atendente]
        tempo_medio = tempo_medio_por_atendente[atendente]
        gestor_email = "caio66419@gmail.com"  # Substitua pelo e-mail correto

        # Gerar relatório PDF
        arquivo_saida = f"relatorio_{atendente}.pdf"
        gerar_relatorio_pdf(atendente, demandas, tempo_medio, gestor_email, arquivo_saida)

        # Enviar relatório por e-mail
        enviar_email(gestor_email, f"Relatório do Atendente {atendente}", "Segue o relatório em anexo.", arquivo_saida)
