import re

import pandas as pd

# Função para limpar os nomes


def limpar_nome(nome):
    return re.sub(r'^\d+\s*-\s*', '', nome).strip()


# Função para limpar o Documento (NF)
def limpar_documento(doc):
    return re.sub(r'^NFE--', '', doc).strip()


def tratar_dados(arquivo: str) -> pd.DataFrame:
    df = pd.read_excel(arquivo)

    # Aplicar a função de limpeza nas colunas
    df['VENDEDOR'] = df['VENDEDOR'].apply(limpar_nome)
    df['CLIENTE'] = df['CLIENTE'].apply(limpar_nome)
    df['Documento'] = df['Documento'].apply(limpar_documento)

    # Limpar a coluna 'Código' e convertê-la para inteiro
    df['Código'] = (
        pd.to_numeric(df['Código'], errors='coerce').fillna(0).astype(int)
    )

    df.dropna(inplace=True)

    # Salvar o DataFrame limpo em um novo arquivo Excel
    df.to_excel('seu_arquivo_limpo.xlsx', index=False)

    return df


arquivo = 'VENDAS MARCELO 20-23.xlsx'
dados = tratar_dados(arquivo)
