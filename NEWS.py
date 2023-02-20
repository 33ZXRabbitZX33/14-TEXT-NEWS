import pygame,sys
import pygame.locals as pl
import requests
import datetime
from bs4 import BeautifulSoup

pygame.init()

size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
rate = 0.9
size = (size[0]*rate,size[1]*rate)

DISPLAYSURF = pygame.display.set_mode(size)
pygame.display.set_caption("Text_Web")
FPS = 60
fpsClock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BROWN = (207, 194, 157)
color_backg = BLACK

COLOR_INACTIVE = WHITE
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

global Err
Err = False
class Text():
    def __init__(self):
        pass
    def crawl(self,url):
        global Err
        try:
            tex = ""
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                if "Our Standards:" in p.text:
                    break
                elif "View 2 more stories" in p.text:
                    continue
                elif "[" and "]" in p.text:
                    continue
                else:
                    tex += p.text + '\n'
                    print(p.text)
            return tex
        except:
            Err = True
            print("Err")

Te = Text()
class InputBox():
    def __init__(self, x, y,blockx,blocky, text=''):
        self.rect = pygame.Rect(x, y, blockx, blocky)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.size = self.txt_surface.get_size()
    def handle_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False

            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                   pass             
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_v and pygame.key.get_mods() & pl.KMOD_CTRL:
                    # Handle pasting text from the clipboard
                    pygame.scrap.init()
                    clipboard_text = pygame.scrap.get(pl.SCRAP_TEXT)
                    if clipboard_text is not None:
                        clipboard_text = clipboard_text.replace(b'\x00', b'')
                        self.text += clipboard_text.decode('utf-8')
                elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Copy text to clipboard
                    pygame.scrap.init()
                    pygame.scrap.put(pygame.SCRAP_TEXT, self.text.encode('utf-8'))
                else:
                    self.text += event.unicode

                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
                self.size = self.txt_surface.get_size()
    def draw(self):
        try:
            margin = 14
            words = self.text.split()
            space_width, _ = FONT.size(' ')

            x, y = self.rect.x+margin,self.rect.y+margin
            max_width = self.rect.width-2*margin

            line = ""
            for word in words:
                if line == "":
                    line = word
                else:
                    new_line = f"{line} {word}"
                    width, _ = FONT.size(new_line)
                    if width < max_width:
                        line = new_line
                    else:
                        txt_surface = FONT.render(line, True, COLOR_ACTIVE)
                        size = txt_surface.get_size()
                        DISPLAYSURF.blit(txt_surface, (x, y))
                        y += size[1] + space_width
                        line = word

            if line != "":
                txt_surface = FONT.render(line, True, COLOR_ACTIVE)
                size = txt_surface.get_size()
                DISPLAYSURF.blit(txt_surface, (x, y))

            # Draw the border of the input box
            pygame.draw.rect(DISPLAYSURF, self.color, self.rect, 1)
        except:
            pass 

class ButtonBox():
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = COLOR_ACTIVE
        self.text = text
        FONT = pygame.font.Font(None, int(height*0.8))
        self.txt_surface = FONT.render(text, True, self.color)
        self.size = self.txt_surface.get_size()
        
        # Add a variable to keep track of whether the button is currently flashing
        self.flashing = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.flashing = True

    def draw(self):
        # Change the button color to red if it is currently flashing
        a = self.rect.x+(-self.size[0]+self.rect.width)/2
        b = self.rect.y+(-self.size[1]+self.rect.height)/2 
        if self.flashing:
            self.txt_surface = FONT.render(self.text, True, RED)
            DISPLAYSURF.blit(self.txt_surface, (a,b))
            pygame.draw.rect(DISPLAYSURF, RED, self.rect, 3)
            pygame.time.delay(100)
            self.txt_surface = FONT.render(self.text, True, COLOR_ACTIVE)
            self.flashing = False
        else:
            DISPLAYSURF.blit(self.txt_surface, (a,b))
            pygame.draw.rect(DISPLAYSURF, self.color, self.rect, 3)

        

def GamePlay():
     global Err
     but1 = ButtonBox(size[0]-150,105,100,40,"RESET")
     but2 = ButtonBox(size[0]-300,105,100,40,"START")
     but3 = ButtonBox(size[0]-450,105,100,40,"COPY")
     but4 = ButtonBox(350,105,250,40,"<Link Error>")

     text1 = ButtonBox(50,5,250,40,"< NEWS LINK >")
     text2 = ButtonBox(50,105,100,40,"<TEXT>")

     box = InputBox(50,50,size[0]-100,50)
     box2 = InputBox(50,150,size[0]-100,size[1]-200)
     while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    url = box.text
                    box2.text = Te.crawl(url) 
            if event.type == pygame.MOUSEBUTTONDOWN:
                Err = False
                if but1.rect.collidepoint(event.pos):
                    box.text = ""
                    box2.text = ""
                elif but2.rect.collidepoint(event.pos):
                    try:
                        url = box.text 
                        box2.text = Te.crawl(url) 
                    except:
                        pass
                elif but3.rect.collidepoint(event.pos):
                    try:
                        pygame.scrap.init()
                        pygame.scrap.put(pygame.SCRAP_TEXT, box2.text.encode('utf-8'))
                    except:
                        pass

            but1.handle_event(event) 
            but2.handle_event(event) 
            but3.handle_event(event)

            box.handle_event(event)
            box2.handle_event(event)

        DISPLAYSURF.fill(color_backg)

        but1.draw()
        but2.draw()
        but3.draw()

        text1.draw()
        text2.draw()

        box.draw()
        box2.draw()

        if Err == True:
            but4.color = RED
            but4.txt_surface = FONT.render("<Link Error>", True, RED)
            but4.draw()
        
        pygame.display.update()
        fpsClock.tick(FPS)

def main():
    while True: 
        GamePlay()


if __name__ == "__main__":
    main()