from typing import List, Tuple
from matplotlib import pyplot as plt
import numpy as np

def dft(x: np.array, n: int, log: bool = False) -> Tuple[np.array, np.array]:
    real_result = np.empty(n)
    imag_result = np.empty(n)

    for i in range(n):
        real_sum = 0
        imag_sum = 0
        if log: print(f"X({i}) = ", end="")
        for k, v in enumerate(x):  # k é o índice atual e v é o valor correspondente em X
            imag = v * np.sin(2 * np.pi * i * k / n)
            real = v * np.cos(2 * np.pi * i * k / n)
            real_sum += real
            imag_sum += imag
            if log: print(f"{v} * [cos(2*pi*{i}*{k}/{n}) + sin(2*pi*{i}*{k}/{n})]\n", end=" + ")

        real_sum = round(real_sum, 4)
        imag_sum = round(imag_sum, 4)
        if log: print(f"\n= {real_sum} + {imag_sum}j\n")

        real_result[i] = real_sum
        imag_result[i] = imag_sum

    return (real_result, imag_result)

def idft(real_result: np.array, imag_result: np.array, n: int, log: bool = False) -> np.array:
    real_econstructed = np.empty(n)
    imag_reconstructed = np.empty(n)

    for k in range(n):
        real_sum = 0
        imag_sum = 0
        if log: print(f"x({k}) = ", end="")
        for i in range(n):
            real = real_result[i] * np.cos(2 * np.pi * i * k / n) + imag_result[i] * np.sin(2 * np.pi * i * k / n)
            imag = imag_result[i] * np.cos(2 * np.pi * i * k / n) - real_result[i] * np.sin(2 * np.pi * i * k / n)
            real_sum += real
            imag_sum += imag
            if log: print(f"({real_result[i]} + {imag_result[i]}j) * [cos(2*pi*{i}*{k}/{n}) - sin(2*pi*{i}*{k}/{n})]\n", end=" + ")
        real_sum = round(real_sum / n, 4)
        imag_sum = round(imag_sum / n, 4)
        if log: print(f"\n= {real_sum} + {imag_sum}j\n")

        real_econstructed[k] = real_sum
        imag_reconstructed[k] = imag_sum

    return real_econstructed

def normalizer(reals: np.array, imags: np.array, n: int) -> Tuple[np.array, np.array]:
    half_n = n // 2  # N/2 para a Lei de Nyquist

    normalized_real = np.array([real / half_n for real in reals[:half_n + 1]])
    normalized_imag = np.array([imag / half_n for imag in imags[:half_n + 1]])

    return (normalized_real, normalized_imag)


