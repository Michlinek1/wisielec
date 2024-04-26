import pygame
import random
import string

# Pygame initialization
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen dimensions
WIDTH, HEIGHT = 1200, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wisielec")

# Fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)
WORD_LABEL_FONT = pygame.font.SysFont('comicsans', 11)

# Reset button
res_label = WORD_FONT.render("Reset", False, (200, 200, 200))
label_res_rect = res_label.get_rect(topleft=(510, 350))

# Button parameters
button_x, button_y = 50, 50
button_width, button_height = 200, 50
button_color = (100, 100, 100)
button_text = "Dodaj swoje słowo"

guessed = []
word = ""

# Function to draw hangman
def draw_hangman(mistakes):
    if mistakes >= 1:
        pygame.draw.circle(win, BLACK, (200, 150), 50, 3)
    if mistakes >= 2:
        pygame.draw.line(win, BLACK, (200, 200), (200, 400), 3)
    if mistakes >= 3:
        pygame.draw.line(win, BLACK, (200, 250), (100, 300), 3)
        pygame.draw.line(win, BLACK, (200, 250), (300, 300), 3)
    if mistakes >= 4:
        pygame.draw.line(win, BLACK, (200, 400), (100, 500), 3)
        pygame.draw.line(win, BLACK, (200, 400), (300, 500), 3)
    if mistakes >= 5:
        pygame.draw.circle(win, BLACK, (185, 135), 5)
        pygame.draw.circle(win, BLACK, (215, 135), 5)
    if mistakes >= 6:
        pygame.draw.arc(win, BLACK, (380, 140, 40, 20), 0, 3.14, 3)

# Function to draw
def draw():
    win.fill(WHITE)
    
    # Title
    title = TITLE_FONT.render("Wisielec", 1, BLACK)
    win.blit(title, (WIDTH/2 - title.get_width()/2, 10))
    
    # Draw button
    pygame.draw.rect(win, button_color, (button_x, button_y, button_width, button_height))
    text = WORD_LABEL_FONT.render(button_text, True, BLACK)
    text_rect = text.get_rect(center=(button_x + button_width / 2, button_y + button_height / 2))
    win.blit(text, text_rect)
    
    # Display word
    display_x, display_y = 600, 200
    for letter in word:
        if letter in guessed:
            text = WORD_FONT.render(letter, 1, BLACK)
            win.blit(text, (display_x, display_y))
        else:
            text = WORD_FONT.render("_", 1, BLACK)
            win.blit(text, (display_x, display_y))
        display_x += 70
    
    draw_hangman(hangman_status)
    
    # Draw reset button if game is over
    if gameplay == False:
        pygame.draw.rect(win, button_color, (510, 350, 180, 50))
        text = WORD_LABEL_FONT.render("Zagraj ponownie", True, BLACK)
        text_rect = text.get_rect(center=(510 + 180 / 2, 350 + 50 / 2))
        win.blit(text, text_rect)
    
    pygame.display.update()

# Function to add word
def add_word():
    global word
    input_box = pygame.Rect(200, 200, 400, 50)
    text = ''
    typing = True

    while typing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    with open("hasla.txt", "a") as file:
                        file.write(text.upper() + '\n')
                    word = text.upper()
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        win.fill(WHITE)
        pygame.draw.rect(win, BLACK, input_box, 2)

        font = pygame.font.Font(None, 32)
        input_text = font.render(text, True, BLACK)
        win.blit(input_text, (input_box.x + 5, input_box.y + 5))

        pygame.display.update()

# Load words from file
words = []
with open("hasla.txt", "r") as file:
    for line in file:
        words.extend(line.strip().split(','))
if not words: 
    add_word()

# Main loop
FPS = 60
clock = pygame.time.Clock()
hangman_status = 0
run = True
gameplay = True

while run:
    clock.tick(FPS)

    if gameplay:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key in range(97, 123):
                    letter = chr(event.key - 32)
                    if letter not in guessed:
                        guessed.append(letter)
                        if letter not in word:
                            hangman_status += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_x <= mouse_pos[0] <= button_x + button_width and \
                   button_y <= mouse_pos[1] <= button_y + button_height:
                       add_word()

            draw()

            # Check win/loss conditions
            won = all(letter in guessed for letter in word)
            if hangman_status == 6:
                win.fill(WHITE)
                lost_text = WORD_FONT.render("Przegrałeś! Słowo to: " + word, 1, BLACK)
                win.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
                pygame.display.update()
                gameplay = False
            if won:
                gameplay = False
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if label_res_rect.collidepoint(event.pos):
                    gameplay = True
                    hangman_status = 0
                    word = random.choice(words)
                    guessed = []
                    break

pygame.quit()
