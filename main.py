import pygame
import interface

def main():
    interface.root.mainloop()
    try:
        pygame.mixer.init()
    except pygame.error:
        print("Não foi possível inicializar o player!")
        return

if __name__ == "__main__":
    main()
