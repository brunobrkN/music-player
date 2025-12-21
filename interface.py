import os,pygame
import tkinter as tk
from tkinter import filedialog

class MusicPlayer:

    def __init__(self):
        self.root = root
        self.lista_de_musicas = lista_de_musicas
        self.pasta = None
        self.musica_atual = None
        self.paused = False
        self.musicas_mp3 = []
        self.play_pause_image= tk.PhotoImage(file="pause.png")


    def duplo_click(self,event):
        index = self.lista_de_musicas.curselection()
        if index:
            self.lista_de_musicas.selection_clear(0, tk.END)
            self.musica_atual = self.lista_de_musicas.get(index)+'.mp3'
            self.lista_de_musicas.selection_set(self.musicas_mp3.index(self.musica_atual))
            gerenciador.carregar_musica()


    def selecionar_musicas(self):
        self.pasta = filedialog.askdirectory(title="Selecione uma Pasta")

        self.musicas_mp3 = [musica for musica in os.listdir(self.pasta) if musica.endswith('.mp3')]

        for musica in self.musicas_mp3:
            self.lista_de_musicas.insert("end", musica.replace(".mp3",''))

        self.lista_de_musicas.select_set(0)
        self.musica_atual = self.musicas_mp3[lista_de_musicas.curselection()[0]]
        pygame.mixer.init()
        gerenciador.carregar_musica()


    def carregar_musica(self):
        pygame.mixer.music.load(os.path.join(self.pasta, self.musica_atual))
        pygame.mixer.music.play()


    def tocar_musica(self):
        if self.pasta:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
                self.play_pause_image = tk.PhotoImage(file='pause.png')
                play_pause_button.config(image=self.play_pause_image)

            else:
                pygame.mixer.music.pause()
                self.play_pause_image = tk.PhotoImage(file='play.png')
                play_pause_button.config(image=self.play_pause_image)
                self.paused = True

        else:
            return


    def proxima_musica(self):
        self.lista_de_musicas.selection_clear(0, tk.END)
        self.lista_de_musicas.selection_set(self.musicas_mp3.index(self.musica_atual) + 1)
        self.musica_atual = self.musicas_mp3[lista_de_musicas.curselection()[0]]
        gerenciador.carregar_musica()


    def musica_anterior(self):
        self.lista_de_musicas.selection_clear(0, tk.END)
        self.lista_de_musicas.selection_set(self.musicas_mp3.index(self.musica_atual) - 1)
        self.musica_atual = self.musicas_mp3[lista_de_musicas.curselection()[0]]
        print(self.musica_atual)
        gerenciador.carregar_musica()


root = tk.Tk()
root.title("Music Player")
root.geometry("600x400")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

lista_de_musicas = tk.Listbox(root,bg="black",fg="white",width=150,height=20)
lista_de_musicas.pack()


previous_button_img = tk.PhotoImage(file="previous.png")
next_button_img = tk.PhotoImage(file="next.png")
add_button_img = tk.PhotoImage(file="add.png")
options_button_img = tk.PhotoImage(file="options.png")

gerenciador = MusicPlayer()
menu_principal = tk.Menu(menu_bar, tearoff=False)
menu_principal.add_command(label="Selecionar pasta de músicas", command= gerenciador.selecionar_musicas)
menu_bar.add_cascade(label='☰ Menu', compound='none', menu=menu_principal)

lista_de_musicas.bind("<Double-Button-1>", gerenciador.duplo_click)

control_frame = tk.Frame(root)
control_frame.pack()

play_pause_button = tk.Button(control_frame, image=gerenciador.play_pause_image, borderwidth=0, command=gerenciador.tocar_musica)
next_button = tk.Button(control_frame, image=next_button_img, borderwidth=0, command=gerenciador.proxima_musica)
previous_button = tk.Button(control_frame, image=previous_button_img, borderwidth=0, command=gerenciador.musica_anterior)


play_pause_button.grid(row=0, column=2,padx=0, pady=10)
next_button.grid(row=0, column=3,padx=0, pady=10)
previous_button.grid(row=0, column=0,padx=0, pady=10)
