import webbrowser

def abrir_youtube_en_brave(url):
    try:
        # Ruta del ejecutable de Brave en tu sistema
        ruta_brave = "/usr/bin/brave-browser"  # Reemplaza con la ruta de tu ejecutable de Brave

        # Establecer el navegador predeterminado como Brave
        webbrowser.register('brave', None, webbrowser.BackgroundBrowser(ruta_brave))

        # Abrir la URL de YouTube en Brave
        webbrowser.get('brave').open_new(url)
    except Exception as e:
        print(f"Error al abrir YouTube en Brave: {str(e)}")

# URL de YouTube que deseas abrir en Brave
url_youtube = 'https://www.youtube.com/'

# Llamar a la función para abrir YouTube en Brave
abrir_youtube_en_brave(url_youtube)
