!pip install crc

import time
import tracemalloc
import os
import matplotlib.pyplot as plt
import platform
import subprocess
from crc import Calculator, Crc16

# @title a) Mensagem Pessoal

MENSAGEM = "Heitor de Souza Alves"
MENSAGEM_BASE = "010010000110010101101001011101000110111101110010001000000110010001100101001000000101001101101111011101010111101001100001001000000100000101101100011101100110010101110011"

# @title b) Gerador Pessoal

# Final 1 - MODBUS
MODBUS = "11000000000000101"

CRC = calcular_crc_manual(MENSAGEM_BASE, MODBUS)
print(CRC)

# @title Verificação do pacote sem adição de erros

calcular_crc_manual(MENSAGEM_BASE + CRC, MODBUS)

# @title Erros

import random
import pandas as pd

random.seed(42) # Geração dos mesmos testes em todas as execuções

resultados = []

for i in range(1, 11):

  CRC = calcular_crc_manual(MENSAGEM_BASE, MODBUS)
  QUADRO_TRANSMITIDO = MENSAGEM_BASE + CRC

  pos = random.randint(0, len(QUADRO_TRANSMITIDO) - 20)
  tamanho = random.randint(3, 16)
  erro = "".join("1" if random.random() > 0.5 else "0" for _ in range(tamanho))

  QUADRO_CORROMPIDO = (
      QUADRO_TRANSMITIDO[:pos] +
      xor_bits(QUADRO_TRANSMITIDO[pos:pos+tamanho], erro) +
      QUADRO_TRANSMITIDO[pos+tamanho:]
  )

  crc_manual = calcular_crc_manual(QUADRO_CORROMPIDO, MODBUS)

  calculator_lib = Calculator(Crc16.MODBUS)
  byte_len = (len(QUADRO_CORROMPIDO) + 7) // 8
  data = int(QUADRO_CORROMPIDO, 2).to_bytes(byte_len, byteorder="big")
  crc_value = calculator_lib.checksum(data)
  crc_lib = format(crc_value, "016b")

  det_manual = (crc_manual != "0" * (len(MODBUS) - 1))
  det_lib = (crc_lib != "0" * 16)

  resultados.append({
      "Teste": i,
      "Posição do Erro": pos,
      "Tamanho da Rajada": tamanho,
      "Padrão de Erro": erro,
      "CRC Manual": crc_manual,
      "CRC Biblioteca": crc_lib,
      "Detectado Manual": det_manual,
      "Detectado Biblioteca": det_lib
  })

df = pd.DataFrame(resultados)
df.style \
  .set_properties(**{'text-align': 'center'}) \
  .set_table_styles(
      [{'selector': 'th', 'props': [('text-align', 'center')]}]
  ) \
.hide(axis="index")

# @title Pontos Cegos

import random
import pandas as pd

random.seed(42) # Geração dos mesmos testes em todas as execuções

pontos_cegos = []

for i in range(11):

  CRC = calcular_crc_manual(MENSAGEM_BASE, MODBUS)
  QUADRO_TRANSMITIDO = MENSAGEM_BASE + CRC

  pos = random.randint(0, len(QUADRO_TRANSMITIDO) - 20)
  tamanho = random.randint(3, 16)
  erro = MODBUS + "0" * i

  QUADRO_CORROMPIDO = QUADRO_TRANSMITIDO + erro

  crc_manual = calcular_crc_manual(QUADRO_CORROMPIDO, MODBUS)

  calculator_lib = Calculator(Crc16.MODBUS)
  byte_len = (len(QUADRO_CORROMPIDO) + 7) // 8
  data = int(QUADRO_CORROMPIDO, 2).to_bytes(byte_len, byteorder="big")
  crc_value = calculator_lib.checksum(data)
  crc_lib = format(crc_value, "016b")

  det_manual = (crc_manual != "0" * (len(MODBUS) - 1))
  det_lib = (crc_lib != "0" * 16)

  pontos_cegos.append({
      "Teste": i,
      "Posição do Erro": pos,
      "Tamanho da Rajada": tamanho,
      "Padrão de Erro": erro,
      "CRC Manual": crc_manual,
      "CRC Biblioteca": crc_lib,
      "Detectado Manual": det_manual,
      "Detectado Biblioteca": det_lib
  })

df = pd.DataFrame(pontos_cegos)
df.style \
  .set_properties(**{'text-align': 'center'}) \
  .set_table_styles(
      [{'selector': 'th', 'props': [('text-align', 'center')]}]
  ) \
.hide(axis="index")
