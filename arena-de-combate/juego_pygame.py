# =============================================================================
#  ARENA DE COMBATE  ·  VERSIÓN 3 · PYGAME
#  El MISMO juego, convertido en un videojuego de verdad.
#
#  Cómo se ejecuta:   pip install pygame      (una sola vez)
#                     python3 juego_pygame.py
# =============================================================================
#
#  SIGUE SIENDO EL MISMO PROYECTO. Compará con juego_consola.py:
#
#    · Personaje sigue siendo la clase de arriba, con vida, recibir_danio()
#      (con su if de encapsulación) y esta_vivo() devolviendo True o False.
#    · Jugador ES UN Personaje  ............ herencia + super()
#    · Jugador TIENE UN Arma  .............. composición
#    · Goblin, Esqueleto, Dragon y JefeFinal responden atacar() cada uno a su
#      manera, y el juego nunca pregunta de qué clase son  ... polimorfismo
#    · atacar() y usar() siguen devolviendo el número del daño ..... return
#
#  LO NUEVO DE ESTA VERSIÓN (todo lo que suma Pygame)
#    ventana · superficies · dibujo · fuentes · colores · teclado · mouse ·
#    eventos · movimiento · animaciones · sprites · grupos · colisiones ·
#    sonidos · música · temporizadores · FPS · estados de pantalla · menú ·
#    HUD · minimapa · proyectiles · partículas · niveles · jefe final
#
#  NINGÚN GRÁFICO VIENE DE INTERNET: todos los personajes se dibujan con
#  pygame.draw sobre superficies, y los sonidos los genera assets/generar_sonidos.py
#  Por eso el juego no depende de ningún archivo que pueda faltar.
# =============================================================================

import math
import os
import random

import pygame

# ----------------------------------------------------------------- constantes
ANCHO = 1024
ALTO = 640
ALTO_HUD = 78                      # la franja de arriba con la vida y el puntaje
ALTO_ARENA = ALTO - ALTO_HUD
FPS = 60

CARPETA = os.path.dirname(os.path.abspath(__file__))
CARPETA_SONIDOS = os.path.join(CARPETA, "assets", "sonidos")
CARPETA_MUSICA = os.path.join(CARPETA, "assets", "musica")

# --------------------------------------------------------------------- colores
NEGRO       = (12, 14, 22)
BLANCO      = (236, 240, 248)
GRIS        = (138, 147, 168)
GRIS_OSCURO = (38, 44, 62)
ORO         = (242, 177, 52)
ROJO        = (224, 85, 60)
ROJO_OSCURO = (140, 44, 34)
VERDE       = (63, 178, 127)
AZUL        = (74, 124, 240)
VIOLETA     = (139, 92, 246)
CELESTE     = (120, 200, 230)
HUESO       = (216, 214, 204)


# =============================================================================
#  PARTE 1 · LOS GRÁFICOS
#  Cada personaje es una lista de imágenes (pygame.Surface) dibujadas con
#  pygame.draw. Dos imágenes por personaje = una animación de dos cuadros.
# =============================================================================

SPRITES = {}          # se llena en crear_sprites(), ya con la ventana abierta


def superficie(ancho, alto):
    """Una imagen vacía y transparente sobre la que vamos a dibujar."""
    return pygame.Surface((ancho, alto), pygame.SRCALPHA)


def frames_heroe():
    """El héroe, mirando a la derecha. Dos cuadros: quieto y con el paso dado."""
    cuadros = []
    for paso in range(2):
        s = superficie(52, 60)
        subir = 2 if paso == 1 else 0
        # capa
        pygame.draw.polygon(s, (40, 60, 130), [(14, 20 - subir), (38, 20 - subir),
                                               (44, 52), (8, 52)])
        # cuerpo
        pygame.draw.rect(s, AZUL, (16, 20 - subir, 20, 24), border_radius=5)
        pygame.draw.rect(s, (150, 175, 255), (16, 26 - subir, 20, 4))
        # piernas
        pygame.draw.rect(s, (45, 54, 84), (17, 44 - subir, 7, 12), border_radius=2)
        pygame.draw.rect(s, (45, 54, 84), (28, 44 + subir, 7, 12), border_radius=2)
        # cabeza y casco
        pygame.draw.circle(s, (240, 201, 160), (26, 13 - subir), 10)
        pygame.draw.rect(s, (192, 200, 224), (16, 3 - subir, 20, 8), border_radius=4)
        pygame.draw.rect(s, (192, 200, 224), (24, 3 - subir, 4, 14))
        pygame.draw.circle(s, ORO, (26, 2 - subir), 3)
        # espada
        pygame.draw.rect(s, (222, 228, 240), (40, 8 - subir, 5, 30), border_radius=2)
        pygame.draw.rect(s, (138, 107, 61), (36, 36 - subir, 13, 5), border_radius=2)
        # escudo
        pygame.draw.circle(s, (212, 175, 90), (12, 32 - subir), 9)
        pygame.draw.circle(s, (150, 118, 55), (12, 32 - subir), 9, 2)
        cuadros.append(s)
    return cuadros


def frames_goblin():
    cuadros = []
    for paso in range(2):
        s = superficie(46, 48)
        alto_cuerpo = 2 if paso == 1 else 0
        verde = (111, 191, 90)
        # orejas
        pygame.draw.polygon(s, verde, [(10, 16), (0, 8), (11, 24)])
        pygame.draw.polygon(s, verde, [(36, 16), (46, 8), (35, 24)])
        pygame.draw.ellipse(s, (86, 150, 70), (11, 26 - alto_cuerpo, 24, 20))
        pygame.draw.circle(s, verde, (23, 18), 14)
        pygame.draw.circle(s, NEGRO, (18, 16), 3)
        pygame.draw.circle(s, NEGRO, (28, 16), 3)
        pygame.draw.line(s, NEGRO, (17, 25), (29, 25), 2)
        cuadros.append(s)
    return cuadros


def frames_esqueleto():
    cuadros = []
    for paso in range(2):
        s = superficie(44, 56)
        inclinacion = 1 if paso == 1 else -1
        pygame.draw.rect(s, HUESO, (17, 24, 10, 22), border_radius=3)
        for i in range(3):                                  # costillas
            pygame.draw.line(s, (150, 148, 140), (13, 28 + i * 6), (31, 28 + i * 6), 2)
        pygame.draw.circle(s, HUESO, (22, 14), 12)
        pygame.draw.circle(s, (30, 30, 36), (18, 13), 3)
        pygame.draw.circle(s, (30, 30, 36), (27, 13), 3)
        pygame.draw.line(s, (30, 30, 36), (19, 21), (26, 21), 2)
        pygame.draw.line(s, HUESO, (17, 28), (6 + inclinacion, 40), 3)   # brazos
        pygame.draw.line(s, HUESO, (27, 28), (38 - inclinacion, 40), 3)
        pygame.draw.line(s, HUESO, (19, 46), (16, 55), 3)                # piernas
        pygame.draw.line(s, HUESO, (25, 46), (28, 55), 3)
        cuadros.append(s)
    return cuadros


def frames_dragon():
    cuadros = []
    for paso in range(2):
        s = superficie(78, 66)
        abrir = 6 if paso == 1 else 0
        rojo = (224, 85, 60)
        # alas
        pygame.draw.polygon(s, (143, 51, 36),
                            [(24, 30), (2, 6 - abrir), (10, 38)])
        pygame.draw.polygon(s, (143, 51, 36),
                            [(54, 30), (76, 6 - abrir), (68, 38)])
        pygame.draw.ellipse(s, rojo, (22, 26, 34, 32))          # cuerpo
        pygame.draw.ellipse(s, rojo, (26, 6, 30, 26))           # cabeza
        pygame.draw.polygon(s, ORO, [(50, 14), (70, 18), (50, 24)])   # hocico
        pygame.draw.polygon(s, (250, 220, 120), [(28, 6), (33, -2), (36, 7)])  # cuernos
        pygame.draw.circle(s, (255, 235, 120), (42, 15), 4)
        pygame.draw.circle(s, NEGRO, (43, 15), 2)
        pygame.draw.polygon(s, (143, 51, 36), [(22, 44), (4, 58), (24, 52)])   # cola
        cuadros.append(s)
    return cuadros


