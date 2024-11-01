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
    Remove caracteres indesejados de um valor monetário e o converte
    para float.

    Args:
        valor_str (str or float): O valor a ser tratado.

    Returns:
        float: O valor tratado como um número decimal.
    """
    if isinstance(valor_str, float):
        return valor_str
    else:
        valor_str = (
            valor_str.replace('R$', '')
            .replace('.', '')
            .replace(',', '.')
            .strip()
        )
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

    # Retirar linhas que possuem algum valor nulo.
    df.dropna(inplace=True)

    df.columns = df.columns.str.upper()

    # Aplicar a função de limpeza nas colunas.
    df['VENDEDOR'] = df['VENDEDOR'].apply(limpar_nome)
    df['CLIENTE'] = df['CLIENTE'].apply(limpar_nome)
    df['DOCUMENTO'] = df['DOCUMENTO'].apply(limpar_documento)

    # Limpar a coluna 'Código' e convertê-la para inteiro.
    df['CÓDIGO'] = (
        pd.to_numeric(df['CÓDIGO'], errors='coerce').fillna(0).astype(int)
    )

    # Limpar a coluna 'Data'
    df['DATA'] = df['DATA'].apply(tratar_data)

    # Tratar os valores nas colunas 'Vl. Unit.' e 'Vl. Total'
    df['VL. UNIT.'] = df['VL. UNIT.'].apply(tratar_valor)
    df['VL. TOTAL'] = df['VL. TOTAL'].apply(tratar_valor)

    df = df[(df['QUANTIDADE'] >= 0) & (df['VL. TOTAL'] >= 0)]

    df.to_excel('seu_arquivo_limpo.xlsx', index=False)

    return df
