import re

def clean_text(text):
    """Corrige los espacios en los metadatos eliminando separaciones innecesarias."""
    text = re.sub(r'\s+', ' ', text).strip()  # Eliminar espacios repetidos
    text = re.sub(r'(?<=\b[A-Za-z]) (?=[A-Za-z]\b)', '', text)  # Unir letras separadas
    text = re.sub(r'(?<=\d) (?=\d)', '', text)  # Unir números separados incorrectamente
    return text

def extract_metadata(text):
    metadata = []
    
    # Buscar posibles metadatos clave
    tracks = re.findall(r'tsng\s+([^t]+)tlen\s+([^t]+)tsiz\s+([^t]+) Btbit\s+([^t]+) stsmp\s+([^t]+) ktbpm\s+([^t]+)tadd\s+([^t]+)tkey\s+([A-G#b]+)', text)
    
    for track in tracks:
        metadata.append({
            "Title": clean_text(track[0].replace('_', ' ')),
            "Duration": clean_text(track[1]),
            "Size (MB)": clean_text(track[2]),
            "Bitrate (kbps)": clean_text(track[3]),
            "Sample Rate (kHz)": clean_text(track[4]),
            "BPM": clean_text(track[5]),
            "Added Timestamp": clean_text(track[6]),
            "Key": clean_text(track[7])
        })
    
    return metadata

def read_serato_database(file_path):
    with open(file_path, "rb") as file:
        data = file.read()
    
    readable_text = "".join(chr(c) if 32 <= c < 127 or c in (10, 13) else " " for c in data)
    readable_text = re.sub(r'\s+', ' ', readable_text)  # Limpiar espacios extras
    
    metadata = extract_metadata(readable_text)
    
    if metadata:
        for track in metadata:
            print("------------------------------------")
            for key, value in track.items():
                print(f"{key}: {value}")
    else:
        print("No metadata extracted.")

if __name__ == "__main__":
    file_path = "C:/Users/Ilandaluce/Desarrollos/Python/Personal/serato-to-record/DJConverter/data/serato/database V2"  # Reemplázalo con la ruta correcta si es necesario
    read_serato_database(file_path)

