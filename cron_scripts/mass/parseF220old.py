import os
import pandas as pd
import numpy as np
import sqlite3
import re

def parse_fort220(file):
    """
    Faz o parsing do arquivo fort.220 e retorna um DataFrame formatado.

    Args:
        file (str): Caminho para o arquivo fort.220.

    Returns:
        pd.DataFrame: DataFrame com os dados extraídos do fort.220.
    """
    with open(file, 'r') as log:
        lines = log.readlines()
    
    # Listas para armazenar os dados
    date_list, hour_list, JRows, costRows, gNormRows, gnorm, reduction = [], [], [], [], [], [], []

    for line in lines:
        line = line.strip()
        if not line:
            continue  # Ignora linhas vazias

        # Identifica padrões de data/hora no início da linha
        match = re.match(r'(\d{8})\s+(\d{2})\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)', line)
        if match:
            date, hour, jrow, cost, gNormRow, gnormVal, redVal = match.groups()
            
            # Converte os valores para os tipos apropriados
            date_list.append(date)
            hour_list.append(int(hour))
            JRows.append(int(jrow))
            costRows.append(float(cost))
            gNormRows.append(float(gNormRow))
            gnorm.append(float(gnormVal))
            reduction.append(float(redVal))

    # Criação do DataFrame com os valores coletados
    data = np.column_stack([date_list, hour_list, JRows, costRows, gNormRows, gnorm, reduction])
    df = pd.DataFrame(data, columns=["date", "hour", "outer", "inner", "cost", "gnorm", "reduction"])

    # Ajustando tipos corretamente
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")  # Converte para formato de data
    df["hour"] = df["hour"].astype(int)

    return df

def save_to_db(df, db_path="database.db"):
    """
    Salva o DataFrame no banco de dados SQLite.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados a serem armazenados.
        db_path (str): Caminho do banco de dados SQLite.
    """
    conn = sqlite3.connect(db_path)
    df.to_sql("cost_table", conn, if_exists="append", index=False)
    conn.close()

if __name__ == "__main__":
    file_path = "caminho/para/fort.220"  # Substituir pelo caminho real do arquivo
    if os.path.exists(file_path):
        df = parse_fort220(file_path)
        if not df.empty:
            save_to_db(df)
            print("Dados salvos no banco de dados com sucesso.")
        else:
            print("O arquivo não contém dados válidos.")
    else:
        print("Arquivo fort.220 não encontrado.")
