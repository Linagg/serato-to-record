import os
import xml.etree.ElementTree as ET

# Estructura del proyecto
PROJECT_DIR = "DJConverter"
SERATO_DIR = os.path.join(PROJECT_DIR, "data", "serato")
SUBCRATES_DIR = os.path.join(SERATO_DIR, "Subcrates")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "rekordbox.xml")

# Crear estructura de carpetas
def setup_directories():
    os.makedirs(SERATO_DIR, exist_ok=True)
    os.makedirs(SUBCRATES_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

# Función para leer archivos .crate
def read_crate_files():
    tracks = []
    for file in os.listdir(SUBCRATES_DIR):
        if file.endswith(".crate"):
            with open(os.path.join(SUBCRATES_DIR, file), "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                for line in lines:
                    if line.strip():  # Evita líneas vacías
                        tracks.append(line.strip())
    return tracks

# Función para generar un archivo rekordbox.xml
def generate_rekordbox_xml(tracks):
    if not tracks:
        print("No se encontraron pistas para convertir.")
        return
    
    root = ET.Element("DJ_PLAYLISTS", Version="1.0.0")
    collection = ET.SubElement(root, "COLLECTION")
    collection.set("Entries", str(len(tracks)))
    
    for i, filepath in enumerate(tracks, start=1):
        track = ET.SubElement(collection, "TRACK", 
                              TrackID=str(i),
                              Name=os.path.basename(filepath),
                              Location=f"file://localhost/{filepath.replace('\\', '/')}",
                              BPM="0.00",
                              Genre="Unknown")
    
    tree = ET.ElementTree(root)
    tree.write(OUTPUT_FILE)
    print(f"Archivo {OUTPUT_FILE} generado con éxito.")

# Ejecutar el proceso
if __name__ == "__main__":
    setup_directories()
    tracks = read_crate_files()
    generate_rekordbox_xml(tracks)
