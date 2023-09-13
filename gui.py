import pygame as p, random, os, engine
p.init()
p.mixer.init()
p.key.set_repeat()
dictionary = engine.read_file("dictionary.txt")

class Settings():  #for easy future modification/s
    def __init__(self):
        self.name   = 'Word Unscrambler'
        self.assets = os.path.relpath('Assets')
        self.clock  = p.time.Clock()
        self.width  = 1280
        self.height = 720

        self.screen = p.display.set_mode((self.width, self.height))
        self.tag    = p.display.set_caption(self.name)
        self.h_font = p.font.SysFont('8bitwondernominal', 30)
        self.n_font = p.font.SysFont('8bitwondernominal', 20)
        self.frames = 50
        self.colors = {"red"   : (255, 0, 0),
                       "green" : (0, 255, 0),
                       "blue"  : (0, 0, 255),
                       "yellow": (255, 255, 0),
                       "purple": (255, 0, 255),
                       "orange": (255, 165, 0),
                       "white" : (255, 255, 255),
                       "black" : (0, 0, 0),
                       "brown" : (153, 76, 0),
                       "lgray" : (170, 171, 171),
                       "llgray": (192, 191, 192),
                       "grey"  : (100, 100, 100),
                       "bg_g"  : (40, 42, 55)}
        @property
        def  width(self): return self.width
        @property
        def height(self): return self.height
        @property
        def  font(self): return self.f_big
        @width.setter
        def  width(self, x): self._width  = x
        @height.setter
        def height(self, x): self._height = x
        @font.setter
        def  font(self, f, x): self._font  = p.font.SysFont(f, x)

#shortcuts
z   = Settings()
a   = z.assets
c   = z.colors
d   = z.screen
f_f = z.n_font
f_h = z.h_font
sw, sh, sc = z.width, z.height, (z.width/2, z.height/2)

def asset(x): return os.path.join(a, x) + '.png'  #shortcut for calling images from \Assets
def collide(x, m): return p.Rect(x).collidepoint(m)  #collision detection shortcut
def seq(x, y): #makes sure number stays in range 0-3
    if x>=len(y): x -= 3
    elif x<0: x += 3
    return x
def fade(): #tints screen
    fade = p.Surface((sw, sh))
    fade.fill(c['black'])
    fade.set_alpha(150)
    d.blit(fade, (0, 0))

#art shortcuts
bg   = p.image.load(asset('Background'))
life = p.image.load(asset('Life')).convert_alpha()
m_h  = p.image.load(asset('Menu_H')).convert_alpha()
m_v  = p.image.load(asset('Menu_V')).convert_alpha()
p_b  = p.image.load(asset('Panel_Big')).convert_alpha()
p_s  = p.image.load(asset('Panel_Small')).convert_alpha()
p_m  = p.image.load(asset('Menu_Pause')).convert_alpha()
pane = p.image.load(asset('Panel')).convert_alpha()
t_b  = p.image.load(asset('Input')).convert_alpha()
t_f  = p.image.load(asset('T_Left')).convert_alpha()
t_l  = p.image.load(asset('T_Lives')).convert_alpha()
t_s  = p.image.load(asset('T_Score')).convert_alpha()
t_t  = p.image.load(asset('T_Time')).convert_alpha()
tile = p.image.load(asset('Tile')).convert_alpha()
buzz = p.mixer.Sound(a+os.path.sep+'Buzz.wav')

pause_state = 1

