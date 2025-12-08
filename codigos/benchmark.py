!pip install crc

import time
import tracemalloc
import os
import matplotlib.pyplot as plt
import platform
import subprocess
from crc import Calculator, Crc16

def xor_bits(a, b):
    """Realiza XOR bit a bit entre duas strings binárias de mesmo comprimento."""
    resultado = []
    for i in range(len(a)):
        if a[i] == b[i]:
            resultado.append('0')
        else:
            resultado.append('1')
    return "".join(resultado)

def calcular_crc_manual(dados_bits: str, gerador_bits: str) -> str:
    """Calcula o CRC via simulação de divisão polinomial em strings binárias."""
    r = len(gerador_bits) - 1
    mensagem_aumentada = list(dados_bits + '0' * r)
    len_dados = len(dados_bits)
    len_gerador = len(gerador_bits)

    for i in range(len_dados):
        if mensagem_aumentada[i] == '1':
            janela_atual_str = "".join(mensagem_aumentada[i : i + len_gerador])
            resultado_xor = xor_bits(janela_atual_str, gerador_bits)

            for j in range(len(resultado_xor)):
                mensagem_aumentada[i + j] = resultado_xor[j]

    return "".join(mensagem_aumentada[-r:])

print("--- Iniciando Benchmark ---")

print(f"Sistema: {platform.system()} {platform.release()}")
try:
    model_name_output = subprocess.check_output("cat /proc/cpuinfo | grep 'model name' | uniq", shell=True).decode().strip()
    processor_name = model_name_output.replace('model name\t: ', '')
    print(f"Processador (Ambiente Colab): {processor_name}")
except Exception as e:
    print(f"Processador: Não foi possível identificar automaticamente. Erro: {e}")
print("\n---")

calculator_lib = Calculator(Crc16.MODBUS)
polinomio_manual = "11000000000000101"
tamanhos_bytes = [1500, 4500, 9000]

resultados = {
    "tamanhos": tamanhos_bytes,
    "tempo_manual": [], "tempo_lib": [],
    "mem_manual": [], "mem_lib": [] # Em KiB
}

print("Rodando testes (a implementação manual pode demorar um pouco)...")
print(f"{'TAMANHO (bytes)':<18} | {'TEMPO MANUAL (s)':<18} | {'TEMPO LIB (s)':<18}")
print("-" * 100)

for tamanho in tamanhos_bytes:
    mensagem_bytes = os.urandom(tamanho)
    mensagem_bits = "".join(format(byte, '08b') for byte in mensagem_bytes)

    tracemalloc.start()
    t_start = time.perf_counter()
    _ = calcular_crc_manual(mensagem_bits, polinomio_manual)
    t_end = time.perf_counter()
    _, mem_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    resultados["tempo_manual"].append(t_end - t_start)
    resultados["mem_manual"].append(mem_peak / 1024)

    tracemalloc.start()
    t_start = time.perf_counter()
    _ = calculator_lib.checksum(mensagem_bytes)
    t_end = time.perf_counter()
    _, mem_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    resultados["tempo_lib"].append(t_end - t_start)
    resultados["mem_lib"].append(mem_peak / 1024)

    print(f"{tamanho:<18} | {resultados['tempo_manual'][-1]:<18.5f} | {resultados['tempo_lib'][-1]:<18.8f}")

print("\n--- Gerando Gráficos ---")

plt.style.use('seaborn-v0_8-darkgrid')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Gráfico 1: Tempo
ax1.plot(resultados["tamanhos"], resultados["tempo_manual"], marker='o', linestyle='-', color='red', label='Manual (Manipulação de String)')
ax1.plot(resultados["tamanhos"], resultados["tempo_lib"], marker='s', linestyle='--', color='blue', label='Biblioteca (Otimizada)')
ax1.set_title('Gráfico 1: Comparação de Tempo de Execução (CRC)')
ax1.set_xlabel('Tamanho da Mensagem (Bytes)')
ax1.set_ylabel('Tempo (segundos)')
ax1.legend()

# Gráfico 2: Memória
ax2.plot(resultados["tamanhos"], resultados["mem_manual"], marker='o', linestyle='-', color='red', label='Manual (Manipulação de String)')
ax2.plot(resultados["tamanhos"], resultados["mem_lib"], marker='s', linestyle='--', color='blue', label='Biblioteca (Otimizada)')
ax2.set_title('Gráfico 2: Comparação de Pico de Alocação de Memória (CRC)')
ax2.set_xlabel('Tamanho da Mensagem (Bytes)')
ax2.set_ylabel('Memória (KiB)')
ax2.legend()

plt.tight_layout()
plt.show()

print("\n--- Benchmark Concluído ---")