def frames_jefe():
    cuadros = []
    for paso in range(2):
        s = superficie(120, 110)
        latido = 3 if paso == 1 else 0
        oscuro = (70, 22, 44)
        pygame.draw.polygon(s, oscuro, [(36, 50), (2, 4 - latido), (18, 66)])
        pygame.draw.polygon(s, oscuro, [(84, 50), (118, 4 - latido), (102, 66)])
        pygame.draw.ellipse(s, (120, 36, 70), (30, 40 - latido, 60, 60))
        pygame.draw.ellipse(s, (150, 44, 86), (36, 10 - latido, 48, 44))
        pygame.draw.polygon(s, (250, 220, 120),
                            [(38, 12 - latido), (30, -6 - latido), (48, 10 - latido)])
        pygame.draw.polygon(s, (250, 220, 120),
                            [(82, 12 - latido), (90, -6 - latido), (72, 10 - latido)])
        pygame.draw.circle(s, (255, 120, 60), (50, 28 - latido), 7)
        pygame.draw.circle(s, (255, 120, 60), (70, 28 - latido), 7)
        pygame.draw.circle(s, NEGRO, (51, 28 - latido), 3)
        pygame.draw.circle(s, NEGRO, (71, 28 - latido), 3)
        for i in range(5):                                     # dientes
            pygame.draw.polygon(s, BLANCO, [(42 + i * 8, 44 - latido),
                                            (46 + i * 8, 54 - latido),
                                            (50 + i * 8, 44 - latido)])
        cuadros.append(s)
    return cuadros


def frames_pocion():
    cuadros = []
    for paso in range(2):
        s = superficie(26, 30)
        brillo = 2 if paso == 1 else 0
        pygame.draw.rect(s, (120, 90, 60), (10, 2, 6, 6), border_radius=2)
        pygame.draw.ellipse(s, (60, 220, 150), (3, 8, 20, 20))
        pygame.draw.ellipse(s, (180, 255, 220), (8, 12 - brillo, 6, 6))
        cuadros.append(s)
    return cuadros


def crear_sprites():
    """Dibuja una sola vez todas las imágenes del juego y las guarda."""
    SPRITES["heroe"] = frames_heroe()
    SPRITES["goblin"] = frames_goblin()
    SPRITES["esqueleto"] = frames_esqueleto()
    SPRITES["dragon"] = frames_dragon()
    SPRITES["jefe"] = frames_jefe()
    SPRITES["pocion"] = frames_pocion()


# =============================================================================
#  PARTE 2 · EL SONIDO
#  Una clase chiquita que carga los .wav y los reproduce. Si la computadora no
#  tiene audio, el juego igual funciona: por eso todo está dentro de un try.
# =============================================================================

class Sonidos:

    def __init__(self):
        self.hay_audio = True
        self.efectos = {}
        try:
            pygame.mixer.init()
        except pygame.error:
            self.hay_audio = False
            return
        nombres = ["disparo", "golpe", "critico", "danio", "enemigo_muere",
                   "pocion", "subir_nivel", "boton", "victoria", "derrota"]
        for nombre in nombres:
            ruta = os.path.join(CARPETA_SONIDOS, nombre + ".wav")
            if os.path.exists(ruta):
                self.efectos[nombre] = pygame.mixer.Sound(ruta)

    def reproducir(self, nombre, volumen=0.6):
        if self.hay_audio and nombre in self.efectos:
            self.efectos[nombre].set_volume(volumen)
            self.efectos[nombre].play()

    def musica(self, encendida):
        """pygame.mixer.music es para los archivos largos: la música de fondo."""
        if not self.hay_audio:
            return
        ruta = os.path.join(CARPETA_MUSICA, "arena.wav")
        if not os.path.exists(ruta):
            return
        if encendida:
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.set_volume(0.35)
            pygame.mixer.music.play(-1)        # -1 = repetir para siempre
        else:
            pygame.mixer.music.stop()


# =============================================================================
#  PARTE 3 · LAS CLASES DEL JUEGO
#  Acá está el corazón del TP. Es el mismo árbol de clases de siempre, con dos
#  agregados: ahora los personajes tienen posición en el mapa y son sprites.
#
#      Personaje  (ES UN pygame.sprite.Sprite)
#         ├── Jugador   (TIENE UN Arma)
#         └── Enemigo
#              ├── Goblin
#              ├── Esqueleto
#              ├── Dragon
#              └── JefeFinal
# =============================================================================

