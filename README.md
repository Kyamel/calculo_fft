# Projeto de Transformada Discreta de Fourier (DFT) e Transformada Discreta de Fourier Inversa (IDFT)

Este projeto implementa a Transformada Discreta de Fourier (DFT) e a Transformada Discreta de Fourier Inversa (IDFT) para análise de sinais amostrados. O objetivo é fornecer uma aplicação simples que carrega sinais amostrados de um arquivo de texto e realiza operações de DFT e IDFT.

## Requisitos

- Python 3.6 ou superior
- Bibliotecas Python:
  - `numpy`
  - `matplotlib` (opcional, para visualização)
  - `scipy` (opcional, para funções adicionais de FFT)

## Estrutura do Projeto

- `src/cli.py`: Script principal para interação com o usuário.
- `src/plotter.py`: Contém as funções para processamento e visualização dos sinais.
- `data/`: Diretório onde os arquivos de dados (TXT) são armazenados.
- `README.md`: Este arquivo.

## Formato do Arquivo de Dados

Os arquivos de dados devem estar no seguinte formato:
- name
- sample frequency
- sample_1
- sample_2
- sample_3
- sample_4
- ...

## Como Executar

1. **Clone o Repositório**

    ```sh
    git clone https://github.com/kyamel/calculo_dft.git
    cd calculo_dft

2.  **Configurar ambiente**

    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    pip install numpy matplotlib

3. **Executar**
    ```sh
    python src/cli.py signat.txt
