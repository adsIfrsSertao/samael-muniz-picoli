import re

import pandas as pd


def limpar_nome(nome: str) -> str:
    """
    Remove um prefixo numérico e espaços em branco de um nome.

    Args:
        nome (str): O nome a ser limpo.

    Returns:
        str: O nome limpo, sem prefixos numéricos e espaços em branco.
    """
    return re.sub(r'^\d+\s*-\s*', '', nome).strip()

#

def limpar_documento(doc: str) -> str:
    """
    Remove o prefixo 'NFE--' ou 'NFCE--' de um número de documento.

    Args:
        doc (str): O documento a ser limpo.

    Returns:
        str: O documento limpo, sem o prefixo 'NFE--'.
    """
    return re.sub(r'^(NFE--|NFCE--)', '', doc).strip()



def tratar_data(data_str: str) -> pd.Timestamp:
    """
    Converte uma string de data no formato 'dd/mm/aaaa' para um objeto de data.

    Args:
        data_str (str): A string da data a ser convertida.

    Returns:
        pd.Timestamp: A data convertida.
    """
    return pd.to_datetime(data_str, format='%d/%m/%Y').date()



def tratar_valor(valor_str) -> float:
    """
    Remove caracteres indesejados de um valor monetário e o converte para float.

    Args:
        valor_str (str or float): O valor a ser tratado.

    Returns:
        float: O valor tratado como um número decimal.
    """
    if isinstance(valor_str, float):
        return valor_str
    else:
        valor_str = valor_str.replace("R$", "").replace(".", "").replace(",", ".").strip()
        return float(valor_str) 



def tratar_dados(arquivo: str) -> pd.DataFrame:
    """
    Lê um arquivo Excel, limpa e trata os dados, e retorna um DataFrame limpo.

    Args:
        arquivo (str): O caminho para o arquivo Excel a ser processado.

    Returns:
        pd.DataFrame: Um DataFrame contendo os dados tratados e limpos.
    """
    df = pd.read_excel(arquivo)

    # Aplicar a função de limpeza nas colunas.
    df['VENDEDOR'] = df['VENDEDOR'].apply(limpar_nome)
    df['CLIENTE'] = df['CLIENTE'].apply(limpar_nome)
    df['Documento'] = df['Documento'].apply(limpar_documento)

    # Limpar a coluna 'Código' e convertê-la para inteiro.
    df['Código'] = pd.to_numeric(df['Código'], errors='coerce').fillna(0).astype(int)

    # Limpar a coluna 'Data'
    df['Data'] = df['Data'].apply(tratar_data)

    # Tratar os valores nas colunas 'Vl. Unit.' e 'Vl. Total'
    df['Vl. Unit.'] = df['Vl. Unit.'].apply(tratar_valor)
    df['Vl. Total'] = df['Vl. Total'].apply(tratar_valor)

    # Remover linhas com valores negativos nas colunas 'Quantidade' e 'Vl. Total'
    df = df[(df['Quantidade'] >= 0) & (df['Vl. Total'] >= 0)]

    # Retirar linhas que possuem algum valor nulo.
    df.dropna(inplace=True)

    df.to_excel('seu_arquivo_limpo.xlsx', index=False)

    return df