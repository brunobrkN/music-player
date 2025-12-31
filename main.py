import pygame, os, random
import tkinter as tk
from tkinter import filedialog

class MusicPlayer:

    def __init__(self):

        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()
        pygame.mixer.init()

        self.root = root

        self.pasta = None

        self.musica_atual = None
        self.musicas_mp3 = []
        self.ordem = []

        self.paused = False

        self.modo_aleatorio = False


        self._carregar_icones()
        self._carregar_tela()

        self.FIM_DA_MUSICA = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.FIM_DA_MUSICA)

        self._verificar_fim_da_musica()


    def _carregar_icones(self):
        """
        Carrega os icones do aplicativo.
        :return:
        """
        self.icones = {
            "play" : tk.PhotoImage(file="play.png"),
            "pause" : tk.PhotoImage(file="pause.png"),
            "next" : tk.PhotoImage(file="next.png"),
            "previous" : tk.PhotoImage(file="previous.png"),
            "add" : tk.PhotoImage(file="add.png"),
            "shuffle_on" : tk.PhotoImage(file="shuffle_on.png"),
            "shuffle_off" : tk.PhotoImage(file="shuffle_off.png"),
        }


    def _carregar_tela(self):

        menu_bar = tk.Menu(root)
        self.root.config(menu=menu_bar)
        menu_principal = tk.Menu(menu_bar, tearoff=False)
        menu_principal.add_command(label="Selecionar pasta de músicas", command=self.selecionar_musicas)
        menu_principal.add_command(label="Adicionar músicas")
        menu_bar.add_cascade(label='☰ Menu', compound='none', menu=menu_principal)

        self.lista_de_musicas = tk.Listbox(root,selectmode=tk.EXTENDED, bg="black", fg="white", width=150, height=20)
        self.lista_de_musicas.pack()

        self.lista_de_musicas.bind("<Double-Button-1>", self.duplo_click)

        control_frame = tk.Frame(self.root)
        control_frame.pack()
        self.aleatorio_button = tk.Button(control_frame, image=self.icones["shuffle_off"], command=self.aleatorio,height=50, width=50)
        self.play_pause_button = tk.Button(control_frame, image=self.icones["pause"], borderwidth=0, command=self.tocar_musica)
        self.next_button = tk.Button(control_frame, image=self.icones["next"], borderwidth=0, command=self.proxima_musica)
        self.previous_button = tk.Button(control_frame, image=self.icones["previous"], borderwidth=0, command=self.musica_anterior)
        self.play_pause_button.grid(row=0, column=1, padx=0, pady=10)
        self.next_button.grid(row=0, column=2, padx=0, pady=10)
        self.previous_button.grid(row=0, column=0, padx=0, pady=10)
        self.aleatorio_button.grid(row=0, column=3, padx=0, pady=10)

        self.lista_de_musicas.bind("<Button-3>", self.musicas_opcoes)

        self.menu_musicas = tk.Menu(root, tearoff=0)
        self.menu_musicas.add_command(label='Remover da playlist', command=self.remover_musicas)
        self.menu_musicas.add_command(label='Adicionar musicas')

    def _verificar_fim_da_musica(self):

        for event in pygame.event.get():
            if event.type == self.FIM_DA_MUSICA:
                self.proxima_musica()

        self.root.after(500, self._verificar_fim_da_musica)


    def aleatorio(self):
        """
        Alterna o estado do modo aleatório (toggle) e embaralha ou retorna a ordem de reprodução de acordo com
        o estado da variável self.modo_aleatorio.
        :return:
        """
        self.modo_aleatorio = not self.modo_aleatorio
        if self.modo_aleatorio:
            self.embaralhar()
            self.aleatorio_button.config(image=self.icones["shuffle_on"])

        else:
            self.ordem = self.musicas_mp3.copy()
            self.aleatorio_button.config(image=self.icones["shuffle_off"])


    def carregar_musica(self,):

        pygame.mixer.music.load(os.path.join(self.pasta, self.musicas_mp3[self.musica_atual]))
        pygame.mixer.music.play()

        self.lista_de_musicas.selection_clear(0, tk.END)
        self.lista_de_musicas.selection_set(self.musica_atual)
        self.lista_de_musicas.see(self.musica_atual)


    def duplo_click(self,event):
        """
        Pega o índice da música clicada e reproduz, alterando a ordem de reprodução para não repetir e adicionar
        no histórico.
        :param event:
        :return:
        """
        index_selecionado = self.lista_de_musicas.curselection()
        if index_selecionado:
            self.lista_de_musicas.selection_clear(0, tk.END)
            self.ordem.remove(index_selecionado[0])
            self.ordem[self.ordem.index(self.musica_atual)+1] = index_selecionado[0]
            self.musica_atual = index_selecionado[0]
            self.lista_de_musicas.selection_set(self.ordem.index(self.musica_atual))
            self.carregar_musica()


    def embaralhar(self):
        self.ordem = [indice for indice in range(len(self.musicas_mp3))]
        random.shuffle(self.ordem)
        self.musica_atual = self.ordem[0]


    def musica_anterior(self):

        try:
            self.lista_de_musicas.selection_clear(0, tk.END)
            self.lista_de_musicas.selection_set(self.ordem.index(self.musica_atual) - 1)
            self.musica_atual = self.ordem[self.lista_de_musicas.curselection()[0]]
            self.carregar_musica()

        except IndexError or ValueError:
            pass


    def musicas_opcoes(self, event):

        index_selecionado = self.lista_de_musicas.nearest(event.y)

        if index_selecionado not in self.lista_de_musicas.curselection():
            self.lista_de_musicas.selection_clear(0, tk.END)

            self.lista_de_musicas.selection_set(index_selecionado)
            self.lista_de_musicas.activate(index_selecionado)

        try:
            self.menu_musicas.tk_popup(event.x_root, event.y_root)

        finally:
            self.menu_musicas.grab_release()


    def proxima_musica(self):
        """
        Busca a próxima música através da lista de índices (self.ordem). Se identificado que é o fim da lista,
        retorna o indice para 0 e embaralha novamente  se o modo aleatório estiver ativo.
        :return:
        """

        if self.musica_atual == len(self.ordem)-1:
            if self.modo_aleatorio:
                self.embaralhar()
            else:
                self.musica_atual = 0

        else:
            self.musica_atual = self.ordem[self.ordem.index(self.musica_atual) + 1]
            self.carregar_musica()


    def remover_musicas(self):
        musicas = self.lista_de_musicas.curselection()

        for musica in reversed(musicas):
            self.musicas_mp3.pop(musica)
            self.ordem.pop(musica)
            self.lista_de_musicas.delete(musica)
        print(self.ordem)


    def selecionar_musicas(self):
        self.pasta = filedialog.askdirectory(title="Selecione uma Pasta")
        if self.pasta:
            self.musicas_mp3 = [musica for musica in os.listdir(self.pasta) if musica.endswith('.mp3')]
            for musica in self.musicas_mp3:
                self.lista_de_musicas.insert("end", musica.replace(".mp3",''))
            self.lista_de_musicas.select_set(0)
            self.musica_atual = 0
            self.ordem = [indice for indice in range(len(self.musicas_mp3))]
            self.carregar_musica()


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
    gerenciador = MusicPlayer()
    root.mainloop()
