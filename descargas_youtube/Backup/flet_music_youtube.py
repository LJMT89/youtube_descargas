import flet as ft
from pytube import YouTube
import os

def main (page):
    url = ft.TextField(label="URL", autofocus=True)
    submit = ft.ElevatedButton("Descarga")
    message = ft.Text("")

    def btn_click(e):
        current_folder = os.getcwd()
        yt = YouTube(url.value)
        audio = yt.streams.filter(only_audio=True).first()
        audio.download(output_path=current_folder)

        print=("Ola q ase")

        # Cambiar el texto del Label después de la descarga
        message.value = "La canción ha sido descargada."

        # Limpiar el contenido del TextField
        url.value = ""

    submit.on_click = btn_click
    page.add(
        url, 
        submit,
        message
    )

ft.app(target=main)