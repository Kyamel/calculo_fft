# DFT and IDFT Calculation Project

## Language Selection

Please select your language:
- [English](#dft-and-idft-calculation-project)
- [Português](#projeto-de-transformada-discreta-de-fourier-dft-e-transformada-discreta-de-fourier-inversa-idft)

---

## DFT and IDFT Calculation Project

This project implements the Discrete Fourier Transform (DFT) and the Inverse Discrete Fourier Transform (IDFT) for sampled signal analysis. The goal is to provide a simple application that loads sampled signals from a text file and performs DFT and IDFT operations.

### Requirements

- Python 3.6 or higher
- Python Libraries:
  - `numpy`
  - `matplotlib` (for graph visualization)


### Project Structure

- `src/cli.py`: Main script for user interaction.
- `src/plotter.py`: Contains functions for processing and visualizing signals.
- `data/`: Directory where data files (TXT) are stored.
- `README.md`: This file.

### Data File Format

The data files should be in the following format:
- name
- sample frequency
- sample_1
- sample_2
- sample_3
- sample_4
- ...

### How to Run

1. **Clone the Repository**

    ```sh
    git clone https://github.com/kyamel/calculo_dft.git
    cd calculo_dft
    ```

2. **Set Up Environment**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install numpy matplotlib
    ```

3. **Run**

    ```sh
    python src/cli.py signal.txt
    ```

---

## Projeto de Transformada Discreta de Fourier (DFT) e Transformada Discreta de Fourier Inversa (IDFT)

Este projeto implementa a Transformada Discreta de Fourier (DFT) e a Transformada Discreta de Fourier Inversa (IDFT) para análise de sinais amostrados. O objetivo é fornecer uma aplicação simples que carrega sinais amostrados de um arquivo de texto e realiza operações de DFT e IDFT.

### Requisitos

- Python 3.6 ou superior
- Bibliotecas Python:
  - `numpy`
  - `matplotlib` (para visualização gráfica)

### Estrutura do Projeto

- `src/cli.py`: Script principal para interação com o usuário.
- `src/plotter.py`: Contém as funções para processamento e visualização dos sinais.
- `data/`: Diretório onde os arquivos de dados (TXT) são armazenados.
- `README.md`: Este arquivo.

### Formato do Arquivo de Dados

Os arquivos de dados devem estar no seguinte formato:
- nome
- frequência de amostragem
- amostra_1
- amostra_2
- amostra_3
- amostra_4
- ...

### Como Executar

1. **Clone o Repositório**

    ```sh
    git clone https://github.com/kyamel/calculo_dft.git
    cd calculo_dft
    ```

2. **Configurar ambiente**

    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    pip install numpy matplotlib
    ```

3. **Executar**

    ```sh
    python src/cli.py signal.txt
    ```

---

**Note:** To switch between languages, simply scroll to the desired section above.
