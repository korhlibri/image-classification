import sys
import time
import threading
from safesearch import detect_safe_search
from scraping import images_from_url

sys.stdout.reconfigure(encoding='utf-8')

def analyze_content(images_uris):

    total_likelihood = [0, 0, 0]
    potential_sensitive_content = [0, 0, 0]

    for uri in images_uris:

        # Call SafeSearch API to detect type of content
        likelihood = detect_safe_search(uri)

        for i in range(len(likelihood)):
            if likelihood[i] > .70:
                potential_sensitive_content[i] += 1

        # Sum all scores per type
        total_likelihood = [sum(i) for i in zip(likelihood, total_likelihood)]

    # Calculate the average score per type
    total_likelihood = [round((i/len(images_uris)), 2) for i in total_likelihood]

    done_event.set()

    return total_likelihood, potential_sensitive_content

def display_results(total_likelihood, potential_content):
    
    print("\n\n***************************")
    print("  RESULTADOS SAFE SEARCH    \n")
    print("  Probabilidades de contenido sensible en total:    \n")
    print(f"  Contenido Adulto:   {total_likelihood[0] * 100}%")
    print(f"  Contenido Médico:   {total_likelihood[1] * 100}%")
    print(f"  Contenido Violento: {total_likelihood[2] * 100}%\n")
    print(f"  Se encontraron:\n")
    print(f"  {potential_content[0]} imágenes con posible contenido adulto,")
    print(f"  {potential_content[1]} imágenes con posible contenido médico y")
    print(f"  {potential_content[2]} imágenes con posible contenido violento.")
    print("\n***************************")

import sys
import time

def animate_dots():
    sys.stdout.write('Analizando')
    while not done_event.is_set():
        time.sleep(.5)
        sys.stdout.write('.')
        sys.stdout.flush()

if __name__ == "__main__":
    images_uris = images_from_url("https://www.female-anatomy-for-artist.com/")

    done_event = threading.Event()
    animation_thread = threading.Thread(target=animate_dots)
    animation_thread.start()

    total_likelihood, potential_sensitive_content = analyze_content(images_uris)

    animation_thread.join()

    display_results(total_likelihood, potential_sensitive_content)