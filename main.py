import pygame
import random
import string

# Inicjalizacja Pygame
pygame.init()

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ekran
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wisielec")

# Czcionki
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# Funkcja do rysowania postaci
def draw_hangman(mistakes):
    # Głowa
    if mistakes >= 1:
        pygame.draw.circle(win, BLACK, (200, 150), 50, 3)
    # Ciało
    if mistakes >= 2:
        pygame.draw.line(win, BLACK, (200, 200), (200, 400), 3)
    # Ręce
    if mistakes >= 3:
        pygame.draw.line(win, BLACK, (200, 250), (100, 300), 3)
        pygame.draw.line(win, BLACK, (200, 250), (300, 300), 3)
    # Nogi
    if mistakes >= 4:
        pygame.draw.line(win, BLACK, (200, 400), (100, 500), 3)
        pygame.draw.line(win, BLACK, (200, 400), (300, 500), 3)
    # Oczy
    if mistakes >= 5:
        pygame.draw.circle(win, BLACK, (185, 135), 5)
        pygame.draw.circle(win, BLACK, (215, 135), 5)
    # Usta
    if mistakes >= 6:
        pygame.draw.arc(win, BLACK, (380, 140, 40, 20), 0, 3.14, 3)

# Funkcja do rysowania
def draw():
    win.fill(WHITE)
    
    # Tytuł
    title = TITLE_FONT.render("Wisielec", 1, BLACK)
    win.blit(title, (WIDTH/2 - title.get_width()/2, 10))
    
    # Wyświetlenie słowa
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    word_text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(word_text, (400, 200))
    
    draw_hangman(hangman_status)
    
    pygame.display.update()

# Ustawienia gry
hangman_status = 0
words = ["PYTHON", "PROGRAMOWANIE", "KOT", "PIES", "OPENAI", "GPT"]
word = random.choice(words)
guessed = []

# Litery alfabetu
letters = [letter for letter in string.ascii_uppercase]

# Główna pętla gry
FPS = 60
clock = pygame.time.Clock()
run = True
while run:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key in range(97, 123):  # ASCII dla liter od 'a' do 'z'
                letter = chr(event.key - 32)  # Zamiana na wielką literę
                if letter in letters:
                    guessed.append(letter)
                    letters.remove(letter)
                    if letter not in word:
                        hangman_status += 1
    
    draw()
    
    # Sprawdź wygraną
    won = all(letter in guessed for letter in word)
    
    # Sprawdź przegraną
    if hangman_status == 6:
        win.fill(WHITE)
        lost_text = WORD_FONT.render("Przegrałeś! Słowo to: " + word, 1, BLACK)
        win.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(3000)
        break
    
    # Wygrana
    if won:
        win.fill(WHITE)
        win_text = WORD_FONT.render("Wygrałeś!", 1, BLACK)
        win.blit(win_text, (WIDTH/2 - win_text.get_width()/2, HEIGHT/2 - win_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(3000)
        break

pygame.quit()