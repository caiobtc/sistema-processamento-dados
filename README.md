# Projeto: Automação de Relatórios de Atendimentos
Este projeto visa processar dados de atendimentos, gerar relatórios em formato PDF e enviá-los por e-mail automaticamente. Ele utiliza as bibliotecas `pandas`, `FPDF` e `smtplib` para realizar as tarefas necessárias.

## Funcionalidades

1. **Processamento de Dados**: 
   - Carrega dados de um arquivo CSV.
   - Calcula o tempo gasto em cada atendimento.
   - Gera métricas como número de demandas por atendente e tempo médio gasto por atendente.

2. **Geração de Relatórios PDF**:
   - Cria relatórios personalizados para cada atendente, contendo informações sobre o número de demandas, tempo médio gasto e o gestor responsável.

3. **Envio de E-mails**:
   - Envia os relatórios gerados para o e-mail do gestor responsável.
