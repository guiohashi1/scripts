import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from threading import Thread
import instaloader

# Função para baixar o vídeo do Instagram
def download_video(url, output_dir):
    try:
        # Verificar se o URL fornecido é um URL válido do Instagram
        if not url.startswith("https://www.instagram.com/"):
            raise ValueError("URL inválido. Certifique-se de que é um URL do Instagram.")
        
        loader = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
        
        if post.typename == 'GraphVideo':
            loader.download_post(post, target=output_dir)
            messagebox.showinfo("Download Concluído", "O vídeo foi baixado com sucesso!")
        else:
            messagebox.showerror("Erro", "O link fornecido não corresponde a um vídeo do Instagram.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante o download: {e}")

# Classe da GUI
class InstagramVideoDownloader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Instagram Video Downloader")
        self.geometry("400x200")

        self.output_dir = tk.StringVar()
        self.output_dir.set(self.load_last_output_dir())

        # Campo de entrada para o URL do vídeo
        self.url_entry = tk.Entry(self, width=50)
        self.url_entry.grid(row=0, column=0, padx=10, pady=10)

        # Botão para escolher a pasta destino
        self.select_output_button = tk.Button(self, text="Escolher Pasta", command=self.select_output_directory)
        self.select_output_button.grid(row=1, column=0, padx=10, pady=5)

        # Botão para iniciar o download
        self.download_button = tk.Button(self, text="Baixar Vídeo", command=self.start_download)
        self.download_button.grid(row=2, column=0, padx=10, pady=5)

        # Barra de progresso
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.grid(row=3, column=0, padx=10, pady=5)

    # Função para selecionar a pasta destino
    def select_output_directory(self):
        output_dir = filedialog.askdirectory()
        self.output_dir.set(output_dir)
        self.save_last_output_dir(output_dir)

    # Função para iniciar o download em uma nova thread
    def start_download(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Erro", "Por favor, insira um URL válido.")
            return
        output_dir = self.output_dir.get()
        thread = Thread(target=download_video, args=(url, output_dir))
        thread.start()

    # Funções para salvar e carregar a pasta destino da última sessão
    def save_last_output_dir(self, output_dir):
        with open("last_output_dir_instagram.txt", "w") as f:
            f.write(output_dir)

    def load_last_output_dir(self):
        if os.path.exists("last_output_dir_instagram.txt"):
            with open("last_output_dir_instagram.txt", "r") as f:
                return f.read().strip()
        return ""

if __name__ == "__main__":
    app = InstagramVideoDownloader()
    app.mainloop()
