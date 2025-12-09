Laboratório de Redes: Implementação e Análise de CRC

Disciplina: Redes de Computadores - UFCG

Grupo 10:
- Jefferson Ribeiro Brasil (123110470)
- Giulia Leticia de Mesquita Aragão (121210663)
- Nicole Brito Maracajá (123111413)
- Heitor de Souza Alves (123110811)

📖 Sobre o Projeto

Este laboratório tem como objetivo explorar o funcionamento do CRC (Cyclic Redundancy Check), um dos mecanismos mais importantes para detecção de erros na camada de enlace. O projeto combina teoria matemática, implementação prática e análise de desempenho.
O trabalho foi estruturado para demonstrar como a divisão polinomial binária garante a integridade dos dados transmitidos e quais são as diferenças práticas entre uma implementação didática e uma biblioteca de produção.

🗂️ Estrutura do Laboratório

O desenvolvimento foi dividido em três etapas principais:
1. Implementação Manual
  - Desenvolvimento "do zero" do algoritmo de cálculo do CRC.
  - Objetivo: Compreender a lógica de "janela deslizante" e a aritmética módulo-2 (operações XOR).
  - Método: Simulação de hardware (Shift Register) utilizando manipulação de strings binárias em Python.

2. Análise de Desempenho
  - Comparação entre a implementação manual e a biblioteca padrão crc.
  - Objetivo: Quantificar o custo computacional da abstração.
  - Métricas: Tempo de execução e pico de uso de memória para diferentes tamanhos de payload (MTU, Jumbo Frames, etc).
  - Comparativo: Abordagem bit-a-bit (Python puro) vs. Abordagem Table-Driven (Otimizada em C).

3. Investigação de Robustez
  - Testes de estresse para identificar as limitações do algoritmo.
  - Objetivo: Verificar a eficácia do CRC contra diferentes tipos de erros de transmissão.
  - Cenários:
      - Injeção de erros de rajada aleatórios.
      - Identificação de "Pontos Cegos" (colisões matemáticas onde erros propositais não são detectados).

Projeto desenvolvido para a disciplina de Redes de Computadores - UFCG.
