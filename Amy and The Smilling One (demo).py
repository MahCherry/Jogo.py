import pygame
pygame.init()
pygame.mixer.init()

# === Trilha sonora e efeitos ===
musica_cutscene = "sad.mp3"
musica_corredor = "mysterious.mp3"
musica_cenario1 = "suspense.mp3"
musica_morte = "dead.mp3"

som_digito = pygame.mixer.Sound("Efeito Sonoro dialogo.mp3")
som_digito.set_volume(0.5)

# === Tela e jogo ===
tela_largura, tela_altura = 800, 600
tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption("Jogo da Amy")
clock = pygame.time.Clock()
velocidade = 2.5

# === Cores e fontes ===
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO_ESCURO = (150, 0, 0)
VERDE_ESCURO = (0, 100, 0)
AMARELO_SUAVE = (255, 255, 100)
CINZA_ESCURO = (70, 70, 70)
CINZA_CLARO = (120, 120, 120)

fonte = pygame.font.SysFont("arial", 20)
fonte_opcao = pygame.font.SysFont("arial", 18)
fonte_sanidade = pygame.font.SysFont("arial", 16, bold=True)

# === Sprites da Amy e NPCs ===
nova_largura, nova_altura = 300, 500
sprite_parado_frente = pygame.transform.scale(pygame.image.load("AmyLonsydeFrente.png").convert_alpha(), (nova_largura, nova_altura))
sprite_andando_frente = pygame.transform.scale(pygame.image.load("AmyFrente.png").convert_alpha(), (nova_largura, nova_altura))
sprite_direita = pygame.transform.scale(pygame.image.load("AmyLonsyDireita.png").convert_alpha(), (nova_largura, nova_altura))
sprite_esquerda = pygame.transform.scale(pygame.image.load("AmyLonsyEsquerda.png").convert_alpha(), (nova_largura, nova_altura))
sprite_costas = pygame.transform.scale(pygame.image.load("AmyCostas.png").convert_alpha(), (nova_largura, nova_altura))

sprite_percy_1 = pygame.transform.scale(pygame.image.load("Percy1.png").convert_alpha(), (nova_largura, nova_altura))
sprite_percy_2 = pygame.transform.scale(pygame.image.load("Percy2.png").convert_alpha(), (nova_largura, nova_altura))

sprite_invasor_parado = pygame.transform.scale(pygame.image.load("theo.png").convert_alpha(), (nova_largura, nova_altura))
sprite_invasor_andando = pygame.transform.scale(pygame.image.load("TheoAndando.png").convert_alpha(), (nova_largura, nova_altura))

sprite_remedio = pygame.transform.scale(pygame.image.load("remedio.png").convert_alpha(), (60, 60))
sprite_chave = pygame.transform.scale(pygame.image.load("chave.png").convert_alpha(), (30, 30))

item_remedio = {"x": 485, "y": 295, "ativo": True, "sprite": sprite_remedio}
item_chave = {"x": 467, "y": 250, "ativo": True, "sprite": sprite_chave}

# === Cenários e cutscenes ===
cenario_0 = pygame.transform.scale(pygame.image.load("corredor.jpeg").convert(), (tela_largura, tela_altura))
cenario_1 = pygame.transform.scale(pygame.image.load("cenario.png").convert(), (tela_largura, tela_altura))
cenario_2 = pygame.transform.scale(pygame.image.load("cenario2.png").convert(), (tela_largura, tela_altura))
cutscene1_img = pygame.transform.scale(pygame.image.load("ImagemCutscene2.png").convert(), (tela_largura, tela_altura))
cutscene2_img = pygame.transform.scale(pygame.image.load("ImagemCutscene1.png").convert(), (tela_largura, tela_altura))
cenarios = [cenario_0, cenario_1, cenario_2]

portas = [[(700, 50)], [(50, 50), (700, 50)], [(700, 50)]]

# === Estado inicial do jogo ===
cenario_atual = 0
personagem_x = 100
personagem_y_base = 100
deslocamento_y = 0
percy_x = 500
mostrar_percy_1 = True
tempo_animacao = 500
ultima_troca = pygame.time.get_ticks()
invasor_x = 900
invasor_velocidade = 1.7
invasor_andando = False
cutscene_ativa = False
morte_triggerada = False
# === Função para tocar música ===
def tocar_musica(caminho, volume=0.5, loop=-1):
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loop)
    except pygame.error as e:
        print(f"Erro ao tocar música '{caminho}': {e}")