def menu_screen():  #mode and difficulty selection
    d.blit(bg, (0, 0))
    d.blit(m_v, (sc[0]-m_v.get_rect().width/2, 0))
    text = f_h.render('SETUP', True, c['white'])
    d.blit(text, (sc[0]-text.get_rect().width/2, 23))
    mode = ['ANAGRAM', 'COMBINE', '[COMING SOON]']
    diff = ['ZEN', 'CHALLENGE', 'HELL']
    md, df = 0, 0
    while True:
        p.draw.rect(d, c['grey'], (sc[0]-150, 90, 300, 46))
        md_s = f_f.render(mode[md], True, c['white'])
        d.blit(md_s, (sc[0]-md_s.get_rect().width/2, 101))
        df_s = f_f.render(diff[df], True, c['white'])
        p.draw.rect(d, c['grey'], (sc[0]-150, sc[1]+23, 300, 46))
        d.blit(df_s, (sc[0]-df_s.get_rect().width/2, sc[1]+34))
        mode_r = button(sc[0]+175, 113, 'Arrow_R')
        mode_l = button(sc[0]-175, 113, 'Arrow_L')
        diff_r = button(sc[0]+175, sc[1]+46, 'Arrow_R')
        diff_l = button(sc[0]-175, sc[1]+46, 'Arrow_L')
        start = button(sc[0], sh-46, 'Start0', 'Start1')
        p.draw.rect(d, c['black'], (sc[0]-200, 136, 400, 200))
        p.draw.rect(d, c['black'], (sc[0]-200, sc[1]+69, 400, 100))
        md_i = p.image.load(asset('MD_'+str(md))).convert_alpha()
        df_i = p.image.load(asset('DF_'+str(df))).convert_alpha()
        d.blit(md_i, (sc[0]-md_i.get_rect().width/2, 136))
        d.blit(df_i, (sc[0]-df_i.get_rect().width/2, sc[1]+69))
        for event in p.event.get():
            if event.type == p.QUIT: quit()
            elif event.type == p.KEYDOWN:
                if event.key == p.K_RETURN:
                    if md==2: buzz.play()
                    else: g_screen(md, df)
            elif event.type == p.MOUSEBUTTONDOWN:
                m = p.mouse.get_pos()
                if collide(start, m):
                    if md==2: buzz.play()
                    else: g_screen(md, df)
                if collide(mode_r, m): md = seq(md+1, mode)
                if collide(mode_l, m): md = seq(md-1, mode)
                if collide(diff_r, m): df = seq(df+1, diff)
                if collide(diff_l, m): df = seq(df-1, diff)
        p.display.update()
        z.clock.tick(z.frames)

def timer_update(timer, time, x=100, y=25):  #updates time for g_screen
    timer, x2 = timer+1, x+t_t.get_rect().width+22
    d.blit(t_t, (x, y+5))
    if timer*20%1000==0: time -= 1
    t_surf = f_h.render(str(time), True, c['white'])
    p.draw.rect(d, c['bg_g'], (x2, y, 100, t_surf.get_rect().height))
    d.blit(t_surf, (x2, y))
    return timer, time

def lives_update(lives, x=40, y=670):  #updates lives for g_screen
    d.blit(t_l, (x, y+5))
    i, x2 = 0, x+t_l.get_rect().width+23
    p.draw.rect(d, c['bg_g'], (x2, y, 400, 55))
    while i<lives:
        d.blit(life, (x2, y))
        x2, i = x2+66, i+1
    return lives
   
def score_update(score, x=480, y=25):  #updates score for g_screen
    d.blit(t_s, (x, y+5))
    s_surf, x2 = f_h.render(str(score), True, c['white']), x+t_s.get_rect().width+22
    p.draw.rect(d, c['bg_g'], (x2, y, t_s.get_rect().width, t_s.get_rect().height + 5))
    d.blit(s_surf, (x2, y))
    return score

