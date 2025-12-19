import os
import tkinter as tk
from tkinter import filedialog


def carregar_musicas():

    global musica_atual

    pasta = filedialog.askdirectory(title="Selecione uma Pasta")

    if pasta:

        musicas_mp3 = [musica for musica in os.listdir(pasta) if musica.endswith('.mp3')]
        for musica in musicas_mp3:
            lista_de_musicas.insert("end", musica)

        lista_de_musicas.select_set(0)
        musica_atual = lista_de_musicas.curselection()[0]

    else:
        print("Escolha uma pasta para listar suas músicas.")
        musicas_mp3 = []

    return musicas_mp3


root = tk.Tk()
root.title("Music Player")
root.geometry("600x400")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

lista_de_musicas = tk.Listbox(root,bg="black",fg="white",width=150,height=20)
lista_de_musicas.pack()

play_button_img = tk.PhotoImage(file="play.png")
pause_button_img = tk.PhotoImage(file="pause.png")
previous_button_img = tk.PhotoImage(file="previous.png")
next_button_img = tk.PhotoImage(file="next.png")
add_button_img = tk.PhotoImage(file="add.png")
options_button_img = tk.PhotoImage(file="options.png")

menu_principal = tk.Menu(menu_bar, tearoff=False)
menu_principal.add_command(label="Selecionar pasta de músicas", command=carregar_musicas)
menu_bar.add_cascade(label='☰ Menu', compound='none', menu=menu_principal)

control_frame = tk.Frame(root)
control_frame.pack()

play_button = tk.Button(control_frame, image=play_button_img, borderwidth=0)
pause_button = tk.Button(control_frame, image=pause_button_img, borderwidth=0)
previous_button = tk.Button(control_frame, image=previous_button_img, borderwidth=0)
next_button = tk.Button(control_frame, image=next_button_img, borderwidth=0)

play_button.grid(row=0, column=2,padx=0, pady=10)
pause_button.grid(row=0, column=1,padx=0, pady=10)
next_button.grid(row=0, column=3,padx=0, pady=10)
previous_button.grid(row=0, column=0,padx=0, pady=10)
