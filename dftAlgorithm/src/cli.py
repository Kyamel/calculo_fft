import argparse
import ast
import os
import numpy as np
from plotter import Plotter

def read_signal_from_file(filename):
    name = None
    fs = None
    samples = []

    with open(filename, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()

        # Ignora linhas comentadas e vazias
        if not line or line.startswith('#'):
            continue

        # Nome do sinal
        if line.startswith('"') and line.endswith('"'):
            name = line.strip('"')

        # Frequência de amostragem
        elif line.isdigit():
            fs = int(line)
        
        # Amostras
        else:
            try:
                samples.extend(map(float, line.split(',')))
            except ValueError:
                print(f"Warning: Skipping invalid sample data '{line}'")

    if name is None or fs is None or not samples:
        raise ValueError("File format is incorrect or missing required data.")

    return name, fs, samples

def main():
    parser = argparse.ArgumentParser(description='Process a single signal from a text file.')
    parser.add_argument('filename', type=str, help='The path to the text file with signal data.')
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        print(f"Error: File {args.filename} does not exist.")
        return
    try:
        name, fs, samples = read_signal_from_file(args.filename)
    except ValueError as e:
        print(f"Error: {e}")
        return

    plotter = Plotter(samples, fs, name)
    plotter.calculate()

    main_loop: bool = True
    while main_loop:
        while True:
            action = input("Type 'd' to display, 's <filename>' to save, 'fr', 'fs' or 'fa' to remove, scale or add frequencies, or 'q' to quit: ").strip().lower()
            if action == 'd':
                plotter.plot()
                plotter.show()

            elif action.startswith('s'):
                filename = action[1:].strip()
                if not filename:
                    filename = ''
                plotter.plot()
                plotter.save(filename)

            elif action == 'fr':
                print(f"{'Freq (Hz)':<20} {'Mag':<20} {'Faze (°)':<20}")
                print("-" * 50)
                for freq, magnitude, fase in zip(plotter.normalized_frequencies, plotter.normalized_magnitudes, plotter.phase):
                    if magnitude > 1e-4:
                        print(f"{freq:<20.2f} {magnitude:<20.2f} {fase:<20.2f}")
                
                freqs_to_zero = input("Enter frequencies to zero out, separated by commas: ").strip()
                try:
                    if freqs_to_zero:
                        freqs_to_zero = list(map(float, freqs_to_zero.split(',')))
                        plotter.eliminate_frequencies(np.array(freqs_to_zero))
                        print(f"Frequencies {freqs_to_zero} removed. You can now 'show' or 'save' the plot.")
                except ValueError:
                    print("Error: Invalid frequency input.")

            elif action == 'fs':
                print(f"{'Freq (Hz)':<20} {'Mag':<20} {'Faze (°)':<20}")
                print("-" * 50)
                for freq, magnitude, fase in zip(plotter.normalized_frequencies, plotter.normalized_magnitudes, plotter.phase):
                    if magnitude > 1e-4:
                        print(f"{freq:<20.2f} {magnitude:<20.2f} {fase:<20.2f}")

                freqs_to_add = input("Enter frequencies to scale in the format (freq1, scale1), (freq2, scale2): ").strip()
                try:
                    if freqs_to_add:
                        # Use ast.literal_eval for safer parsing
                        freqs_to_add = ast.literal_eval(f"[{freqs_to_add}]")
                        if isinstance(freqs_to_add, list) and all(isinstance(item, tuple) and len(item) == 2 for item in freqs_to_add):
                            plotter.scale_frequencies(freqs_to_add)
                            print(f"Frequencies {freqs_to_add} scaled. You can now 'show' or 'save' the plot.")
                        else:
                            raise ValueError("Input is not in the correct format.")
                except (ValueError, SyntaxError):
                    print("Error: Invalid input. Please enter frequencies and magnitudes in the format (600, 20), (720, 30).")

            elif action == 'fa':
                print(f"{'Freq (Hz)':<20} {'Mag':<20} {'Faze (°)':<20}")
                print("-" * 50)
                for freq, magnitude, fase in zip(plotter.normalized_frequencies, plotter.normalized_magnitudes, plotter.phase):
                    if magnitude < 1e-4:
                        print(f"{freq:<20.2f} {magnitude:<20.2f} {fase:<20.2f}")

                freqs_to_add = input("Enter frequencies and magnitudes to add in the format (freq1, mag1), (freq2, mag2): ").strip()
                try:
                    if freqs_to_add:
                        # Use ast.literal_eval for safer parsing
                        freqs_to_add = ast.literal_eval(f"[{freqs_to_add}]")
                        if isinstance(freqs_to_add, list) and all(isinstance(item, tuple) and len(item) == 2 for item in freqs_to_add):
                            plotter.add_frequencies(freqs_to_add)
                            print(f"Frequencies {freqs_to_add} added. You can now 'show' or 'save' the plot.")
                        else:
                            raise ValueError("Input is not in the correct format.")
                except (ValueError, SyntaxError):
                    print("Error: Invalid input. Please enter frequencies and magnitudes in the format (600, 20), (720, 30).")

            elif action == 'q':
                main_loop = False
                break

            else:
                print("Invalid action. Type 'd' to display, 's <filename>' to save, 'fr' to remove frequencies, 'fs' to scale frequencies, or 'q' to quit.")

if __name__ == '__main__':
    main()