def g_screen(md, df, word_list=[]):  #main display screen with text input
    global pause_state
    text, timer, time, lives, score, done, highest = '', 999, 100, 5, 0, [], []
    if md==0: game = engine.AnagramMode(dictionary)
    elif md==1: game = engine.CombineMode(dictionary)
    scramble, word_list = ''.join(random.sample(game.word, len(game.word))), game.words
    n = max([len(i) for i in word_list])
    while True:
        if pause_state == 1:
            left = str(len(word_list)-len(done))
            d.blit(bg, (0, 0))
            d.blit(p_b, (sc[0]-p_b.get_rect().width/2, 70))
            d.blit(p_s, (sc[0]-p_s.get_rect().width/2, 445))
            d.blit(t_f, (1000, 675))
            d.blit(f_h.render(left, True, c['white']), (1180, 670))
            if md==0: text, lives, score, done = list_words(text, lives, score, done, word_list)
            elif md==1: text, lives, score, highest, done = list_highs(text, lives, score, highest, done, word_list)
            if df==0 or df==2: prev_lives = lives_update(lives)
            prev_score = score_update(score)
            timer, pause_state = 999, 0
     
        if df==1 or df==2: timer, time = timer_update(timer, time)
        pause  = button(sw-25, 25, 'Pause0', 'Pause1')
        p.draw.rect(d, c['lgray'], (sc[0]-90, 538, 180, 24))
        shuff  = button(sc[0], 550, 'Shuffle0', 'Shuffle1')
        for event in p.event.get():
            if event.type == p.MOUSEBUTTONDOWN:
                m = p.mouse.get_pos()
                if collide(pause, m): pause_panel(md, df, word_list)
                elif collide(shuff, m): scramble = ''.join(random.sample(scramble, len(scramble)))
            elif event.type == p.KEYDOWN:
                if event.key == p.K_RETURN:
                    if len(text)>2:
                        if md==0: text, lives, score, done = list_words(text, lives, score, done, word_list)
                        elif md==1: text, lives, score, highest, done = list_highs(text, lives, score, highest, done, word_list)
                    if df==0 or df==2:
                        if prev_lives!=lives: prev_lives = lives_update(lives)
                    if prev_score!=score: prev_score = score_update(score)
                    left   = str(len(word_list)-len(done))
                    p.draw.rect(d, c['bg_g'], (1180, 670, 160, 55))
                    d.blit(f_h.render(left, True, c['white']), (1180, 670))
                elif event.key == p.K_BACKSPACE: text = text[:-1]
                else: text += event.unicode.upper()
        if sorted(done)==sorted(word_list): end_panel('WIN', md, df)
        elif lives==0 or time==0: end_panel('LOSE', md, df)

        text = text[:n]
        scram  = f_h.render(scramble, True, c['white'])
        t_surf = f_f.render(text, True, c['white'])
        p.draw.rect(d, c['black'], (sc[0]-t_b.get_rect().width/2+20, 572, t_b.get_rect().width-40, 42))
        p.draw.rect(d, c['lgray'], (sc[0]-scram.get_rect().width/2, 475, scram.get_rect().width, scram.get_rect().height))
        d.blit(scram, (sc[0]-scram.get_rect().width/2, 475))
        d.blit(t_b, (sc[0]-t_b.get_rect().width/2, 570))
        d.blit(t_surf, (sc[0]-t_surf.get_rect().width/2, 580))
        p.display.update()
        z.clock.tick(z.frames)

def pause_panel(md, df, word_list, x=465, y=310):  #pause screen
    global pause_state
    pause_state = 1
    fade()
    d.blit(p_m, (340, 100))
    while True:
        resu = button(x, y,     'Play0', 'Play1')
        rest = button(x, y+90,  'Res0', 'Res1')
        menu = button(x, y+180, 'Exit0', 'Exit1')
        for event in p.event.get():
            if event.type == p.MOUSEBUTTONDOWN:
                m = p.mouse.get_pos()
                if   collide(resu, m): return
                elif collide(rest, m): return g_screen(md, df, word_list)
                elif collide(menu, m): menu_screen()
        p.display.update()
        z.clock.tick(z.frames)

