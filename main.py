from icrawler.builtin import GoogleImageCrawler
import random
import os

# --- Constantes (para mejorar la legibilidad y mantenibilidad) ---
ADJECTIVES_FILE = "english-adjectives.txt"
BASE_SEARCH_TERM = "mapache"

# --- Funciones ---

def get_valid_integer_input(prompt):
    """Solicita una entrada de número entero positivo al usuario y la valida."""
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Por favor, introduce un número positivo.")
        except ValueError:
            print("Entrada inválida. Por favor, introduce un número entero.")

def get_download_location_input():
    """Solicita la ubicación de descarga y asegura que el directorio exista."""
    while True:
        download_location = input("Ubicación de descarga (usa \"/\"): ")
        if os.path.isabs(download_location) or download_location.startswith('./') or download_location.startswith('../'): # Verifica si es una ruta absoluta o relativa válida
            break
        else:
            print("Ruta inválida. Por favor, usa '/' como separador y asegúrate de que sea una ruta absoluta o relativa válida (ej: C:/Fotos/Mapaches o ./descargas).")

    # Asegurarse de que la ubicación de descarga exista
    if not os.path.exists(download_location):
        try:
            os.makedirs(download_location)
            print(f"Directorio creado: {download_location}")
        except OSError as e:
            print(f"Error al crear el directorio '{download_location}': {e}")
            exit()
    return download_location

def confirm_download(num_raccoons, location):
    """Pide confirmación al usuario antes de proceder con la descarga."""
    print(f"\nVas a descargar {num_raccoons} imágenes de mapaches en '{location}'.")
    confirm = input("¿Estás seguro de que quieres continuar? (s/n): ").lower()
    if confirm != 's':
        print("Descarga cancelada.")
        exit()

def load_adjectives(script_dir):
    """Carga los adjetivos desde el archivo especificado."""
    file_path = os.path.join(script_dir, ADJECTIVES_FILE)
    keywords = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                keywords.append(line.strip())
    except FileNotFoundError:
        print(f"Error: El archivo de adjetivos '{ADJECTIVES_FILE}' no fue encontrado en '{script_dir}'.")
        print(f"Asegúrate de que '{ADJECTIVES_FILE}' esté en el mismo directorio que 'main.py'.")
        exit()
    return keywords

def get_search_term(keywords):
    """Construye el término de búsqueda usando un adjetivo aleatorio."""
    chosen_word = keywords[random.randint(0, len(keywords) - 1)]
    return f"{BASE_SEARCH_TERM} {chosen_word}"

def perform_download(num_of_raccoons, download_location, search_term):
    """Realiza la descarga de imágenes usando GoogleImageCrawler."""
    google_crawler = GoogleImageCrawler(storage={'root_dir': download_location})
    try:
        print(f"\nIniciando la descarga de {num_of_raccoons} imágenes de '{search_term}'...")
        google_crawler.crawl(filters={'type': "photo"}, keyword=search_term, max_num=num_of_raccoons)
        print(f"\nDescarga completa. Se descargaron {num_of_raccoons} imágenes de '{search_term}' en: {download_location}")
    except Exception as e:
        print(f"\nOcurrió un error durante la descarga: {e}")
        print("Por favor, verifica tu conexión a internet o que la ruta de descarga sea válida y tengas permisos de escritura.")

def main():
    """Función principal del programa."""
    num_of_raccoons = get_valid_integer_input("¿Cuántos mapaches te gustaría descargar?: ")
    download_location = get_download_location_input()

    confirm_download(num_of_raccoons, download_location)

    script_dir = os.path.dirname(__file__)
    keywords = load_adjectives(script_dir)
    search_term = get_search_term(keywords)

    perform_download(num_of_raccoons, download_location, search_term)

if __name__ == "__main__":
    main()