# === Função de cutscene com imagem e texto revelado ===
def exibir_cutscene(texto, imagem=None, velocidade_texto=45):
    linhas = texto.strip().split("\n")
    y = 100
    for linha in linhas:
        exibido = ""
        for letra in linha:
            exibido += letra

            # Fundo
            if imagem:
                tela.blit(imagem, (0, 0))
            else:
                tela.fill(PRETO)

            # Som ao digitar
            if letra.strip():
                som_digito.play()

            # Texto com sombra
            sombra = fonte.render(exibido, True, (30, 30, 30))
            texto_render = fonte.render(exibido, True, BRANCO)
            tela.blit(sombra, (62, y + 2))
            tela.blit(texto_render, (60, y))

            pygame.display.flip()
            pygame.time.wait(velocidade_texto)

        y += 40
        pygame.time.wait(300)
    pygame.time.wait(1000)

# === Textos das cutscenes ===
texto_cutscene_inicial = """
Estou resolvendo um caso... Que me lembra de tanta coisa...
Eu havia só 8 anos... quando fui andar na rua...
vi coisas que não devia... que iam me assombrar a vida inteira...
eu vi um homem matando...
Não lembro rostos... a lembrança do rosto do mesmo para mim era um borrão...
E agora parece que tenho um déjà vu.
"""

texto_cutscene_final = """
Sorrisos... sorrisos demais.
A minha boca... não fechava. Nem depois da morte.
Ele me deixou uma carta.
Escreveu com um emoji sorridente. Como se fosse... uma diversão para o seu prazer.
Eu ainda lembro do cheiro.
Do som.
Do silêncio…
Antes de tudo morrer, sumir num piscar de olhos.
Assim como a minha sanidade.... E eu... Eu era a vítima.
"""