class Plotter:
    def __init__(self, sampled_signal: np.array, sample_rate: float, name = 'signal') -> None:
        self.name = name
        self.sampled_signal = sampled_signal
        self.N = len(sampled_signal)
        self.frequencies = np.arange(self.N)
        self.fs = sample_rate
        self.normalized_frequencies = np.array([(sample_rate * k) / self.N for k in range(int(self.N/2 + 1))])
        self.time = np.linspace(0, self.N/self.fs, self.N, endpoint=True)


    def _dft(self, log: bool = False) -> None:
        self.signal_on_freq_domain = dft(self.sampled_signal, self.N, log)
        self.normalized_signal = normalizer(self.signal_on_freq_domain[0], self.signal_on_freq_domain[1], self.N)

        self.magnitudes = np.sqrt(np.array(self.signal_on_freq_domain[0])**2 + np.array(self.signal_on_freq_domain[1])**2)
        self.normalized_magnitudes = np.sqrt(np.array(self.normalized_signal[0])**2 + np.array(self.normalized_signal[1])**2)

        self.faze = np.arctan2(self.normalized_signal[1], self.normalized_signal[0]) + np.pi / 2
        self.faze = np.where(abs(self.normalized_signal[0]) > 1e-4, self.faze, 0)

    def _idft(self, log: bool = False) -> None:
        real_part = self.normalized_signal[0]
        imag_part = self.normalized_signal[1]

        half_n = self.N // 2

        real_symmetric = np.concatenate([real_part, real_part[1:half_n][::-1]]) * half_n
        imag_symmetric = np.concatenate([imag_part, -imag_part[1:half_n][::-1]]) * half_n

        self.signal_reconstructed = idft(real_symmetric, imag_symmetric, self.N, log)

    def calculate(self, log: bool = False) -> None:
        self._dft(log)
        self._idft(log)

    def eliminate_frequencies(self, freq_to_zero: np.array):
        if self.signal_on_freq_domain is None or self.normalized_signal is None:
            raise ValueError("DFT not calculated. Please run dft() first.")

        indices_to_zero = []
        for freq in freq_to_zero:
            idx = np.argmin(np.abs(self.normalized_frequencies - freq))
            indices_to_zero.append(idx)

        for idx in indices_to_zero:
            self.normalized_signal[0][idx] = 0
            self.normalized_signal[1][idx] = 0

            self.signal_on_freq_domain[0][idx] = 0
            self.signal_on_freq_domain[1][idx] = 0
            if idx != len(self.normalized_frequencies) - 1:
                self.signal_on_freq_domain[0][-idx] = 0
                self.signal_on_freq_domain[1][-idx] = 0

        self.update()

    def add_frequencies(self, freq_to_add: List[Tuple[float, float]]):
        if self.signal_on_freq_domain is None or self.normalized_signal is None:
            raise ValueError("DFT not calculated. Please run dft() first.")

        indices_to_update = []
        for freq, value in freq_to_add:
            idx = np.argmin(np.abs(self.normalized_frequencies - freq))
            indices_to_update.append((idx, value))

        for idx, value in indices_to_update:
            self.normalized_signal[0][idx] = value
            self.normalized_signal[1][idx] = 0

            self.signal_on_freq_domain[0][idx] = value
            self.signal_on_freq_domain[1][idx] = 0
            if idx != len(self.normalized_frequencies) - 1:
                self.signal_on_freq_domain[0][-idx] = value
                self.signal_on_freq_domain[1][-idx] = 0

        self.update()

    def scale_frequencies(self, freq_to_scale: List[Tuple[float, float]]):
        if self.signal_on_freq_domain is None or self.normalized_signal is None:
            raise ValueError("DFT not calculated. Please run dft() first.")

        for freq, scale_factor in freq_to_scale:
            idx = np.argmin(np.abs(self.normalized_frequencies - freq))
            if idx == len(self.normalized_frequencies) - 1:
                # Handling the last index if it's not an exact match (like zero frequency)
                continue

            # Scale the real and imaginary parts
            self.normalized_signal[0][idx] *= scale_factor
            self.normalized_signal[1][idx] *= scale_factor

            self.signal_on_freq_domain[0][idx] *= scale_factor
            self.signal_on_freq_domain[1][idx] *= scale_factor

            # Apply the same scale factor to the conjugate part for negative frequencies
            self.signal_on_freq_domain[0][-idx] *= scale_factor
            self.signal_on_freq_domain[1][-idx] *= scale_factor

        self.update()

    def update(self) -> None:
        if self.normalized_signal is None:
            raise ValueError("DFT not calculated. Please run dft() first.")

        # Atualizar magnitudes
        self.magnitudes = np.sqrt(self.signal_on_freq_domain[0]**2 + self.signal_on_freq_domain[1]**2)
        self.normalized_magnitudes = np.sqrt(self.normalized_signal[0]**2 + self.normalized_signal[1]**2)

        # Atualizar fases
        self.faze = np.arctan2(self.normalized_signal[1], self.normalized_signal[0]) + np.pi / 2
        self.faze = np.where(np.abs(self.normalized_signal[0]) > 1e-4, self.faze, 0)

        # Atualizar sinal reconstruído
        self._idft()

    def plot(self) -> None:

        self.fig = plt.figure(figsize=(12, 8))

        plt.subplot(2, 2, 1)
        plt.stem(self.frequencies, self.magnitudes, basefmt=" ")
        plt.xlabel('Frequência')
        plt.ylabel('Magnitude')
        plt.title('Magnitude pela Frequência (DFT)')
        plt.grid(True)

        plt.subplot(2, 2, 2)
        plt.stem(self.normalized_frequencies, self.normalized_magnitudes, basefmt=" ")
        plt.xlabel('Frequência (Hz)')
        plt.ylabel('Magnitude')
        plt.title('Magnitude Normalizada pela Frequência (DFT)')
        plt.grid(True)

        plt.subplot(2, 2, 3)
        plt.stem(self.normalized_frequencies, self.faze * 180 / np.pi , basefmt=" ")
        plt.xlabel('Frequência (Hz)')
        plt.ylabel('Ãngulo (graus)')
        plt.title('Fase pela Frequência (DFT)')
        plt.grid(True)

        plt.subplot(2, 2, 4)
        plt.plot(self.time, self.signal_reconstructed)
        plt.xlabel('Tempo (s)')
        plt.ylabel('Função Reconstruída')
        plt.title('Função Reconstruída (IDFT) - Linhas')
        plt.grid(True)

        # Ajustar o layout para evitar sobreposição
        plt.tight_layout()

    def show(self) -> None:
        if hasattr(self, 'fig'):
            plt.show()
        else:
            print("No figure was created. Execute plot() before showing.")

    def save(self, filename: str = '') -> None:
        if hasattr(self, 'fig'):
            if not filename:
                filename = self.name + '.png'

            if not filename.lower().endswith('.png'):
                filename += '.png'

            self.fig.savefig(filename)
            print(f"Saved as: {filename}")
        else:
            print("No figure was created. Execute plot() before saving.")

    def __del__(self) -> None:
        if hasattr(self, 'fig'):
            plt.close(self.fig)
