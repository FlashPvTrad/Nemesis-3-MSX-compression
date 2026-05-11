import sys
import os

def compress_msx_vdp(data):
    compressed = bytearray()
    i = 0
    size = len(data)

    while i < size:
        # 1. Tentative RLE (Répétition)
        run_len = 1
        while i + run_len < size and data[i] == data[i + run_len] and run_len < 127:
            run_len += 1

        if run_len >= 3:
            compressed.append(run_len) # Bit 7 est à 0
            compressed.append(data[i])
            i += run_len
        else:
            # 2. Tentative Littéral (Copie)
            lit_bytes = []
            while i < size and len(lit_bytes) < 127:
                if i + 2 < size and data[i] == data[i+1] == data[i+2]:
                    break
                lit_bytes.append(data[i])
                i += 1
            if lit_bytes:
                compressed.append(0x80 | len(lit_bytes)) # Bit 7 est à 1
                compressed.extend(lit_bytes)

    compressed.append(0x00) # Fin
    return compressed

def main():
    if len(sys.argv) < 3:
        print("Usage: python msx_comp.py <fichier_entree> <fichier_sortie>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(input_file, "rb") as f:
            raw_data = f.read()
        
        comp_data = compress_msx_vdp(raw_data)

        with open(output_file, "wb") as f:
            f.write(comp_data)

        print(f"Succès !")
        print(f"Taille originale : {len(raw_data)} octets")
        print(f"Taille compressée : {len(comp_data)} octets")
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    main()