def end_panel(text, md, df):  #win/lose screen
    global pause_state, done
    pause_state, done = 1, []
    x, y = sc[0]-pane.get_rect().width/2, sc[1]-pane.get_rect().height/2
    fade()
    d.blit(pane, (x, y))
    while True:
        msg = f_h.render(text, True, c['white'])
        d.blit(msg, (x+(200-msg.get_rect().width)/2, y+10))
        rest = button(x+100, y+91,  'Restart0', 'Restart1')
        menu = button(x+100, y+152, 'Menu0', 'Menu1')
        bbye = button(x+100, y+213, 'Quit0', 'Quit1')
        for event in p.event.get():
            if event.type == p.MOUSEBUTTONDOWN:
                m = p.mouse.get_pos()
                if   collide(rest, m): g_screen(md, df)
                elif collide(menu, m): menu_screen()
                elif collide(bbye, m): quit()
        p.display.update()
        z.clock.tick(z.frames)

def list_words(text, lives, score, done, word_list):  #processes display for anagram mode
    i, y = 0, 100
    while i<len(word_list):
        if i==0:
            if len(word_list)<=4: x = sc[0]-200
            elif 5<len(word_list)<11: x = 300
            else: x = 200
        if i!=0 and i%5==0:
            x, y = x+300, 100
            def_x = x
        else: def_x = x
        if (text.lower()==word_list[i] or word_list[i] in done) and text!='':
            if text.lower() not in done:
                if text.lower() in word_list:
                    score += engine.scrabble_score(text.lower())
                    done.append(text.lower())
            for j in range(len(word_list[i])):
                slot = f_f.render(word_list[i][j], True, c['white'])
                d.blit(tile, (x, y))
                d.blit(slot, (x+tile.get_rect().width/2-slot.get_rect().width/2,
                              y+tile.get_rect().height/2-slot.get_rect().height/2))
                x += 46
        else:
            for j in range(len(word_list[i])):
                slot  = f_f.render(word_list[i][j], True, c['llgray'])
                d.blit(tile, (x, y))
                d.blit(slot, (x+tile.get_rect().width/2-slot.get_rect().width/2,
                              y+tile.get_rect().height/2-slot.get_rect().height/2))
                x += 46
        x = def_x
        i, y = i+1, y+50
    if text!='' and text.lower() not in word_list: lives -= 1
    return '', lives, score, done

def list_highs(text, lives, score, highest, done, word_list):  #processes display for combine mode
    i, y = 0, 100
    if text!='' and text.lower() in word_list and text.lower() not in highest and text.lower() not in done:
        done.append(text.lower())
        if len(highest)<6: highest.append(text.lower())
        else:
            while i < len(highest):
                if text!='' and engine.scrabble_score(text.lower())==engine.scrabble_score(highest[i]) and text.lower() not in highest:
                    if text.lower()>=highest[i]: highest.insert(i, text.lower())
                    else: highest.insert(i+1, text.lower())
                    score, i = score+engine.scrabble_score(text.lower()), i+1
                elif text!='' and engine.scrabble_score(text.lower())>engine.scrabble_score(highest[i]) and text.lower() not in highest:
                    highest.insert(i, text.lower())
                    score, i = score+engine.scrabble_score(text.lower()), i+1
                i += 1
    elif text!='' and text.lower() not in highest: lives -= 1
    highest, i = sorted(highest[:6], key=lambda x: engine.scrabble_score(x), reverse=True), 0
    p.draw.rect(d, c['lgray'], (sc[0]-300, 100, 600, 275))
    while i < len(highest):
        word  = f_f.render(highest[i]+'     '+str(engine.scrabble_score(highest[i])), True, c['white'])
        d.blit(word, (sc[0]-word.get_rect().width/2, y))
        i, y = i+1, y+50
    return '', lives, score, highest, done

def button(x, y, off, on=0):  #button creation shortcut
    mouse = p.mouse.get_pos()
    b_off = p.image.load(asset(off)).convert_alpha()
    if on!=0: b_on = p.image.load(asset(on)).convert_alpha()
    w, h = b_off.get_rect().width, b_off.get_rect().height
    new_x, new_y = x-w/2, y-h/2
    if new_x+w>mouse[0]>new_x and new_y+h>mouse[1]>new_y and on!=0: d.blit(b_on, (new_x, new_y))
    else: d.blit(b_off, (new_x, new_y))
    return (new_x, new_y, w, h)