# === Classe de sanidade ===
class Sanidade:
    def __init__(self):
        self.max_sanidade = 100
        self.sanidade_atual = 80
        self.ultima_decrescimo = pygame.time.get_ticks()
        self.intervalo_decrescimo = 10000
        self.taxa_decrescimo = 5
        self.critico = 30
        self.perigo = 50

    def update(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultima_decrescimo > self.intervalo_decrescimo:
            self.sanidade_atual = max(0, self.sanidade_atual - self.taxa_decrescimo)
            self.ultima_decrescimo = agora

    def aumentar_sanidade(self, qtd):
        self.sanidade_atual = min(self.max_sanidade, self.sanidade_atual + qtd)

    def draw(self, surface):
        pygame.draw.rect(surface, CINZA_ESCURO, (10, 10, 200, 25))
        pygame.draw.rect(surface, CINZA_CLARO, (10, 10, 200, 25), 2)
        largura = int((self.sanidade_atual / self.max_sanidade) * 200)
        cor = VERDE_ESCURO if self.sanidade_atual > self.perigo else (
            AMARELO_SUAVE if self.sanidade_atual > self.critico else VERMELHO_ESCURO)
        pygame.draw.rect(surface, cor, (10, 10, largura, 25))
        texto = fonte_sanidade.render(f"Sanidade: {int(self.sanidade_atual)}/100", True, BRANCO)
        surface.blit(texto, (220, 10))

# === Diálogo com Percy ===
fala_percy = "Então você é a novata no FBI? Sabe, entrou na hora errada, temos o pior caso para resolver..."
opcoes = [
    "Sério? Que frescura...",
    "Vou tentar o meu melhor.",
    "Talvez sim... talvez não..."
]
respostas_percy = [
    "Vamos ver quanto tempo você aguenta...",
    "Boa sorte. Vai precisar.",
    "Então venha. O caso nos espera."
]

class DialogSystem:
    def __init__(self):
        self.active = False
        self.stage = 0
        self.message = ""
        self.options = []
        self.responses = []
        self.selected = None
        self.timer = 0
        self.duration = 3000

    def start(self, msg, ops, resps):
        self.active = True
        self.stage = 0
        self.message = msg
        self.options = ops
        self.responses = resps
        self.selected = None
        self.timer = 0

    def handle_event(self, evento):
        if not self.active or evento.type != pygame.MOUSEBUTTONDOWN:
            return
        mouse = pygame.mouse.get_pos()
        box = pygame.Rect(50, 300, 700, 250)
        if self.stage == 0:
            botao = pygame.Rect(box.right - 120, box.bottom - 40, 100, 30)
            if botao.collidepoint(mouse):
                self.stage = 1
        elif self.stage == 1:
            for i in range(len(self.options)):
                r = pygame.Rect(70, 370 + i * 45, 660, 35)
                if r.collidepoint(mouse):
                    self.selected = i
                    self.stage = 2
                    self.timer = pygame.time.get_ticks()

    def update(self):
        if self.stage == 2 and pygame.time.get_ticks() - self.timer > self.duration:
            self.active = False

    def draw(self, tela):
        if not self.active:
            return
        caixa = pygame.Rect(50, 300, 700, 250)
        pygame.draw.rect(tela, PRETO, caixa)
        pygame.draw.rect(tela, BRANCO, caixa, 2)
        if self.stage == 0:
            renderizar_texto_quebrado(tela, self.message, fonte, BRANCO, caixa)
            botao = pygame.Rect(caixa.right - 120, caixa.bottom - 40, 100, 30)
            pygame.draw.rect(tela, CINZA_ESCURO, botao)
            pygame.draw.rect(tela, BRANCO, botao, 1)
            texto = fonte.render("Continuar", True, BRANCO)
            tela.blit(texto, (botao.x + 10, botao.y + 5))
        elif self.stage == 1:
            renderizar_texto_quebrado(tela, self.message, fonte, BRANCO, pygame.Rect(60, 310, 680, 50))
            for i, opcao in enumerate(self.options):
                r = pygame.Rect(70, 370 + i * 45, 660, 35)
                cor = (100, 100, 100) if r.collidepoint(pygame.mouse.get_pos()) else (50, 50, 50)
                pygame.draw.rect(tela, cor, r)
                pygame.draw.rect(tela, BRANCO, r, 1)
                txt = fonte_opcao.render(opcao, True, BRANCO)
                tela.blit(txt, (r.x + 10, r.y + 8))
        elif self.stage == 2 and self.selected is not None:
            renderizar_texto_quebrado(tela, self.responses[self.selected], fonte, BRANCO, caixa)

def renderizar_texto_quebrado(surface, texto, fonte, cor, rect, x_offset=10, y_offset=10):
    palavras = texto.split()
    linhas = []
    linha_atual = ""
    for palavra in palavras:
        tentativa = f"{linha_atual} {palavra}".strip()
        if fonte.size(tentativa)[0] <= rect.width - 2 * x_offset:
            linha_atual = tentativa
        else:
            linhas.append(linha_atual)
            linha_atual = palavra
    if linha_atual:
        linhas.append(linha_atual)
    y = rect.y + y_offset
    for linha in linhas:
        surface.blit(fonte.render(linha, True, cor), (rect.x + x_offset, y))
        y += fonte.get_height() + 5

def escolher_sprite(teclas):
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        return sprite_direita
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        return sprite_esquerda
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        return sprite_costas
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        return sprite_andando_frente
    return sprite_parado_frente  # 👈 Se nenhuma tecla for pressionada
# === INICIALIZAÇÃO DE SISTEMAS ===
sanidade = Sanidade()
dialog = DialogSystem()
rodando = True

# === CUTSCENE DE ABERTURA + MÚSICA DO CENÁRIO ===
tocar_musica(musica_cutscene)
exibir_cutscene(texto_cutscene_inicial, imagem=cutscene1_img)
tocar_musica(musica_corredor)  # inicia música do corredor (cenário 0)

# === LOOP PRINCIPAL ===
while rodando:
    tela.blit(cenarios[cenario_atual], (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_e:
                if cenario_atual == 1 and abs(personagem_x - percy_x) < 200 and not dialog.active:
                    dialog.start(fala_percy, opcoes, respostas_percy)

            if evento.key == pygame.K_r:
                if cenario_atual == 1 and item_remedio["ativo"] and abs(personagem_x - item_remedio["x"]) < 100:
                    sanidade.aumentar_sanidade(20)
                    item_remedio["ativo"] = False
                if cenario_atual == 1 and item_chave["ativo"] and abs(personagem_x - item_chave["x"]) < 100:
                    item_chave["ativo"] = False

        dialog.handle_event(evento)

    teclas = pygame.key.get_pressed()
    if not dialog.active and not cutscene_ativa:
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            personagem_x += velocidade
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            personagem_x -= velocidade
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            deslocamento_y -= velocidade * 0.5
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            deslocamento_y += velocidade * 0.5

    agora = pygame.time.get_ticks()
    if agora - ultima_troca > tempo_animacao:
        mostrar_percy_1 = not mostrar_percy_1
        ultima_troca = agora

    # === INVASOR NO CENÁRIO 2 ===
    if cenario_atual == 2:
        cutscene_ativa = True
        invasor_andando = True
        if invasor_x > personagem_x:
            invasor_x -= invasor_velocidade
        elif invasor_x < personagem_x:
            invasor_x += invasor_velocidade

        sanidade.sanidade_atual = max(0, sanidade.sanidade_atual - 0.2)

        if not morte_triggerada and abs(invasor_x - personagem_x) < 100:
            tela.fill(PRETO)
            mensagem_morte = fonte.render("VOCÊ MORREU", True, VERMELHO_ESCURO)
            tela.blit(mensagem_morte, (tela_largura // 2 - 80, tela_altura // 2))
            pygame.display.flip()
            tocar_musica(musica_morte)
            pygame.time.wait(1000)
            exibir_cutscene(texto_cutscene_final, imagem=cutscene2_img)
            rodando = False
            morte_triggerada = True
            continue
    else:
        cutscene_ativa = False
        invasor_andando = False
        invasor_x = 900
        morte_triggerada = False

    # === GAME OVER — SANIDADE ZERADA ===
    sanidade.update()
    if sanidade.sanidade_atual <= 0:
        tela.fill(PRETO)
        texto = fonte.render("GAME OVER — Sanidade esgotada!", True, VERMELHO_ESCURO)
        tela.blit(texto, (tela_largura // 2 - 150, tela_altura // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        break

    # === TROCA DE CENÁRIOS ===
    for porta in portas[cenario_atual]:
        px, plarg = porta
        if personagem_x + nova_largura > px and personagem_x < px + plarg:
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                if px > personagem_x and cenario_atual < len(cenarios) - 1:
                    cenario_atual += 1
                    personagem_x = 60
                    # 🎵 Música do novo cenário
                    if cenario_atual == 0:
                        tocar_musica(musica_corredor)
                    elif cenario_atual == 1:
                        tocar_musica(musica_cenario1)
                    elif cenario_atual == 2:
                        tocar_musica(musica_corredor)

            elif teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                if px < personagem_x and cenario_atual > 0:
                    cenario_atual -= 1
                    personagem_x = tela_largura - nova_largura - 60
                    if cenario_atual == 0:
                        tocar_musica(musica_corredor)
                    elif cenario_atual == 1:
                        tocar_musica(musica_cenario1)
                    elif cenario_atual == 2:
                        tocar_musica(musica_corredor)

    # === DESENHO DE ELEMENTOS ===
    for porta in portas[cenario_atual]:
        pygame.draw.rect(tela, (200, 100, 0), (porta[0], personagem_y_base + nova_altura - 10, porta[1], 80))

    if cenario_atual == 1:
        sprite_percy = sprite_percy_1 if mostrar_percy_1 else sprite_percy_2
        tela.blit(sprite_percy, (percy_x, personagem_y_base))

    if cenario_atual == 1 and item_remedio["ativo"]:
        tela.blit(item_remedio["sprite"], (item_remedio["x"], item_remedio["y"]))
        texto = fonte.render("Remédio", True, BRANCO)
        tela.blit(texto, (item_remedio["x"] - 30, item_remedio["y"] - 20))

    if cenario_atual == 1 and item_chave["ativo"]:
        tela.blit(item_chave["sprite"], (item_chave["x"], item_chave["y"]))
        texto = fonte.render("Chave", True, BRANCO)
        tela.blit(texto, (item_chave["x"] - 20, item_chave["y"] - 20))

    if cenario_atual == 2:
        sprite_invasor = sprite_invasor_andando if invasor_andando else sprite_invasor_parado
        tela.blit(sprite_invasor, (invasor_x, personagem_y_base))

    # === AMY, DIÁLOGO E INTERFACE ===
    sprite_amy = escolher_sprite(teclas)
    tela.blit(sprite_amy, (personagem_x, personagem_y_base + deslocamento_y))

    if cenario_atual == 1 and abs(personagem_x - percy_x) < 200 and not dialog.active:
        tela.blit(fonte.render("Aperte E para conversar", True, BRANCO), (20, 550))
    if cenario_atual == 1 and item_remedio["ativo"] and abs(personagem_x - item_remedio["x"]) < 100:
        tela.blit(fonte.render("Pressione R para tomar remédio (+20 sanidade)", True, BRANCO), (20, 500))
    if cenario_atual == 1 and item_chave["ativo"] and abs(personagem_x - item_chave["x"]) < 100:
        tela.blit(fonte.render("Pressione R para pegar a chave", True, BRANCO), (20, 470))

    dialog.update()
    dialog.draw(tela)
    sanidade.draw(tela)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