class Personaje(pygame.sprite.Sprite):
    """La clase de arriba, igual que en la consola.

    NUEVO: ahora hereda de pygame.sprite.Sprite. Es la misma herencia de
    siempre, pero de una clase que nos regala una librería: gracias a eso
    podemos meter personajes en grupos y detectar choques con una sola línea.
    """

    def __init__(self, nombre, vida, x, y, cuadros):
        super().__init__()                  # ← el super() del Sprite de pygame
        self.nombre = nombre
        self.vida = vida
        self.vida_maxima = vida
        self.cuadros = cuadros              # la lista de imágenes = la animación
        self.image = cuadros[0]             # pygame necesita que se llame image
        self.rect = self.image.get_rect(center=(x, y))
        self.x = float(x)                   # posición exacta (el rect va con
        self.y = float(y)                   # números enteros y se ve a saltos)
        self.mirando_derecha = True
        self.destello = 0                   # cuadros que le quedan de "flash"
        self.empuje_x = 0.0                 # retroceso al recibir un golpe
        self.empuje_y = 0.0

    # --- lo de siempre --------------------------------------------------
    def recibir_danio(self, cantidad):
        self.vida = self.vida - cantidad
        if self.vida < 0:                   # ENCAPSULACIÓN: nunca vida negativa
            self.vida = 0
        self.destello = 8                   # NUEVO: feedback visual del golpe

    def esta_vivo(self):
        return self.vida > 0                # RETURN: lo usa todo el juego

    def porcentaje_vida(self):
        return self.vida / self.vida_maxima

    # --- lo nuevo: moverse por el mapa ----------------------------------
    def mover(self, dx, dy, obstaculos):
        """Se mueve primero en x y después en y, revisando los choques.

        Separar los dos ejes es el truco clásico: así, si chocás una pared de
        costado, podés seguir caminando pegado a ella en vez de quedar trabado.
        """
        self.x = self.x + dx
        self.rect.centerx = int(self.x)
        for muro in obstaculos:
            if self.rect.colliderect(muro):
                if dx > 0:
                    self.rect.right = muro.left
                elif dx < 0:
                    self.rect.left = muro.right
                self.x = float(self.rect.centerx)

        self.y = self.y + dy
        self.rect.centery = int(self.y)
        for muro in obstaculos:
            if self.rect.colliderect(muro):
                if dy > 0:
                    self.rect.bottom = muro.top
                elif dy < 0:
                    self.rect.top = muro.bottom
                self.y = float(self.rect.centery)

        # Que no se escape de la arena.
        # OJO con un detalle importante: el rect de pygame guarda números
        # ENTEROS, y nosotros guardamos la posición con decimales en x e y.
        # Si copiáramos el rect de vuelta a x e y, perderíamos los decimales
        # en cada cuadro y un enemigo que avanza 0,9 píxeles por cuadro no se
        # movería nunca. Por eso x e y mandan, y el rect los sigue.
        mitad_ancho = self.rect.width // 2
        mitad_alto = self.rect.height // 2
        self.x = min(max(self.x, mitad_ancho), ANCHO - mitad_ancho)
        self.y = min(max(self.y, mitad_alto), ALTO_ARENA - mitad_alto)
        self.rect.center = (int(self.x), int(self.y))

    def aplicar_empuje(self, obstaculos):
        if abs(self.empuje_x) > 0.1 or abs(self.empuje_y) > 0.1:
            self.mover(self.empuje_x, self.empuje_y, obstaculos)
            self.empuje_x = self.empuje_x * 0.82
            self.empuje_y = self.empuje_y * 0.82

    def imagen_actual(self, velocidad_animacion=180):
        """Elige qué cuadro de la animación toca ahora, mirando el reloj."""
        indice = (pygame.time.get_ticks() // velocidad_animacion) % len(self.cuadros)
        imagen = self.cuadros[indice]
        if not self.mirando_derecha:
            imagen = pygame.transform.flip(imagen, True, False)
        return imagen


class Arma:
    """La misma Arma del TP: guarda su daño y lo entrega cuando se la usa."""

    def __init__(self, nombre, danio_minimo, danio_maximo, cadencia, color):
        self.nombre = nombre
        self.danio_minimo = danio_minimo
        self.danio_maximo = danio_maximo
        self.cadencia = cadencia            # milisegundos entre disparo y disparo
        self.color = color

    def usar(self):
        return random.randint(self.danio_minimo, self.danio_maximo)

    def mejorar(self):
        # El arma sabe mejorarse sola (la pista de la etapa 10 del TP).
        self.danio_minimo = self.danio_minimo + 2
        self.danio_maximo = self.danio_maximo + 3


class Pocion:
    """La misma Pocion del TP."""

    def __init__(self, nombre, cura):
        self.nombre = nombre
        self.cura = cura

    def usar(self):
        return self.cura


class Jugador(Personaje):                   # HERENCIA: un Jugador ES UN Personaje

    def __init__(self, nombre, vida, arma, x, y):
        super().__init__(nombre, vida, x, y, SPRITES["heroe"])
        self.arma = arma                    # COMPOSICIÓN: TIENE UN arma
        self.nivel = 1
        self.experiencia = 0
        self.velocidad = 4.2
        self.ultimo_disparo = 0
        self.invulnerable_hasta = 0
        self.ultimo_golpe_fue_critico = False
        self.caminando = False

    def atacar(self):
        danio = self.arma.usar()            # le pregunta a su arma, como siempre
        self.ultimo_golpe_fue_critico = random.randint(1, 100) <= 15
        if self.ultimo_golpe_fue_critico:
            danio = danio * 2
        return danio

    def puede_disparar(self):
        return pygame.time.get_ticks() - self.ultimo_disparo >= self.arma.cadencia

    def recibir_danio(self, cantidad):
        """Sobrescribimos el método del padre para agregar los segundos de
        invulnerabilidad. super() nos deja aprovechar lo que ya hacía."""
        if pygame.time.get_ticks() < self.invulnerable_hasta:
            return False                    # todavía está protegido
        super().recibir_danio(cantidad)     # el padre resta la vida
        self.invulnerable_hasta = pygame.time.get_ticks() + 700
        return True

    def curarse(self, pocion):
        self.vida = self.vida + pocion.usar()
        if self.vida > self.vida_maxima:
            self.vida = self.vida_maxima

    def ganar_experiencia(self, cantidad):
        self.experiencia = self.experiencia + cantidad
        if self.experiencia >= 100:
            self.subir_nivel()
            return True
        return False

    def subir_nivel(self):
        self.nivel = self.nivel + 1
        self.experiencia = self.experiencia - 100
        self.vida_maxima = self.vida_maxima + 20
        self.vida = self.vida_maxima
        self.arma.mejorar()                 # el arma se encarga de mejorarse


class Enemigo(Personaje):                   # HERENCIA: un Enemigo ES UN Personaje

    def __init__(self, nombre, vida, danio, x, y, cuadros, velocidad,
                 puntos, experiencia, color):
        super().__init__(nombre, vida, x, y, cuadros)
        self.danio = danio
        self.velocidad = velocidad
        self.puntos = puntos
        self.experiencia = experiencia
        self.color = color
        self.ultimo_ataque = 0
        self.rodeando = 0          # cuadros que le quedan caminando de costado
        self.giro = 1              # hacia qué lado decidió bordear el muro

    def atacar(self):
        return self.danio

    def distancia_a(self, otro):
        return math.hypot(otro.x - self.x, otro.y - self.y)

    def perseguir(self, jugador, obstaculos, velocidad=None):
        """Camina hacia el jugador. Lo usan casi todos los enemigos."""
        if velocidad is None:
            velocidad = self.velocidad
        dx = jugador.x - self.x
        dy = jugador.y - self.y
        distancia = math.hypot(dx, dy)
        if distancia > 1:
            self.mirando_derecha = dx > 0
            paso_x = dx / distancia * velocidad
            paso_y = dy / distancia * velocidad

            # Si viene de chocarse un muro, sigue un rato de costado para
            # bordearlo. Sin esto quedaría apretado contra la columna,
            # yendo y viniendo sin avanzar nunca.
            if self.rodeando > 0:
                self.rodeando = self.rodeando - 1
                self.mover(-paso_y * self.giro, paso_x * self.giro, obstaculos)
                return

            x_antes = self.x
            y_antes = self.y
            self.mover(paso_x, paso_y, obstaculos)
            if abs(self.x - x_antes) < 0.15 and abs(self.y - y_antes) < 0.15:
                self.rodeando = 38                  # "voy a rodearlo"
                self.giro = random.choice([-1, 1])  # para un lado o para el otro

    def actualizar(self, jugador, juego):
        """Qué hace este enemigo en cada cuadro del juego.

        POLIMORFISMO: el juego llama a enemigo.actualizar() para todos por
        igual, y cada clase se comporta distinto. En el bucle no hay un solo if
        preguntando de qué tipo es cada enemigo.
        """
        self.perseguir(jugador, juego.nivel.obstaculos)


# --- LOS CUATRO ENEMIGOS ----------------------------------------------------
# Cada uno hereda todo y cambia solo lo suyo.

class Goblin(Enemigo):
    """Rápido, débil, va derecho al jugador."""

    def __init__(self, x, y):
        super().__init__("Goblin", 40, 8, x, y, SPRITES["goblin"], 2.1, 10, 20,
                         (111, 191, 90))

    def atacar(self):
        return self.danio + random.randint(0, 4)


class Esqueleto(Enemigo):
    """Mantiene la distancia y tira huesos. Pega el doble (etapa 8 del TP)."""

    def __init__(self, x, y):
        super().__init__("Esqueleto", 55, 7, x, y, SPRITES["esqueleto"], 1.5, 15,
                         25, HUESO)

    def atacar(self):
        return self.danio * 2

    def actualizar(self, jugador, juego):
        distancia = self.distancia_a(jugador)
        if distancia > 250:
            self.perseguir(jugador, juego.nivel.obstaculos)
        elif distancia < 170:
            self.perseguir(jugador, juego.nivel.obstaculos, -self.velocidad)
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_ataque > 1600 and distancia < 420:
            self.ultimo_ataque = ahora
            juego.disparo_enemigo(self, jugador, self.atacar(), HUESO, 5.0)


class Dragon(Enemigo):
    """Lento y duro. Escupe tres bolas de fuego. Pega más fuerte (+15)."""

    def __init__(self, x, y):
        super().__init__("Dragón", 120, 20, x, y, SPRITES["dragon"], 1.15, 30,
                         40, ROJO)

    def atacar(self):
        return self.danio + 15

    def actualizar(self, jugador, juego):
        self.perseguir(jugador, juego.nivel.obstaculos)
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_ataque > 2400 and self.distancia_a(jugador) < 500:
            self.ultimo_ataque = ahora
            for desvio in (-0.25, 0.0, 0.25):
                juego.disparo_enemigo(self, jugador, self.atacar(),
                                      (255, 150, 60), 4.4, desvio)


class JefeFinal(Enemigo):
    """El último rival del juego: enorme, con mucha vida y dos ataques."""

    def __init__(self, x, y):
        super().__init__("Ozmodeus, Señor de la Arena", 480, 25, x, y,
                         SPRITES["jefe"], 1.25, 200, 60, (180, 60, 100))
        self.ultimo_especial = 0

    def atacar(self):
        return self.danio + random.randint(0, 15)

    def actualizar(self, jugador, juego):
        self.perseguir(jugador, juego.nivel.obstaculos)
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_ataque > 1500:
            self.ultimo_ataque = ahora
            for desvio in (-0.35, 0.0, 0.35):
                juego.disparo_enemigo(self, jugador, self.atacar(),
                                      (255, 120, 90), 5.0, desvio)
        # ataque especial: una ronda de fuego en todas las direcciones
        if ahora - self.ultimo_especial > 5200:
            self.ultimo_especial = ahora
            juego.sacudir(10)
            for i in range(14):
                angulo = i * (2 * math.pi / 14)
                juego.disparo_en_angulo(self, angulo, self.danio, VIOLETA, 3.6)


# =============================================================================
#  PARTE 4 · LAS COSAS QUE VUELAN Y BRILLAN
# =============================================================================

class Proyectil(pygame.sprite.Sprite):
    """Un disparo. También es un Sprite, para poder usar los grupos y las
    colisiones de pygame."""

    def __init__(self, x, y, dx, dy, danio, color, radio=7, de_quien="jugador"):
        super().__init__()
        self.image = superficie(radio * 2 + 8, radio * 2 + 8)
        pygame.draw.circle(self.image, color, (radio + 4, radio + 4), radio)
        pygame.draw.circle(self.image, BLANCO, (radio + 2, radio + 2),
                           max(2, radio // 3))
        self.rect = self.image.get_rect(center=(int(x), int(y)))
        self.x = float(x)
        self.y = float(y)
        self.dx = dx
        self.dy = dy
        self.danio = danio                  # el número que devolvió atacar()
        self.color = color
        self.de_quien = de_quien
        self.critico = False
        self.nacio = pygame.time.get_ticks()

    def actualizar(self, obstaculos):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.center = (int(self.x), int(self.y))
        if (self.x < -20 or self.x > ANCHO + 20 or
                self.y < -20 or self.y > ALTO_ARENA + 20):
            self.kill()                     # kill() lo saca de todos los grupos
            return
        for muro in obstaculos:
            if self.rect.colliderect(muro):
                self.kill()
                return


class Particula:
    """Un pedacito de color que sale volando cuando algo explota."""

    def __init__(self, x, y, color, fuerza=4.0, vida=26, tamanio=4):
        angulo = random.uniform(0, 2 * math.pi)
        rapidez = random.uniform(1.0, fuerza)
        self.x = x
        self.y = y
        self.dx = math.cos(angulo) * rapidez
        self.dy = math.sin(angulo) * rapidez
        self.color = color
        self.vida = vida
        self.vida_inicial = vida
        self.tamanio = tamanio

    def actualizar(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.dx = self.dx * 0.94
        self.dy = self.dy * 0.94 + 0.12     # un poquito de gravedad
        self.vida = self.vida - 1

    def dibujar(self, destino):
        if self.vida <= 0:
            return
        proporcion = self.vida / self.vida_inicial
        radio = max(1, int(self.tamanio * proporcion))
        pygame.draw.circle(destino, self.color, (int(self.x), int(self.y)), radio)


class NumeroFlotante:
    """El "-25" que sube y se desvanece arriba del que recibió el golpe."""

    def __init__(self, x, y, texto, color, tamanio=22):
        self.x = x
        self.y = y
        self.texto = texto
        self.color = color
        self.tamanio = tamanio
        self.vida = 45

    def actualizar(self):
        self.y = self.y - 1.1
        self.vida = self.vida - 1


class ObjetoEnElSuelo(pygame.sprite.Sprite):
    """Una poción tirada en el piso, esperando que alguien la levante.

    Fijate que TIENE UNA Pocion adentro: composición otra vez. El objeto del
    suelo se encarga de aparecer y de flotar; la poción, de saber cuánto cura.
    """

    def __init__(self, x, y, pocion):
        super().__init__()
        self.pocion = pocion
        self.cuadros = SPRITES["pocion"]
        self.image = self.cuadros[0]
        self.rect = self.image.get_rect(center=(int(x), int(y)))
        self.y_base = y
        self.nacio = pygame.time.get_ticks()

    def imagen_actual(self):
        indice = (pygame.time.get_ticks() // 260) % len(self.cuadros)
        return self.cuadros[indice]

    def altura_flotante(self):
        # sube y baja suavemente usando el reloj del juego
        return math.sin(pygame.time.get_ticks() / 260.0) * 5


# =============================================================================
#  PARTE 5 · EL MAPA
#  Cada nivel es un objeto con su propio color, sus obstáculos y sus oleadas
#  de enemigos. Agregar un nivel nuevo es agregar un Nivel más a la lista.
# =============================================================================

class Nivel:

    def __init__(self, numero, nombre, lema, color_fondo, color_piso,
                 color_detalle, color_muro, obstaculos, oleadas):
        self.numero = numero
        self.nombre = nombre
        self.lema = lema
        self.color_fondo = color_fondo
        self.color_piso = color_piso
        self.color_detalle = color_detalle
        self.color_muro = color_muro
        self.obstaculos = obstaculos          # lista de pygame.Rect
        self.oleadas = oleadas                # lista de listas de clases
        self.fondo = self.dibujar_fondo()     # se dibuja UNA sola vez

    def dibujar_fondo(self):
        """Dibuja el escenario completo en una superficie.

        Se hace una vez y después se pega entera en cada cuadro. Dibujar 300
        piedritas 60 veces por segundo sería un desperdicio: esto es lo mismo
        que hacer la escenografía antes de que empiece la obra.
        """
        fondo = pygame.Surface((ANCHO, ALTO_ARENA))
        fondo.fill(self.color_fondo)

        # baldosas del piso
        for x in range(0, ANCHO, 64):
            for y in range(0, ALTO_ARENA, 64):
                pygame.draw.rect(fondo, self.color_piso, (x, y, 64, 64), 1)

        # detalles al azar (piedritas, cristales, grietas)
        generador = random.Random(self.numero * 7)   # siempre los mismos
        for _ in range(140):
            x = generador.randint(0, ANCHO)
            y = generador.randint(0, ALTO_ARENA)
            radio = generador.randint(1, 4)
            pygame.draw.circle(fondo, self.color_detalle, (x, y), radio)

        # los obstáculos, con un poco de relieve
        for muro in self.obstaculos:
            sombra = muro.move(4, 6)
            pygame.draw.rect(fondo, (0, 0, 0), sombra, border_radius=8)
            pygame.draw.rect(fondo, self.color_muro, muro, border_radius=8)
            pygame.draw.rect(fondo, self.color_detalle, muro, 3, border_radius=8)
            brillo = pygame.Rect(muro.x + 8, muro.y + 6, muro.width - 16, 6)
            pygame.draw.rect(fondo, self.color_piso, brillo, border_radius=3)

        return fondo


def crear_niveles():
    """Los tres escenarios del juego, de menor a mayor dificultad."""
    nivel_1 = Nivel(
        1, "LA ARENA DE PIEDRA", "Donde todos empiezan",
        (42, 36, 48), (59, 50, 66), (85, 72, 95), (74, 63, 85),
        [pygame.Rect(200, 110, 80, 80), pygame.Rect(744, 110, 80, 80),
         pygame.Rect(200, 372, 80, 80), pygame.Rect(744, 372, 80, 80),
         pygame.Rect(374, 246, 72, 72), pygame.Rect(578, 246, 72, 72)],
        [[Goblin] * 4,
         [Goblin] * 6,
         [Goblin] * 4 + [Esqueleto] * 2])

    nivel_2 = Nivel(
        2, "EL BOSQUE HELADO", "El frío también duele",
        (24, 42, 56), (34, 59, 77), (47, 84, 104), (53, 96, 122),
        [pygame.Rect(120, 90, 190, 44), pygame.Rect(714, 90, 190, 44),
         pygame.Rect(120, 428, 190, 44), pygame.Rect(714, 428, 190, 44),
         pygame.Rect(492, 118, 44, 108), pygame.Rect(492, 336, 44, 108)],
        [[Esqueleto] * 3 + [Goblin] * 3,
         [Esqueleto] * 4 + [Goblin] * 4,
         [Dragon] * 1 + [Esqueleto] * 3])

    nivel_3 = Nivel(
        3, "LA GUARIDA DEL DRAGÓN", "El último rival te espera",
        (43, 20, 32), (61, 28, 36), (110, 45, 40), (92, 40, 38),
        [pygame.Rect(150, 150, 96, 96), pygame.Rect(778, 150, 96, 96),
         pygame.Rect(150, 316, 96, 96), pygame.Rect(778, 316, 96, 96),
         pygame.Rect(452, 40, 120, 46), pygame.Rect(452, 476, 120, 46)],
        [[Dragon] * 2 + [Goblin] * 4,
         [Dragon] * 2 + [Esqueleto] * 4,
         [JefeFinal]])

    return [nivel_1, nivel_2, nivel_3]


# =============================================================================
#  PARTE 6 · EL JUEGO
#  Esta clase es la que arma la ventana, escucha el teclado y el mouse, y
#  dibuja. No calcula daño: eso lo siguen haciendo el Jugador y los Enemigos.
# =============================================================================

class Juego:

    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Arena de Combate · POO + Pygame")
        self.reloj = pygame.time.Clock()           # para los FPS
        self.corriendo = True

        crear_sprites()
        self.sonidos = Sonidos()

        self.fuente_titulo = pygame.font.SysFont("menlo,consolas,dejavusansmono,monospace", 60, bold=True)
        self.fuente_grande = pygame.font.SysFont("menlo,consolas,dejavusansmono,monospace", 30, bold=True)
        self.fuente_media = pygame.font.SysFont("menlo,consolas,dejavusansmono,monospace", 20, bold=True)
        self.fuente_chica = pygame.font.SysFont("menlo,consolas,dejavusansmono,monospace", 15)
        self.fuente_mini = pygame.font.SysFont("menlo,consolas,dejavusansmono,monospace", 12)

        # la arena se dibuja en su propia superficie: así podemos sacudirla
        self.arena = pygame.Surface((ANCHO, ALTO_ARENA))

        self.estado = "menu"                       # menu · controles · jugando
        self.opcion_menu = 0                       # pausa · transicion
        self.opciones_menu = ["JUGAR", "CÓMO SE JUEGA", "SALIR"]
        self.rectangulos_menu = []
        self.estrellas = [[random.randint(0, ANCHO), random.randint(0, ALTO),
                           random.uniform(0.2, 0.9)] for _ in range(70)]

        self.niveles = crear_niveles()
        self.nivel = self.niveles[0]
        self.heroe = None
        self.sacudida = 0
        self.tinte_rojo = 0
        self.mensaje = ""
        self.mensaje_hasta = 0
        self.sonidos.musica(True)

    # =====================================================================
    #  ARRANQUE DE PARTIDA
    # =====================================================================
    def nueva_partida(self):
        espada = Arma("Espada de acero", 14, 22, 260, ORO)
        self.heroe = Jugador("Aria", 120, espada, ANCHO // 2, ALTO_ARENA // 2)

        self.enemigos = pygame.sprite.Group()          # GRUPOS de pygame
        self.proyectiles_jugador = pygame.sprite.Group()
        self.proyectiles_enemigos = pygame.sprite.Group()
        self.objetos = pygame.sprite.Group()
        self.particulas = []
        self.numeros = []

        self.puntaje = 0
        self.enemigos_vencidos = 0
        self.indice_nivel = 0
        self.golpe_mas_fuerte = 0
        self.momento_inicio = pygame.time.get_ticks()
        self.empezar_nivel(0)

    def empezar_nivel(self, indice):
        self.indice_nivel = indice
        self.nivel = self.niveles[indice]
        self.enemigos.empty()
        self.proyectiles_jugador.empty()
        self.proyectiles_enemigos.empty()
        self.objetos.empty()
        self.numero_oleada = 0
        self.heroe.x, self.heroe.y = ANCHO // 2, ALTO_ARENA // 2
        self.heroe.rect.center = (ANCHO // 2, ALTO_ARENA // 2)
        self.estado = "transicion"
        self.transicion_hasta = pygame.time.get_ticks() + 2400

    def lanzar_oleada(self):
        """Hace aparecer la próxima tanda de enemigos repartidos por el mapa."""
        oleada = self.nivel.oleadas[self.numero_oleada]
        for clase_de_enemigo in oleada:
            # Acá se ve el polimorfismo desde otro ángulo: la lista guarda
            # CLASES, y todas se crean igual, con (x, y).
            enemigo = clase_de_enemigo(0, 0)
            # Recién ahora sabemos cuánto ocupa: el jefe es enorme y necesita
            # un lugar más grande que un goblin para no aparecer encajado.
            x, y = self.lugar_libre(enemigo.rect.width, enemigo.rect.height)
            enemigo.x = float(x)
            enemigo.y = float(y)
            enemigo.rect.center = (x, y)
            self.enemigos.add(enemigo)
            for _ in range(14):
                self.particulas.append(Particula(x, y, enemigo.color, 5.0, 24))
        self.numero_oleada = self.numero_oleada + 1
        self.avisar("OLEADA " + str(self.numero_oleada) + " DE " +
                    str(len(self.nivel.oleadas)))

    def lugar_libre(self, ancho=60, alto=60):
        """Busca dónde hacer aparecer un enemigo de ese tamaño: lejos del
        jugador y sin que quede encajado en un muro."""
        margen_x = ancho // 2 + 20
        margen_y = alto // 2 + 20

        # 1) probamos lugares al azar, lejos del jugador
        for intento in range(200):
            # si después de 100 intentos no encontró, se conforma con menos
            # distancia: el jefe es grande y le entran pocos lugares.
            distancia_minima = 280 if intento < 100 else 170
            x = random.randint(margen_x, ANCHO - margen_x)
            y = random.randint(margen_y, ALTO_ARENA - margen_y)
            if math.hypot(x - self.heroe.x, y - self.heroe.y) < distancia_minima:
                continue
            if self.hay_lugar(x, y, ancho, alto):
                return x, y

        # 2) si el azar no encontró nada, recorremos el mapa en orden
        for y in range(margen_y, ALTO_ARENA - margen_y, 20):
            for x in range(margen_x, ANCHO - margen_x, 20):
                if self.hay_lugar(x, y, ancho, alto):
                    return x, y
        return ANCHO // 2, margen_y

    def hay_lugar(self, x, y, ancho, alto):
        """¿Entra algo de ese tamaño en ese punto sin tocar ningún muro?"""
        zona = pygame.Rect(0, 0, ancho + 16, alto + 16)
        zona.center = (x, y)
        return zona.collidelist(self.nivel.obstaculos) == -1

    def avisar(self, texto, milisegundos=1600):
        self.mensaje = texto
        self.mensaje_hasta = pygame.time.get_ticks() + milisegundos

    def sacudir(self, fuerza):
        self.sacudida = max(self.sacudida, fuerza)

    # =====================================================================
    #  ATAQUES
    # =====================================================================
    def disparo_jugador(self, punto=None):
        """Dispara hacia un punto de la arena. Si no le pasamos ninguno,
        dispara hacia donde está el mouse."""
        if punto is None:
            raton_x, raton_y = pygame.mouse.get_pos()
            punto = (raton_x, raton_y - ALTO_HUD)
        dx = punto[0] - self.heroe.x
        dy = punto[1] - self.heroe.y
        distancia = math.hypot(dx, dy)
        if distancia < 1:
            return
        self.heroe.mirando_derecha = dx > 0
        self.heroe.ultimo_disparo = pygame.time.get_ticks()

        # ¡LA LÍNEA DE SIEMPRE! El jugador le pide el daño a su arma.
        danio = self.heroe.atacar()
        if danio > self.golpe_mas_fuerte:
            self.golpe_mas_fuerte = danio

        critico = self.heroe.ultimo_golpe_fue_critico
        color = (255, 240, 180) if critico else self.heroe.arma.color
        radio = 11 if critico else 7
        velocidad = 11.0
        proyectil = Proyectil(self.heroe.x, self.heroe.y,
                              dx / distancia * velocidad,
                              dy / distancia * velocidad,
                              danio, color, radio, "jugador")
        proyectil.critico = critico
        self.proyectiles_jugador.add(proyectil)
        self.sonidos.reproducir("critico" if critico else "disparo", 0.4)

    def disparo_enemigo(self, enemigo, jugador, danio, color, velocidad, desvio=0.0):
        dx = jugador.x - enemigo.x
        dy = jugador.y - enemigo.y
        angulo = math.atan2(dy, dx) + desvio
        self.disparo_en_angulo(enemigo, angulo, danio, color, velocidad)

    def disparo_en_angulo(self, enemigo, angulo, danio, color, velocidad):
        proyectil = Proyectil(enemigo.x, enemigo.y,
                              math.cos(angulo) * velocidad,
                              math.sin(angulo) * velocidad,
                              danio, color, 8, "enemigo")
        self.proyectiles_enemigos.add(proyectil)

    def golpear_enemigo(self, enemigo, danio, critico=False):
        if not enemigo.esta_vivo():
            # Puede pasar que dos disparos lleguen en el mismo cuadro: sin este
            # if, el enemigo se contaría dos veces como derrotado.
            return
        enemigo.recibir_danio(danio)                 # el método de siempre
        self.numeros.append(NumeroFlotante(enemigo.x, enemigo.y - 30,
                                           ("¡" + str(danio) + "!") if critico
                                           else str(danio),
                                           ORO if critico else BLANCO,
                                           26 if critico else 20))
        for _ in range(8 if not critico else 16):
            self.particulas.append(Particula(enemigo.x, enemigo.y, enemigo.color))
        self.sonidos.reproducir("golpe", 0.35)

        if not enemigo.esta_vivo():                  # esta_vivo() otra vez
            self.enemigo_derrotado(enemigo)

    def enemigo_derrotado(self, enemigo):
        for _ in range(30):
            self.particulas.append(Particula(enemigo.x, enemigo.y, enemigo.color,
                                             6.5, 40, 6))
        self.puntaje = self.puntaje + enemigo.puntos
        self.enemigos_vencidos = self.enemigos_vencidos + 1
        self.sonidos.reproducir("enemigo_muere", 0.45)
        self.sacudir(6)

        if self.heroe.ganar_experiencia(enemigo.experiencia):
            self.sonidos.reproducir("subir_nivel", 0.6)
            self.avisar("¡NIVEL " + str(self.heroe.nivel) + "!  Arma mejorada")
            for _ in range(40):
                self.particulas.append(Particula(self.heroe.x, self.heroe.y,
                                                 VIOLETA, 7.0, 45, 5))

        # el enemigo puede soltar una poción (la idea de random de la clase 3)
        if random.randint(1, 100) <= 28:
            self.objetos.add(ObjetoEnElSuelo(enemigo.x, enemigo.y,
                                             Pocion("Poción", 35)))
        enemigo.kill()                    # lo saca de todos los grupos

    # =====================================================================
    #  EL BUCLE PRINCIPAL
    #  Todo videojuego hace siempre lo mismo, muchas veces por segundo:
    #      1. escuchar     2. actualizar     3. dibujar
    # =====================================================================
    def jugar(self):
        while self.corriendo:
            self.reloj.tick(FPS)          # no más de 60 cuadros por segundo
            self.escuchar_eventos()
            self.actualizar()
            self.dibujar()
        pygame.quit()

    # ------------------------------------------------------------- 1. escuchar
    def escuchar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.corriendo = False

            elif evento.type == pygame.KEYDOWN:
                self.tecla_apretada(evento.key)

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.estado == "menu":
                    self.clic_en_el_menu(evento.pos)
                elif self.estado == "controles":
                    self.estado = "menu"
                elif self.estado == "jugando" and self.heroe.puede_disparar():
                    self.disparo_jugador()

        # el teclado sostenido se consulta aparte (movimiento continuo)
        if self.estado == "jugando":
            self.mover_al_heroe()
            teclas = pygame.key.get_pressed()
            botones = pygame.mouse.get_pressed()
            if (teclas[pygame.K_SPACE] or botones[0]) and self.heroe.puede_disparar():
                self.disparo_jugador()

    def tecla_apretada(self, tecla):
        if self.estado == "menu":
            if tecla in (pygame.K_DOWN, pygame.K_s):
                self.opcion_menu = (self.opcion_menu + 1) % len(self.opciones_menu)
                self.sonidos.reproducir("boton", 0.3)
            elif tecla in (pygame.K_UP, pygame.K_w):
                self.opcion_menu = (self.opcion_menu - 1) % len(self.opciones_menu)
                self.sonidos.reproducir("boton", 0.3)
            elif tecla in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                self.elegir_opcion_del_menu()
            elif tecla == pygame.K_ESCAPE:
                self.corriendo = False

        elif self.estado == "controles":
            self.estado = "menu"

        elif self.estado == "jugando":
            if tecla in (pygame.K_ESCAPE, pygame.K_p):
                self.estado = "pausa"

        elif self.estado == "pausa":
            if tecla in (pygame.K_ESCAPE, pygame.K_p):
                self.estado = "jugando"
            elif tecla == pygame.K_m:
                self.estado = "menu"

        elif self.estado in ("victoria", "derrota"):
            if tecla == pygame.K_r:
                self.nueva_partida()
            elif tecla == pygame.K_m:
                self.estado = "menu"
            elif tecla == pygame.K_ESCAPE:
                self.corriendo = False

    def clic_en_el_menu(self, posicion):
        for numero in range(len(self.rectangulos_menu)):
            if self.rectangulos_menu[numero].collidepoint(posicion):
                self.opcion_menu = numero
                self.elegir_opcion_del_menu()

    def elegir_opcion_del_menu(self):
        self.sonidos.reproducir("boton", 0.5)
        if self.opcion_menu == 0:
            self.nueva_partida()
        elif self.opcion_menu == 1:
            self.estado = "controles"
        else:
            self.corriendo = False

    def mover_al_heroe(self):
        teclas = pygame.key.get_pressed()
        dx = 0.0
        dy = 0.0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx = dx - 1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx = dx + 1
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy = dy - 1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy = dy + 1
        if dx != 0 and dy != 0:               # en diagonal no se va más rápido
            dx = dx * 0.7071
            dy = dy * 0.7071
        if dx != 0 or dy != 0:
            self.heroe.mover(dx * self.heroe.velocidad, dy * self.heroe.velocidad,
                             self.nivel.obstaculos)
            self.heroe.caminando = True
        else:
            self.heroe.caminando = False

    # ----------------------------------------------------------- 2. actualizar
    def actualizar(self):
        # efectos que siguen andando en cualquier pantalla
        for estrella in self.estrellas:
            estrella[1] = estrella[1] + estrella[2]
            if estrella[1] > ALTO:
                estrella[1] = 0
                estrella[0] = random.randint(0, ANCHO)

        if self.sacudida > 0:
            self.sacudida = self.sacudida - 1
        if self.tinte_rojo > 0:
            self.tinte_rojo = self.tinte_rojo - 6

        if self.estado == "transicion":
            if pygame.time.get_ticks() >= self.transicion_hasta:
                self.estado = "jugando"
                self.lanzar_oleada()
            return

        if self.estado != "jugando":
            return

        # --- los enemigos piensan (polimorfismo: ni un solo if acá) ---
        for enemigo in self.enemigos:
            enemigo.actualizar(self.heroe, self)
            enemigo.aplicar_empuje(self.nivel.obstaculos)
            if enemigo.destello > 0:
                enemigo.destello = enemigo.destello - 1

        # --- los proyectiles vuelan ---
        for proyectil in list(self.proyectiles_jugador):
            proyectil.actualizar(self.nivel.obstaculos)
        for proyectil in list(self.proyectiles_enemigos):
            proyectil.actualizar(self.nivel.obstaculos)

        # --- COLISIONES ---
        # 1) mis disparos contra los enemigos
        choques = pygame.sprite.groupcollide(self.proyectiles_jugador,
                                             self.enemigos, True, False)
        for proyectil, tocados in choques.items():
            enemigo = tocados[0]
            empuje = math.hypot(proyectil.dx, proyectil.dy)
            if empuje > 0:
                enemigo.empuje_x = proyectil.dx / empuje * 7
                enemigo.empuje_y = proyectil.dy / empuje * 7
            self.golpear_enemigo(enemigo, proyectil.danio, proyectil.critico)

        # 2) los disparos enemigos contra mí
        recibidos = pygame.sprite.spritecollide(self.heroe,
                                                self.proyectiles_enemigos, True)
        for proyectil in recibidos:
            self.danio_al_heroe(proyectil.danio)

        # 3) los enemigos que me tocan (daño por contacto)
        for enemigo in pygame.sprite.spritecollide(self.heroe, self.enemigos, False):
            self.danio_al_heroe(enemigo.atacar())    # polimorfismo otra vez

        # 4) las pociones tiradas en el piso
        for objeto in pygame.sprite.spritecollide(self.heroe, self.objetos, True):
            vida_antes = self.heroe.vida
            self.heroe.curarse(objeto.pocion)        # el método de siempre
            curado = self.heroe.vida - vida_antes
            self.numeros.append(NumeroFlotante(self.heroe.x, self.heroe.y - 40,
                                               "+" + str(curado), VERDE))
            self.sonidos.reproducir("pocion", 0.5)

        # --- partículas y números flotantes ---
        vivas = []
        for particula in self.particulas:
            particula.actualizar()
            if particula.vida > 0:
                vivas.append(particula)
        self.particulas = vivas

        vivos = []
        for numero in self.numeros:
            numero.actualizar()
            if numero.vida > 0:
                vivos.append(numero)
        self.numeros = vivos

        # --- ¿se terminó la oleada, el nivel o la partida? ---
        if not self.heroe.esta_vivo():
            self.terminar(False)
            return

        if len(self.enemigos) == 0:
            if self.numero_oleada < len(self.nivel.oleadas):
                self.lanzar_oleada()
            elif self.indice_nivel + 1 < len(self.niveles):
                self.avisar("¡NIVEL SUPERADO!")
                self.empezar_nivel(self.indice_nivel + 1)
            else:
                self.terminar(True)

    def danio_al_heroe(self, cantidad):
        if self.heroe.recibir_danio(cantidad):       # devuelve False si estaba
            self.sacudir(9)                          # invulnerable
            self.tinte_rojo = 90
            self.sonidos.reproducir("danio", 0.5)
            self.numeros.append(NumeroFlotante(self.heroe.x, self.heroe.y - 40,
                                               "-" + str(cantidad), ROJO))
            for _ in range(10):
                self.particulas.append(Particula(self.heroe.x, self.heroe.y, ROJO))

    def terminar(self, gano):
        self.estado = "victoria" if gano else "derrota"
        self.segundos_jugados = (pygame.time.get_ticks() - self.momento_inicio) // 1000
        self.sonidos.reproducir("victoria" if gano else "derrota", 0.7)

    # -------------------------------------------------------------- 3. dibujar
    def texto(self, destino, texto, x, y, fuente, color, centrado=False):
        imagen = fuente.render(texto, True, color)
        if centrado:
            destino.blit(imagen, imagen.get_rect(center=(x, y)))
        else:
            destino.blit(imagen, (x, y))
        return imagen.get_rect()

    def barra(self, destino, x, y, ancho, alto, proporcion, color):
        pygame.draw.rect(destino, GRIS_OSCURO, (x, y, ancho, alto), border_radius=alto // 2)
        relleno = int(ancho * max(0.0, min(1.0, proporcion)))
        if relleno > alto:
            pygame.draw.rect(destino, color, (x, y, relleno, alto),
                             border_radius=alto // 2)

    def dibujar(self):
        pygame.mouse.set_visible(self.estado != "jugando")

        if self.estado == "menu":
            self.dibujar_menu()
        elif self.estado == "controles":
            self.dibujar_controles()
        elif self.estado == "transicion":
            self.dibujar_transicion()
        elif self.estado in ("jugando", "pausa"):
            self.dibujar_partida()
            if self.estado == "pausa":
                self.dibujar_pausa()
        else:
            self.dibujar_final(self.estado == "victoria")

        pygame.display.flip()             # mostrar todo lo dibujado

    # ------------------------------------------------------------------ menú
    def dibujar_fondo_estrellado(self):
        self.pantalla.fill(NEGRO)
        for x, y, velocidad in self.estrellas:
            brillo = int(90 + velocidad * 120)
            pygame.draw.circle(self.pantalla, (brillo, brillo, brillo + 20),
                               (int(x), int(y)), 1 if velocidad < 0.6 else 2)

    def dibujar_menu(self):
        self.dibujar_fondo_estrellado()
        tiempo = pygame.time.get_ticks()

        # personajes de adorno, como en la portada de un juego
        self.pantalla.blit(pygame.transform.scale(SPRITES["dragon"][(tiempo // 400) % 2],
                                                  (156, 132)), (760, 400))
        self.pantalla.blit(pygame.transform.scale(SPRITES["goblin"][(tiempo // 300) % 2],
                                                  (92, 96)), (130, 440))
        self.pantalla.blit(pygame.transform.scale(SPRITES["heroe"][(tiempo // 350) % 2],
                                                  (104, 120)), (450, 410))

        flotar = math.sin(tiempo / 400.0) * 6
        self.texto(self.pantalla, "ARENA DE COMBATE", ANCHO // 2, 130 + flotar,
                   self.fuente_titulo, ORO, True)
        self.texto(self.pantalla, "Versión 3 · el mismo TP, hecho videojuego",
                   ANCHO // 2, 180 + flotar, self.fuente_chica, GRIS, True)

        raton = pygame.mouse.get_pos()
        self.rectangulos_menu = []
        for numero in range(len(self.opciones_menu)):
            y = 250 + numero * 56
            caja = pygame.Rect(ANCHO // 2 - 170, y - 22, 340, 44)
            self.rectangulos_menu.append(caja)
            if caja.collidepoint(raton):
                self.opcion_menu = numero
            elegida = (numero == self.opcion_menu)
            if elegida:
                pygame.draw.rect(self.pantalla, (28, 34, 52), caja, border_radius=10)
                pygame.draw.rect(self.pantalla, ORO, caja, 2, border_radius=10)
            self.texto(self.pantalla, self.opciones_menu[numero], ANCHO // 2, y,
                       self.fuente_grande, ORO if elegida else GRIS, True)

        self.texto(self.pantalla,
                   "Flechas o mouse para elegir  ·  ENTER o clic para confirmar",
                   ANCHO // 2, ALTO - 42, self.fuente_chica, GRIS, True)
        self.texto(self.pantalla,
                   "Mismas clases que juego_consola.py: Personaje · Jugador · "
                   "Enemigo · Arma · Pocion",
                   ANCHO // 2, ALTO - 20, self.fuente_mini, (70, 78, 98), True)

    def dibujar_controles(self):
        self.dibujar_fondo_estrellado()
        self.texto(self.pantalla, "CÓMO SE JUEGA", ANCHO // 2, 90,
                   self.fuente_grande, ORO, True)
        lineas = [
            ("W A S D  /  flechas", "mover a tu personaje por la arena"),
            ("mouse", "apuntar hacia donde querés atacar"),
            ("clic  /  barra espaciadora", "atacar con tu arma"),
            ("P  /  ESC", "pausa"),
            ("", ""),
            ("Objetivo", "superá las oleadas de los 3 niveles y venc al jefe final"),
            ("Pociones", "las sueltan los enemigos: pasá por encima para curarte"),
            ("Experiencia", "cada enemigo te da EXP; al llegar a 100 subís de nivel"),
            ("Al subir de nivel", "más vida máxima y el arma se mejora sola"),
        ]
        y = 160
        for izquierda, derecha in lineas:
            if izquierda != "":
                self.texto(self.pantalla, izquierda, 210, y, self.fuente_media, BLANCO)
                self.texto(self.pantalla, derecha, 480, y + 3, self.fuente_chica, GRIS)
            y = y + 38
        self.texto(self.pantalla, "tocá cualquier tecla para volver", ANCHO // 2,
                   ALTO - 50, self.fuente_chica, ORO, True)

    # ------------------------------------------------------------- transición
    def dibujar_transicion(self):
        self.pantalla.fill(self.nivel.color_fondo)
        falta = self.transicion_hasta - pygame.time.get_ticks()
        aparicion = min(1.0, max(0.0, (2400 - falta) / 500.0))
        aparicion = min(aparicion, max(0.0, falta / 500.0))

        capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        self.texto(capa, "NIVEL " + str(self.nivel.numero), ANCHO // 2, ALTO // 2 - 70,
                   self.fuente_grande, GRIS, True)
        self.texto(capa, self.nivel.nombre, ANCHO // 2, ALTO // 2,
                   self.fuente_titulo, ORO, True)
        self.texto(capa, self.nivel.lema, ANCHO // 2, ALTO // 2 + 60,
                   self.fuente_media, BLANCO, True)
        capa.set_alpha(int(255 * aparicion))
        self.pantalla.blit(capa, (0, 0))

    # ----------------------------------------------------------- la partida
    def dibujar_partida(self):
        arena = self.arena
        arena.blit(self.nivel.fondo, (0, 0))          # la escenografía, entera

        # pociones en el piso
        for objeto in self.objetos:
            imagen = objeto.imagen_actual()
            arena.blit(imagen, (objeto.rect.x, objeto.rect.y +
                                objeto.altura_flotante()))

        # partículas de atrás
        for particula in self.particulas:
            particula.dibujar(arena)

        # enemigos, con su barrita de vida
        for enemigo in self.enemigos:
            imagen = enemigo.imagen_actual(220)
            if enemigo.destello > 0:
                imagen = imagen.copy()
                imagen.fill((110, 110, 110), special_flags=pygame.BLEND_RGB_ADD)
            arena.blit(imagen, imagen.get_rect(center=enemigo.rect.center))
            if not isinstance(enemigo, JefeFinal):
                ancho = enemigo.rect.width
                self.barra(arena, enemigo.rect.centerx - ancho // 2,
                           enemigo.rect.top - 12, ancho, 5,
                           enemigo.porcentaje_vida(), ROJO)

        # proyectiles
        for proyectil in self.proyectiles_jugador:
            arena.blit(proyectil.image, proyectil.rect)
        for proyectil in self.proyectiles_enemigos:
            arena.blit(proyectil.image, proyectil.rect)

        # el héroe (parpadea mientras es invulnerable)
        parpadeo = (pygame.time.get_ticks() // 70) % 2 == 0
        protegido = pygame.time.get_ticks() < self.heroe.invulnerable_hasta
        if not protegido or parpadeo:
            velocidad_animacion = 150 if self.heroe.caminando else 400
            imagen = self.heroe.imagen_actual(velocidad_animacion)
            arena.blit(imagen, imagen.get_rect(center=self.heroe.rect.center))

        # números de daño
        for numero in self.numeros:
            fuente = self.fuente_media if numero.tamanio < 24 else self.fuente_grande
            imagen = fuente.render(numero.texto, True, numero.color)
            imagen.set_alpha(min(255, numero.vida * 8))
            arena.blit(imagen, imagen.get_rect(center=(int(numero.x), int(numero.y))))

        # la arena se pega en la ventana, temblando si hubo un golpe fuerte
        temblor_x = random.randint(-self.sacudida, self.sacudida) if self.sacudida else 0
        temblor_y = random.randint(-self.sacudida, self.sacudida) if self.sacudida else 0
        self.pantalla.fill(NEGRO)
        self.pantalla.blit(arena, (temblor_x, ALTO_HUD + temblor_y))

        self.dibujar_hud()

        # tinte rojo cuando nos pegan
        if self.tinte_rojo > 0:
            capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            capa.fill((200, 40, 40, self.tinte_rojo))
            self.pantalla.blit(capa, (0, 0))

        # mira del mouse
        raton = pygame.mouse.get_pos()
        pygame.draw.circle(self.pantalla, ORO, raton, 11, 2)
        pygame.draw.line(self.pantalla, ORO, (raton[0] - 16, raton[1]),
                         (raton[0] - 5, raton[1]), 2)
        pygame.draw.line(self.pantalla, ORO, (raton[0] + 5, raton[1]),
                         (raton[0] + 16, raton[1]), 2)

        if pygame.time.get_ticks() < self.mensaje_hasta:
            self.texto(self.pantalla, self.mensaje, ANCHO // 2, ALTO_HUD + 40,
                       self.fuente_grande, ORO, True)

    def dibujar_hud(self):
        pygame.draw.rect(self.pantalla, (18, 21, 32), (0, 0, ANCHO, ALTO_HUD))
        pygame.draw.line(self.pantalla, GRIS_OSCURO, (0, ALTO_HUD), (ANCHO, ALTO_HUD), 2)

        # vida y experiencia del héroe
        self.texto(self.pantalla, self.heroe.nombre, 20, 10, self.fuente_media, BLANCO)
        self.texto(self.pantalla, "Nv " + str(self.heroe.nivel), 20, 52,
                   self.fuente_chica, ORO)
        self.barra(self.pantalla, 20, 34, 280, 14, self.heroe.porcentaje_vida(), VERDE)
        self.texto(self.pantalla, str(self.heroe.vida) + " / " +
                   str(self.heroe.vida_maxima), 160, 33, self.fuente_mini, BLANCO, True)
        self.barra(self.pantalla, 70, 54, 230, 8, self.heroe.experiencia / 100.0,
                   VIOLETA)

        # nivel y oleada
        self.texto(self.pantalla, self.nivel.nombre, ANCHO // 2, 20,
                   self.fuente_media, BLANCO, True)
        self.texto(self.pantalla, "Oleada " + str(self.numero_oleada) + " de " +
                   str(len(self.nivel.oleadas)) + "   ·   Enemigos: " +
                   str(len(self.enemigos)), ANCHO // 2, 46, self.fuente_chica,
                   GRIS, True)

        # puntaje
        self.texto(self.pantalla, "PUNTAJE", ANCHO - 330, 12, self.fuente_mini, GRIS)
        self.texto(self.pantalla, str(self.puntaje), ANCHO - 330, 30,
                   self.fuente_grande, ORO)

        self.dibujar_minimapa()

        # barra del jefe, si está en pantalla
        for enemigo in self.enemigos:
            if isinstance(enemigo, JefeFinal):
                self.texto(self.pantalla, enemigo.nombre, ANCHO // 2, ALTO - 44,
                           self.fuente_chica, ROJO, True)
                self.barra(self.pantalla, ANCHO // 2 - 300, ALTO - 30, 600, 16,
                           enemigo.porcentaje_vida(), ROJO)

    def dibujar_minimapa(self):
        mapa = pygame.Rect(ANCHO - 170, 10, 150, 58)
        pygame.draw.rect(self.pantalla, (10, 12, 20), mapa, border_radius=6)
        pygame.draw.rect(self.pantalla, GRIS_OSCURO, mapa, 1, border_radius=6)
        escala_x = mapa.width / ANCHO
        escala_y = mapa.height / ALTO_ARENA
        for muro in self.nivel.obstaculos:
            chico = pygame.Rect(mapa.x + muro.x * escala_x,
                                mapa.y + muro.y * escala_y,
                                max(2, muro.width * escala_x),
                                max(2, muro.height * escala_y))
            pygame.draw.rect(self.pantalla, (52, 60, 80), chico)
        for enemigo in self.enemigos:
            pygame.draw.circle(self.pantalla,
                               ROJO if not isinstance(enemigo, JefeFinal) else VIOLETA,
                               (int(mapa.x + enemigo.x * escala_x),
                                int(mapa.y + enemigo.y * escala_y)), 2)
        pygame.draw.circle(self.pantalla, ORO,
                           (int(mapa.x + self.heroe.x * escala_x),
                            int(mapa.y + self.heroe.y * escala_y)), 3)

    def dibujar_pausa(self):
        capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        capa.fill((8, 10, 18, 190))
        self.pantalla.blit(capa, (0, 0))
        self.texto(self.pantalla, "PAUSA", ANCHO // 2, ALTO // 2 - 30,
                   self.fuente_titulo, ORO, True)
        self.texto(self.pantalla, "P o ESC para seguir   ·   M para volver al menú",
                   ANCHO // 2, ALTO // 2 + 40, self.fuente_media, GRIS, True)

    # ------------------------------------------------------ victoria / derrota
    def dibujar_final(self, gano):
        self.dibujar_fondo_estrellado()
        if gano:
            self.texto(self.pantalla, "¡VICTORIA!", ANCHO // 2, 120,
                       self.fuente_titulo, ORO, True)
            self.texto(self.pantalla, "Limpiaste la arena y venciste al jefe final.",
                       ANCHO // 2, 178, self.fuente_media, BLANCO, True)
            self.pantalla.blit(pygame.transform.scale(SPRITES["heroe"][
                (pygame.time.get_ticks() // 300) % 2], (104, 120)), (460, 400))
        else:
            self.texto(self.pantalla, "GAME OVER", ANCHO // 2, 120,
                       self.fuente_titulo, ROJO, True)
            self.texto(self.pantalla, "Caíste en la arena. Probá de nuevo.",
                       ANCHO // 2, 178, self.fuente_media, BLANCO, True)

        datos = [
            ("Puntaje final", str(self.puntaje)),
            ("Enemigos vencidos", str(self.enemigos_vencidos)),
            ("Nivel alcanzado", str(self.heroe.nivel)),
            ("Golpe más fuerte", str(self.golpe_mas_fuerte) + " de daño"),
            ("Niveles del mapa", str(self.indice_nivel + 1) + " de " +
             str(len(self.niveles))),
            ("Tiempo jugado", str(self.segundos_jugados) + " segundos"),
        ]
        y = 240
        for etiqueta, valor in datos:
            self.texto(self.pantalla, etiqueta, ANCHO // 2 - 200, y,
                       self.fuente_chica, GRIS)
            self.texto(self.pantalla, valor, ANCHO // 2 + 200, y,
                       self.fuente_media, BLANCO)
            y = y + 30

        self.texto(self.pantalla, "R  jugar de nuevo      M  menú      ESC  salir",
                   ANCHO // 2, ALTO - 50, self.fuente_media, ORO, True)


# =============================================================================
#  PARTE 7 · ARRANCAMOS
# =============================================================================

if __name__ == "__main__":
    Juego().jugar()
