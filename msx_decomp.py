import sys
import os

def decompress_msx_vdp(rom_data):
    """
    Décompresse les données selon la logique du code Z80 MSX :
    - Bit 7 à 0 : RLE (Répétition)
    - Bit 7 à 1 : Littéral (Copie)
    - 0x00      : Fin de flux
    """
    pos = 0
    output = bytearray()
    
    while pos < len(rom_data):
        header = rom_data[pos]
        pos += 1
        
        # Marqueur de fin (RET Z)
        if header == 0:
            break
            
        count = header & 0x7F
        is_literal = (header & 0x80) != 0

        if is_literal:
            # --- MODE LITTÉRAL ---
            # On copie 'count' octets depuis la source
            for _ in range(count):
                if pos < len(rom_data):
                    output.append(rom_data[pos])
                    pos += 1
        else:
            # --- MODE RLE ---
            # On répète l'octet suivant 'count' fois
            if pos < len(rom_data):
                val = rom_data[pos]
                pos += 1
                for _ in range(count):
                    output.append(val)
                    
    return output

def main():
    if len(sys.argv) < 3:
        print("Usage: python msx_decomp.py <fichier_compresse> <fichier_sortie>")
        print("Exemple: python msx_decomp.py gfx_comp.bin gfx_raw.bin")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        if not os.path.exists(input_file):
            print(f"Erreur : Le fichier '{input_file}' n'existe pas.")
            return

        with open(input_file, "rb") as f:
            comp_data = f.read()
        
        raw_data = decompress_msx_vdp(comp_data)

        with open(output_file, "wb") as f:
            f.write(raw_data)

        print(f"Décompression réussie !")
        print(f"Taille compressée : {len(comp_data)} octets")
        print(f"Taille décompressée : {len(raw_data)} octets")
        
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

if __name__ == "__main__":
    main()