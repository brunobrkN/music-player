import pygame, os, random
import tkinter as tk
from tkinter import filedialog

class MusicPlayer:

    def __init__(self,root):

        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()
        pygame.mixer.init()

        self.root = root

        self.pasta = None

        self.musica_atual = None
        self.musicas_mp3 = []

        self.paused = False

        self.modo_aleatorio = False

        self._carregar_icones()
        self._carregar_tela()

        self.FIM_DA_MUSICA = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.FIM_DA_MUSICA)

        self.verificar_fim_da_musica()


    def _carregar_icones(self):
        self.icones = {
            "play" : tk.PhotoImage(file="play.png"),
            "pause" : tk.PhotoImage(file="pause.png"),
            "next" : tk.PhotoImage(file="next.png"),
            "previous" : tk.PhotoImage(file="previous.png"),
            "add" : tk.PhotoImage(file="add.png"),
            "shuffle_on" : tk.PhotoImage(file="shuffle_on.png"),
            "shuffle_off" : tk.PhotoImage(file="shuffle_off.png"),
        }

    def verificar_fim_da_musica(self):
        for event in pygame.event.get():
            if event.type == self.FIM_DA_MUSICA:
                self.proxima_musica()

        self.root.after(1000, self.verificar_fim_da_musica)


    def _carregar_tela(self):

        menu_bar = tk.Menu(root)
        self.root.config(menu=menu_bar)
        menu_principal = tk.Menu(menu_bar, tearoff=False)
        menu_principal.add_command(label="Selecionar pasta de músicas", command=self.selecionar_musicas)
        menu_bar.add_cascade(label='☰ Menu', compound='none', menu=menu_principal)

        self.lista_de_musicas = tk.Listbox(root, bg="black", fg="white", width=150, height=20)
        self.lista_de_musicas.pack()

        self.lista_de_musicas.bind("<Double-Button-1>", self.duplo_click)

        control_frame = tk.Frame(self.root)
        control_frame.pack()
        self.aleatorio_button = tk.Button(control_frame, image=self.icones["shuffle_off"], command=self.aleatorio,height=50, width=50)
        self.play_pause_button = tk.Button(control_frame, image=self.icones["play"], borderwidth=0, command=self.tocar_musica)
        self.next_button = tk.Button(control_frame, image=self.icones["next"], borderwidth=0, command=self.proxima_musica)
        self.previous_button = tk.Button(control_frame, image=self.icones["previous"], borderwidth=0, command=self.musica_anterior)
        self.play_pause_button.grid(row=0, column=1, padx=0, pady=10)
        self.next_button.grid(row=0, column=2, padx=0, pady=10)
        self.previous_button.grid(row=0, column=0, padx=0, pady=10)
        self.aleatorio_button.grid(row=0, column=3, padx=0, pady=10)


    def aleatorio(self):
        pass
        self.modo_aleatorio = not self.modo_aleatorio
        if self.modo_aleatorio:
            self.aleatorio_button.config(image=self.icones["shuffle_on"])
        else:
            self.aleatorio_button.config(image=self.icones["shuffle_off"])


    def duplo_click(self,event):
        pass
        index = self.lista_de_musicas.curselection()
        if index:
            self.lista_de_musicas.selection_clear(0, tk.END)
            self.musica_atual = self.lista_de_musicas.get(index)+'.mp3'
            self.lista_de_musicas.selection_set(self.musicas_mp3.index(self.musica_atual))
            self.carregar_musica()


    def selecionar_musicas(self):
        self.pasta = filedialog.askdirectory(title="Selecione uma Pasta")

        self.musicas_mp3 = [musica for musica in os.listdir(self.pasta) if musica.endswith('.mp3')]

        for musica in self.musicas_mp3:
            self.lista_de_musicas.insert("end", musica.replace(".mp3",''))

        self.lista_de_musicas.select_set(0)
        self.musica_atual = self.musicas_mp3[self.lista_de_musicas.curselection()[0]]

        self.carregar_musica()



    def carregar_musica(self):
        pygame.mixer.music.load(os.path.join(self.pasta, self.musica_atual))
        pygame.mixer.music.play()


    def tocar_musica(self):
        if self.pasta:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
                self.play_pause_button.config(image=self.icones["pause"])

            else:
                pygame.mixer.music.pause()
                self.play_pause_button.config(image=self.icones["play"])
                self.paused = True
        else:
            return


    def proxima_musica(self):
        if not self.modo_aleatorio:
            self.lista_de_musicas.selection_clear(0, tk.END)
            self.lista_de_musicas.selection_set(self.musicas_mp3.index(self.musica_atual) + 1)
            self.musica_atual = self.musicas_mp3[self.lista_de_musicas.curselection()[0]]
            self.carregar_musica()
        else:
            self.lista_de_musicas.selection_clear(0, tk.END)
            index = self.lista_de_musicas.curselection()
            musica_aleatoria = random.choice(self.musicas_mp3)
            self.lista_de_musicas.selection_set(self.musicas_mp3.index(musica_aleatoria))
            self.musica_atual = self.musicas_mp3[self.lista_de_musicas.curselection()[0]]
            self.carregar_musica()


    def musica_anterior(self):
        self.lista_de_musicas.selection_clear(0, tk.END)
        self.lista_de_musicas.selection_set(self.musicas_mp3.index(self.musica_atual))
        self.musica_atual = self.musicas_mp3[self.lista_de_musicas.curselection()[0]]
        self.carregar_musica()



def main():
    root.mainloop()
    try:
        pygame.mixer.init()

    except pygame.error:
        print("Não foi possível inicializar o player!")
        return


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Music Player")
    root.geometry("600x400")
    gerenciador = MusicPlayer(root)
    root.mainloop()


