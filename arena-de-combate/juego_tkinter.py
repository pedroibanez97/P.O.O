# =============================================================================
#  ARENA DE COMBATE  ·  VERSIÓN 2 · TKINTER
#  El MISMO juego de la versión 1, ahora con ventana, botones y dibujos.
#
#  Cómo se ejecuta:   python3 juego_tkinter.py
#  No hay que instalar nada: tkinter viene con Python.
# =============================================================================
#
#  ESTE NO ES OTRO JUEGO. Es el de juego_consola.py, un escalón más arriba.
#
#  LO QUE NO CAMBIÓ (abrí los dos archivos al lado y compará)
#    · Las clases son las mismas: Personaje, Arma, Pocion, Jugador, Enemigo...
#    · La herencia es la misma:   Jugador ES UN Personaje.
#    · La composición es la misma: Jugador TIENE UN Arma.
#    · El polimorfismo es el mismo: cada enemigo responde atacar() a su manera.
#    · La cuenta del combate es la misma: atacar() devuelve un número y
#      recibir_danio() se lo resta a la vida.
#
#  LO QUE SÍ CAMBIÓ (todo lo de la clase 3)
#    · import: incorporamos tres librerías (random, time, tkinter).
#    · random: el daño ya no es fijo, hay golpes críticos, el rival sale al
#      azar y el que empieza la pelea también.
#    · tiempo: el contraataque tarda un momento y el combate se cronometra.
#    · tkinter: el input() y los print() se reemplazan por botones y dibujos.
#
#  LA IDEA MÁS IMPORTANTE DE LA CLASE 3:
#    Tkinter dibuja. Nuestras clases siguen siendo las que saben de vida,
#    daño, experiencia y niveles. Son dos trabajos separados.
# =============================================================================

import random                # números al azar          (clase 3, bloque 3)
import time                  # para cronometrar la pelea (clase 3, bloque 2)
import tkinter as tk         # la interfaz gráfica       (clase 3, bloque 5)


# =============================================================================
#  PARTE 1 · LAS CLASES DEL JUEGO
#  Esta parte es POO pura: no sabe que existe una ventana. Si mañana borramos
#  toda la interfaz, estas clases siguen funcionando igual.
# =============================================================================

class Personaje:
    """La clase de arriba: solo lo que comparten todos."""

    def __init__(self, nombre, vida):
        self.nombre = nombre
        self.vida = vida
        self.vida_maxima = vida

    def recibir_danio(self, cantidad):
        self.vida = self.vida - cantidad
        if self.vida < 0:                 # encapsulación: nunca vida negativa
            self.vida = 0

    def esta_vivo(self):
        return self.vida > 0              # return: lo usa el programa

    def porcentaje_vida(self):
        # NUEVO: lo necesita la barra de vida. Fijate que igual es un return,
        # y que el cálculo lo hace el personaje, no la ventana.
        return self.vida / self.vida_maxima


class Arma:
    """NUEVO: el daño ahora es un rango, y usar() devuelve un número al azar."""

    def __init__(self, nombre, danio_minimo, danio_maximo):
        self.nombre = nombre
        self.danio_minimo = danio_minimo
        self.danio_maximo = danio_maximo

    def usar(self):
        # Antes era:  return self.danio
        # Ahora:      un número al azar dentro del rango del arma.
        return random.randint(self.danio_minimo, self.danio_maximo)


class Pocion:
    """NUEVO: la poción tiene usos limitados (desafío nivel 2 del TP)."""

    def __init__(self, nombre, cura, usos):
        self.nombre = nombre
        self.cura = cura
        self.usos = usos

    def usar(self):
        if self.usos <= 0:
            return 0                      # ya no queda nada adentro
        self.usos = self.usos - 1
        return self.cura

    def recargar(self, cantidad):
        # La poción se encarga de sus propios usos: nadie los toca desde afuera.
        self.usos = self.usos + cantidad


class Jugador(Personaje):                 # HERENCIA: un Jugador ES UN Personaje

    def __init__(self, nombre, vida, arma):
        super().__init__(nombre, vida)    # SUPER(): el padre guarda nombre y vida
        self.arma = arma                  # COMPOSICIÓN: TIENE UN arma
        self.nivel = 1
        self.experiencia = 0
        self.ultimo_golpe_fue_critico = False   # NUEVO: para avisarle a la ventana

    def atacar(self):
        danio = self.arma.usar()          # le pregunta al arma, como siempre
        # NUEVO: 20 de cada 100 golpes son críticos y pegan el doble.
        if random.randint(1, 100) <= 20:
            self.ultimo_golpe_fue_critico = True
            danio = danio * 2
        else:
            self.ultimo_golpe_fue_critico = False
        return danio

    def curarse(self, pocion):
        self.vida = self.vida + pocion.usar()
        if self.vida > self.vida_maxima:
            self.vida = self.vida_maxima

    def ganar_experiencia(self, cantidad):
        self.experiencia = self.experiencia + cantidad
        if self.experiencia >= 100:
            self.subir_nivel()
            return True                   # return: la ventana necesita saberlo
        return False

    def subir_nivel(self):
        self.nivel = self.nivel + 1
        self.experiencia = self.experiencia - 100
        self.vida_maxima = self.vida_maxima + 20
        self.vida = self.vida_maxima


class Enemigo(Personaje):                 # HERENCIA: un Enemigo ES UN Personaje

    def __init__(self, nombre, vida, danio, color):
        super().__init__(nombre, vida)
        self.danio = danio
        self.color = color                # su aspecto, para poder dibujarlo

    def atacar(self):
        return self.danio


# --- POLIMORFISMO -----------------------------------------------------------
# Los tres entienden atacar() y cada uno contesta distinto. Ninguno escribe
# __init__: lo heredan de Enemigo, porque no agregan ningún atributo nuevo.

class Goblin(Enemigo):
    def atacar(self):
        return self.danio + random.randint(0, 4)


class Esqueleto(Enemigo):
    def atacar(self):
        return self.danio * 2             # pega doble (desafío de la etapa 8)


class Dragon(Enemigo):
    def atacar(self):
        return self.danio + 15            # el dragón pega más fuerte


def armar_rivales():
    """Devuelve la lista de rivales de la partida, en orden al azar.

    random.shuffle() mezcla una lista: es otra herramienta de random que no
    vimos en clase y que se investiga igual que randint (clase 3, bloque 2).
    El dragón se agrega al final: siempre es el último rival.
    """
    rivales = [
        Goblin("Goblin", 60, 12, "#6fbf5a"),
        Esqueleto("Esqueleto", 45, 9, "#d8d6cc"),
    ]
    random.shuffle(rivales)
    rivales.append(Dragon("Dragón rojo", 90, 20, "#e0553c"))
    return rivales


# =============================================================================
#  PARTE 2 · LA INTERFAZ
#  De acá para abajo es tkinter. Esta parte dibuja y escucha clics: no decide
#  cuánto daño hace un golpe, eso sigue siendo trabajo de las clases de arriba.
# =============================================================================

FUENTE = "Helvetica"

FONDO        = "#11141f"     # el azul casi negro del fondo
PANEL        = "#1b2030"     # las cajas de adelante
BORDE        = "#2c3347"
TEXTO        = "#e8ecf5"
TEXTO_SUAVE  = "#8b93a8"
ORO          = "#f2b134"
ROJO         = "#e0553c"
VERDE        = "#3fb27f"
AZUL         = "#4a7cf0"
VIOLETA      = "#8b5cf6"

ANCHO = 960
ALTO = 680


def rectangulo_redondeado(lienzo, x1, y1, x2, y2, radio, color, borde=""):
    """Tkinter no trae rectángulos redondeados: los armamos con un polígono
    suavizado. Es un truco de dibujo, no un concepto nuevo de POO."""
    puntos = [x1 + radio, y1, x2 - radio, y1, x2, y1, x2, y1 + radio,
              x2, y2 - radio, x2, y2, x2 - radio, y2, x1 + radio, y2,
              x1, y2, x1, y2 - radio, x1, y1 + radio, x1, y1]
    return lienzo.create_polygon(puntos, fill=color, outline=borde, smooth=True)


class Boton:
    """Un botón hecho con un Label.

    ¿Por qué no tk.Button? Porque en Mac no deja cambiarle el color de fondo.
    Con un Label y bind("<Button-1>", ...) el botón se ve igual en todos lados.
    Es un objeto más: tiene datos (color, comando) y sabe hacer cosas.
    """

    def __init__(self, padre, texto, color, comando, ancho=14):
        self.color = color
        self.comando = comando
        self.habilitado = True
        self.etiqueta = tk.Label(padre, text=texto, bg=color, fg="#0d1018",
                                 font=(FUENTE, 15, "bold"), width=ancho,
                                 pady=12, cursor="hand2")
        self.etiqueta.bind("<Button-1>", self.al_hacer_clic)
        self.etiqueta.bind("<Enter>", self.al_entrar_el_mouse)
        self.etiqueta.bind("<Leave>", self.al_salir_el_mouse)

    def al_hacer_clic(self, evento):
        if self.habilitado:
            self.comando()            # ← acá se conecta el clic con el juego

    def al_entrar_el_mouse(self, evento):
        if self.habilitado:
            self.etiqueta.config(bg="#ffffff")

    def al_salir_el_mouse(self, evento):
        if self.habilitado:
            self.etiqueta.config(bg=self.color)

    def habilitar(self):
        self.habilitado = True
        self.etiqueta.config(bg=self.color, fg="#0d1018", cursor="hand2")

    def deshabilitar(self):
        self.habilitado = False
        self.etiqueta.config(bg="#333a4d", fg=TEXTO_SUAVE, cursor="arrow")


class NumeroFlotante:
    """El "-25" rojo que sube y se desvanece cuando alguien recibe un golpe.

    Otro objeto chiquito: guarda dónde está y sabe moverse.
    """

    def __init__(self, x, y, texto, color, tamanio=22):
        self.x = x
        self.y = y
        self.texto = texto
        self.color = color
        self.tamanio = tamanio
        self.vida = 40                # cuántos cuadros le quedan

    def actualizar(self):
        self.y = self.y - 1.6         # sube
        self.vida = self.vida - 1

    def sigue_vivo(self):
        return self.vida > 0


class ArenaDeCombate:
    """La ventana. Dibuja el estado del juego y traduce los clics en órdenes
    para los objetos. No calcula daño ni decide quién gana: eso lo saben
    el Jugador, el Enemigo y el Arma."""

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Arena de Combate · POO + Tkinter")
        self.ventana.geometry(str(ANCHO) + "x" + str(ALTO))
        self.ventana.configure(bg=FONDO)
        self.ventana.resizable(False, False)

        self.contenedor = tk.Frame(self.ventana, bg=FONDO)
        self.contenedor.pack(fill="both", expand=True)

        # Estado de la partida (se completa al empezar)
        self.heroe = None
        self.rivales = []
        self.enemigo = None
        self.pocion = None
        self.arma_elegida = 0
        self.mensajes = []
        self.numeros = []
        self.animando = False
        self.turno_del_jugador = True
        self.vencidos = 0
        self.golpe_mas_fuerte = 0
        self.momento_de_inicio = 0

        # Lo que se muestra en las barras (se acerca de a poco al valor real:
        # así la barra baja suave en vez de saltar de golpe).
        self.vida_dibujada_heroe = 0
        self.vida_dibujada_enemigo = 0
        self.sacudida_heroe = 0
        self.sacudida_enemigo = 0

        self.armas_disponibles = [
            Arma("Espada", 20, 30),
            Arma("Hacha", 12, 42),
            Arma("Arco", 23, 27),
        ]

        self.pantalla_inicio()

    # ---------------------------------------------------------------- utilidad
    def limpiar(self):
        """Borra todos los widgets: así cambiamos de pantalla."""
        for hijo in self.contenedor.winfo_children():
            hijo.destroy()

    def escribir(self, mensaje):
        """Reemplaza al print() de la versión consola."""
        self.mensajes.append(mensaje)
        if len(self.mensajes) > 6:
            self.mensajes.pop(0)
        if self.registro is not None:
            self.registro.config(text="\n".join(self.mensajes))

    # =====================================================================
    #  PANTALLA 1 · elegir personaje y arma
    # =====================================================================
    def pantalla_inicio(self):
        self.limpiar()
        self.registro = None

        tk.Label(self.contenedor, text="⚔  ARENA DE COMBATE", bg=FONDO, fg=ORO,
                 font=(FUENTE, 40, "bold")).pack(pady=(50, 0))
        tk.Label(self.contenedor, text="Versión 2 · POO + librerías + interfaz",
                 bg=FONDO, fg=TEXTO_SUAVE, font=(FUENTE, 14)).pack(pady=(4, 26))

        caja = tk.Frame(self.contenedor, bg=PANEL, padx=40, pady=26)
        caja.pack()

        tk.Label(caja, text="¿Cómo se llama tu personaje?", bg=PANEL, fg=TEXTO,
                 font=(FUENTE, 15, "bold")).pack()
        self.entrada_nombre = tk.Entry(caja, font=(FUENTE, 18), width=18,
                                       justify="center", bg=FONDO, fg=ORO,
                                       insertbackground=ORO, relief="flat")
        self.entrada_nombre.insert(0, "Aria")
        self.entrada_nombre.pack(pady=(10, 22), ipady=8)

        tk.Label(caja, text="Elegí tu arma", bg=PANEL, fg=TEXTO,
                 font=(FUENTE, 15, "bold")).pack()
        tk.Label(caja, text="Cada arma pega un número al azar dentro de su rango",
                 bg=PANEL, fg=TEXTO_SUAVE, font=(FUENTE, 11)).pack(pady=(2, 12))

        fila = tk.Frame(caja, bg=PANEL)
        fila.pack()
        self.tarjetas_arma = []
        for numero in range(len(self.armas_disponibles)):
            arma = self.armas_disponibles[numero]
            tarjeta = tk.Frame(fila, bg=FONDO, padx=22, pady=14,
                               highlightthickness=3, highlightbackground=FONDO)
            tarjeta.pack(side="left", padx=8)
            tk.Label(tarjeta, text=arma.nombre, bg=FONDO, fg=TEXTO,
                     font=(FUENTE, 16, "bold")).pack()
            rango = str(arma.danio_minimo) + " - " + str(arma.danio_maximo)
            tk.Label(tarjeta, text=rango + " de daño", bg=FONDO, fg=TEXTO_SUAVE,
                     font=(FUENTE, 12)).pack()
            # Cada tarjeta recuerda su propio número gracias al parámetro n.
            tarjeta.bind("<Button-1>", lambda e, n=numero: self.elegir_arma(n))
            for hijo in tarjeta.winfo_children():
                hijo.bind("<Button-1>", lambda e, n=numero: self.elegir_arma(n))
            self.tarjetas_arma.append(tarjeta)
        self.elegir_arma(0)

        Boton(self.contenedor, "▶  ENTRAR A LA ARENA", ORO,
              self.empezar_partida, ancho=22).etiqueta.pack(pady=30)

        tk.Label(self.contenedor,
                 text="Las clases del juego son las mismas de juego_consola.py."
                      "  Lo único nuevo es la cara.",
                 bg=FONDO, fg=TEXTO_SUAVE, font=(FUENTE, 11)).pack(side="bottom",
                                                                   pady=14)

    def elegir_arma(self, numero):
        self.arma_elegida = numero
        for i in range(len(self.tarjetas_arma)):
            if i == numero:
                self.tarjetas_arma[i].config(highlightbackground=ORO)
            else:
                self.tarjetas_arma[i].config(highlightbackground=BORDE)

    # =====================================================================
    #  PANTALLA 2 · el combate
    # =====================================================================
    def empezar_partida(self):
        nombre = self.entrada_nombre.get()
        if nombre == "":                      # validamos la entrada, igual que
            nombre = "Aria"                   # el else del menú de la versión 1

        # Acá se crean los objetos, exactamente como en la versión consola.
        arma = self.armas_disponibles[self.arma_elegida]
        self.heroe = Jugador(nombre, 150, arma)
        self.pocion = Pocion("Poción", 30, 3)
        self.rivales = armar_rivales()
        self.enemigo = self.rivales.pop(0)

        self.mensajes = []
        self.numeros = []
        self.vencidos = 0
        self.golpe_mas_fuerte = 0
        self.momento_de_inicio = time.time()      # librería time: cronómetro
        self.vida_dibujada_heroe = self.heroe.vida
        self.vida_dibujada_enemigo = self.enemigo.vida

        self.pantalla_combate()

        self.escribir("Aparece " + self.enemigo.nombre + ".")
        # random otra vez: ¿quién empieza la pelea? (idea de la clase 3)
        if random.choice(["jugador", "enemigo"]) == "enemigo":
            self.escribir(self.enemigo.nombre + " ataca primero.")
            self.bloquear_botones()
            self.ventana.after(900, self.turno_del_enemigo)
        else:
            self.escribir("Empezás vos. ¡A pelear!")

    def pantalla_combate(self):
        self.limpiar()

        tk.Label(self.contenedor, text="⚔  ARENA DE COMBATE", bg=FONDO, fg=ORO,
                 font=(FUENTE, 22, "bold")).pack(pady=(16, 0))
        self.subtitulo = tk.Label(self.contenedor, text="", bg=FONDO,
                                  fg=TEXTO_SUAVE, font=(FUENTE, 12))
        self.subtitulo.pack()

        self.lienzo = tk.Canvas(self.contenedor, width=900, height=330,
                                bg=PANEL, highlightthickness=0)
        self.lienzo.pack(pady=12)

        fila_botones = tk.Frame(self.contenedor, bg=FONDO)
        fila_botones.pack(pady=4)
        self.boton_atacar = Boton(fila_botones, "⚔  ATACAR", ORO, self.accion_atacar)
        self.boton_atacar.etiqueta.pack(side="left", padx=8)
        self.boton_pocion = Boton(fila_botones, "✚  POCIÓN", VERDE, self.accion_pocion)
        self.boton_pocion.etiqueta.pack(side="left", padx=8)

        self.registro = tk.Label(self.contenedor, text="", bg=FONDO, fg=TEXTO,
                                 font=(FUENTE, 12), justify="left", height=6,
                                 anchor="nw")
        self.registro.pack(fill="x", padx=40, pady=(10, 0))
        self.registro.config(text="\n".join(self.mensajes))

        self.animar()                      # arranca el "bucle" de dibujo

    # ------------------------------------------------------------- el dibujo
    def animar(self):
        """Se llama sola cada 30 milisegundos con after(): dibuja todo de nuevo.

        Así funcionan los videojuegos: no se corrige el dibujo, se borra todo y
        se vuelve a dibujar a partir del estado actual. En la versión de Pygame
        vamos a hacer exactamente esto, pero 60 veces por segundo.

        OJO: acá NO se puede usar time.sleep(), porque congelaría la ventana.
        En una interfaz, esperar se hace con after().
        """
        if not self.lienzo.winfo_exists():
            return

        # las barras se acercan de a poco al valor real
        self.vida_dibujada_heroe = self.acercar(self.vida_dibujada_heroe,
                                                self.heroe.vida)
        self.vida_dibujada_enemigo = self.acercar(self.vida_dibujada_enemigo,
                                                  self.enemigo.vida)
        self.sacudida_heroe = self.sacudida_heroe * 0.85
        self.sacudida_enemigo = self.sacudida_enemigo * 0.85

        vivos = []
        for numero in self.numeros:
            numero.actualizar()
            if numero.sigue_vivo():
                vivos.append(numero)
        self.numeros = vivos

        self.dibujar_arena()
        self.ventana.after(30, self.animar)

    def acercar(self, actual, objetivo):
        if abs(actual - objetivo) < 0.6:
            return objetivo
        return actual + (objetivo - actual) * 0.18

    def dibujar_arena(self):
        lienzo = self.lienzo
        lienzo.delete("all")

        # --- escenario ---
        lienzo.create_rectangle(0, 0, 900, 240, fill="#151a2b", outline="")
        lienzo.create_oval(700, 20, 780, 100, fill="#2a3150", outline="")   # luna
        lienzo.create_polygon(0, 240, 150, 120, 300, 240, fill="#1d2338", outline="")
        lienzo.create_polygon(180, 240, 380, 100, 580, 240, fill="#222943", outline="")
        lienzo.create_polygon(500, 240, 700, 140, 900, 240, fill="#1d2338", outline="")
        lienzo.create_rectangle(0, 240, 900, 330, fill="#2a2036", outline="")
        for x in range(0, 900, 60):
            lienzo.create_line(x, 240, x - 40, 330, fill="#332843")

        self.dibujar_heroe(200 + self.sacudida_heroe, 235)
        self.dibujar_enemigo(700 + self.sacudida_enemigo, 235)

        self.dibujar_barra(40, 28, self.heroe.nombre,
                           self.vida_dibujada_heroe, self.heroe.vida_maxima,
                           VERDE, "Nivel " + str(self.heroe.nivel))
        self.dibujar_barra(520, 28, self.enemigo.nombre,
                           self.vida_dibujada_enemigo, self.enemigo.vida_maxima,
                           ROJO, type(self.enemigo).__name__)

        # barra de experiencia del héroe
        rectangulo_redondeado(lienzo, 40, 84, 340, 96, 6, "#232a3d")
        ancho_exp = 300 * (self.heroe.experiencia / 100)
        if ancho_exp > 8:
            rectangulo_redondeado(lienzo, 40, 84, 40 + ancho_exp, 96, 6, VIOLETA)
        lienzo.create_text(40, 108, anchor="w", fill=TEXTO_SUAVE,
                           font=(FUENTE, 10),
                           text="EXP " + str(self.heroe.experiencia) + " / 100")

        lienzo.create_text(450, 300, fill=TEXTO_SUAVE, font=(FUENTE, 11),
                           text="Pociones: " + str(self.pocion.usos) +
                                "   ·   Rivales vencidos: " + str(self.vencidos))

        for numero in self.numeros:
            lienzo.create_text(numero.x, numero.y, text=numero.texto,
                               fill=numero.color,
                               font=(FUENTE, numero.tamanio, "bold"))

        self.subtitulo.config(text="Rival " + str(self.vencidos + 1) + " de 3   ·   " +
                                   self.heroe.arma.nombre + " (" +
                                   str(self.heroe.arma.danio_minimo) + "-" +
                                   str(self.heroe.arma.danio_maximo) + ")")

    def dibujar_barra(self, x, y, nombre, vida, vida_maxima, color, etiqueta):
        lienzo = self.lienzo
        lienzo.create_text(x, y, anchor="w", text=nombre, fill=TEXTO,
                           font=(FUENTE, 15, "bold"))
        lienzo.create_text(x + 340, y, anchor="e", text=etiqueta, fill=TEXTO_SUAVE,
                           font=(FUENTE, 11))
        rectangulo_redondeado(lienzo, x, y + 14, x + 340, y + 38, 10, "#232a3d")
        ancho = 340 * max(0, vida) / vida_maxima
        if ancho > 12:
            rectangulo_redondeado(lienzo, x, y + 14, x + ancho, y + 38, 10, color)
        lienzo.create_text(x + 170, y + 26,
                           text=str(int(round(vida))) + " / " + str(vida_maxima),
                           fill="#0d1018", font=(FUENTE, 12, "bold"))

    def dibujar_heroe(self, x, y):
        """Nuestro personaje, dibujado con figuras (sin imágenes externas)."""
        lienzo = self.lienzo
        lienzo.create_oval(x - 45, y - 8, x + 45, y + 12, fill="#0e1120", outline="")
        lienzo.create_rectangle(x - 22, y - 78, x + 22, y - 18, fill=AZUL, outline="")
        lienzo.create_polygon(x - 22, y - 78, x + 22, y - 78, x, y - 96,
                              fill="#7ba0ff", outline="")
        lienzo.create_oval(x - 18, y - 122, x + 18, y - 86, fill="#f0c9a0", outline="")
        lienzo.create_rectangle(x - 18, y - 122, x + 18, y - 104, fill="#c0c8e0",
                                outline="")
        lienzo.create_rectangle(x - 12, y - 108, x - 4, y - 102, fill="#1b2030",
                                outline="")
        lienzo.create_rectangle(x + 4, y - 108, x + 12, y - 102, fill="#1b2030",
                                outline="")
        lienzo.create_rectangle(x + 26, y - 96, x + 34, y - 26, fill="#d8dde8",
                                outline="")       # la espada
        lienzo.create_rectangle(x + 18, y - 32, x + 42, y - 24, fill="#8a6b3d",
                                outline="")
        lienzo.create_rectangle(x - 16, y - 18, x - 4, y + 4, fill="#2d3654", outline="")
        lienzo.create_rectangle(x + 4, y - 18, x + 16, y + 4, fill="#2d3654", outline="")

    def dibujar_enemigo(self, x, y):
        """El enemigo se dibuja con SU color y con la forma que corresponde a
        su clase. Los tres usan el mismo método: cambia el resultado."""
        lienzo = self.lienzo
        color = self.enemigo.color
        lienzo.create_oval(x - 50, y - 8, x + 50, y + 12, fill="#0e1120", outline="")

        if isinstance(self.enemigo, Dragon):
            lienzo.create_polygon(x - 10, y - 70, x - 70, y - 120, x - 24, y - 40,
                                  fill="#8f3324", outline="")
            lienzo.create_polygon(x + 10, y - 70, x + 70, y - 120, x + 24, y - 40,
                                  fill="#8f3324", outline="")
            lienzo.create_oval(x - 34, y - 86, x + 34, y - 6, fill=color, outline="")
            lienzo.create_oval(x - 26, y - 128, x + 30, y - 78, fill=color, outline="")
            lienzo.create_polygon(x + 24, y - 112, x + 56, y - 104, x + 24, y - 92,
                                  fill="#f2b134", outline="")
        elif isinstance(self.enemigo, Esqueleto):
            lienzo.create_oval(x - 24, y - 118, x + 24, y - 74, fill=color, outline="")
            lienzo.create_rectangle(x - 16, y - 74, x + 16, y - 16, fill=color,
                                    outline="")
            for i in range(3):
                lienzo.create_line(x - 16, y - 66 + i * 14, x + 16, y - 66 + i * 14,
                                   fill="#1b2030", width=3)
        else:                                   # goblin
            lienzo.create_oval(x - 30, y - 74, x + 30, y - 10, fill=color, outline="")
            lienzo.create_oval(x - 26, y - 116, x + 26, y - 66, fill=color, outline="")
            lienzo.create_polygon(x - 26, y - 100, x - 54, y - 112, x - 24, y - 84,
                                  fill=color, outline="")
            lienzo.create_polygon(x + 26, y - 100, x + 54, y - 112, x + 24, y - 84,
                                  fill=color, outline="")

        lienzo.create_oval(x - 16, y - 104, x - 6, y - 94, fill="#12151f", outline="")
        lienzo.create_oval(x + 6, y - 104, x + 16, y - 94, fill="#12151f", outline="")

    # ------------------------------------------------------------ las acciones
    def bloquear_botones(self):
        self.animando = True
        self.boton_atacar.deshabilitar()
        self.boton_pocion.deshabilitar()

    def desbloquear_botones(self):
        self.animando = False
        self.boton_atacar.habilitar()
        if self.pocion.usos > 0:
            self.boton_pocion.habilitar()
        else:
            self.boton_pocion.deshabilitar()

    def accion_atacar(self):
        """El clic del botón ATACAR. Estas son las MISMAS dos líneas de la
        versión consola: danio = heroe.atacar() y enemigo.recibir_danio(danio)."""
        if self.animando:
            return
        self.bloquear_botones()

        danio = self.heroe.atacar()
        self.enemigo.recibir_danio(danio)
        self.sacudida_enemigo = 14
        if danio > self.golpe_mas_fuerte:
            self.golpe_mas_fuerte = danio

        if self.heroe.ultimo_golpe_fue_critico:
            self.numeros.append(NumeroFlotante(700, 150, "¡CRÍTICO! -" + str(danio),
                                               ORO, 20))
            self.escribir("¡GOLPE CRÍTICO! " + self.heroe.nombre + " hace " +
                          str(danio) + " de daño con " + self.heroe.arma.nombre + ".")
        else:
            self.numeros.append(NumeroFlotante(700, 150, "-" + str(danio), ROJO))
            self.escribir(self.heroe.nombre + " ataca con " +
                          self.heroe.arma.nombre + " y hace " + str(danio) +
                          " de daño.")

        if self.enemigo.esta_vivo():
            self.ventana.after(750, self.turno_del_enemigo)
        else:
            self.ventana.after(700, self.enemigo_derrotado)

    def accion_pocion(self):
        if self.animando:
            return
        if self.pocion.usos == 0:
            self.escribir("No te quedan pociones.")
            return
        self.bloquear_botones()

        vida_antes = self.heroe.vida
        self.heroe.curarse(self.pocion)
        curado = self.heroe.vida - vida_antes
        self.numeros.append(NumeroFlotante(200, 150, "+" + str(curado), VERDE))
        self.escribir(self.heroe.nombre + " usa una poción y recupera " +
                      str(curado) + " de vida.")
        self.ventana.after(750, self.turno_del_enemigo)

    def turno_del_enemigo(self):
        """El contraataque. Igual que en la consola, pero con espera: after()
        deja que la ventana siga respondiendo mientras tanto."""
        if not self.enemigo.esta_vivo():
            self.desbloquear_botones()
            return

        golpe = self.enemigo.atacar()          # POLIMORFISMO: cada clase contesta
        self.heroe.recibir_danio(golpe)        # distinto y acá no hay ni un if
        self.sacudida_heroe = 14
        self.numeros.append(NumeroFlotante(200, 150, "-" + str(golpe), ROJO))
        self.escribir(self.enemigo.nombre + " contraataca y hace " + str(golpe) +
                      " de daño.")

        if not self.heroe.esta_vivo():
            self.ventana.after(900, lambda: self.pantalla_final(False))
            return

        if self.heroe.vida < 30:
            self.escribir("¡Cuidado, estás por morir!")
        self.desbloquear_botones()

    def enemigo_derrotado(self):
        self.vencidos = self.vencidos + 1
        self.escribir(self.enemigo.nombre + " fue derrotado.")
        subio = self.heroe.ganar_experiencia(50)
        self.numeros.append(NumeroFlotante(700, 130, "+50 EXP", VIOLETA, 18))
        self.escribir(self.heroe.nombre + " ganó 50 de experiencia.")
        if subio:
            self.escribir("¡" + self.heroe.nombre + " subió al nivel " +
                          str(self.heroe.nivel) + "! Vida máxima: " +
                          str(self.heroe.vida_maxima))
            self.numeros.append(NumeroFlotante(200, 120, "¡NIVEL " +
                                               str(self.heroe.nivel) + "!", ORO, 20))

        # El enemigo puede soltar una poción: otra idea con random (clase 3).
        if random.randint(1, 100) <= 60:
            self.pocion.recargar(1)
            self.escribir("Soltó una poción. Ahora tenés " + str(self.pocion.usos) + ".")

        if len(self.rivales) == 0:
            self.ventana.after(1200, lambda: self.pantalla_final(True))
        else:
            self.ventana.after(1200, self.siguiente_rival)

    def siguiente_rival(self):
        self.enemigo = self.rivales.pop(0)
        self.vida_dibujada_enemigo = self.enemigo.vida
        self.escribir("Aparece " + self.enemigo.nombre + ".")
        self.desbloquear_botones()

    # =====================================================================
    #  PANTALLA 3 · victoria o derrota
    # =====================================================================
    def pantalla_final(self, gano):
        segundos = int(time.time() - self.momento_de_inicio)   # librería time
        self.limpiar()
        self.registro = None

        if gano:
            titulo, color, frase = ("🏆  ¡VICTORIA!", ORO,
                                    "Venciste a los tres rivales de la arena.")
        else:
            titulo, color, frase = ("☠  GAME OVER", ROJO,
                                    "Caíste en la arena. Probá de nuevo.")

        tk.Label(self.contenedor, text=titulo, bg=FONDO, fg=color,
                 font=(FUENTE, 44, "bold")).pack(pady=(80, 6))
        tk.Label(self.contenedor, text=frase, bg=FONDO, fg=TEXTO,
                 font=(FUENTE, 15)).pack(pady=(0, 30))

        caja = tk.Frame(self.contenedor, bg=PANEL, padx=50, pady=24)
        caja.pack()
        datos = [
            ("Personaje", self.heroe.nombre),
            ("Nivel alcanzado", str(self.heroe.nivel)),
            ("Rivales vencidos", str(self.vencidos) + " de 3"),
            ("Golpe más fuerte", str(self.golpe_mas_fuerte) + " de daño"),
            ("Duración del combate", str(segundos) + " segundos"),
        ]
        for etiqueta, valor in datos:
            fila = tk.Frame(caja, bg=PANEL)
            fila.pack(fill="x", pady=3)
            tk.Label(fila, text=etiqueta, bg=PANEL, fg=TEXTO_SUAVE,
                     font=(FUENTE, 13), width=20, anchor="w").pack(side="left")
            tk.Label(fila, text=valor, bg=PANEL, fg=TEXTO,
                     font=(FUENTE, 13, "bold")).pack(side="left")

        fila_botones = tk.Frame(self.contenedor, bg=FONDO)
        fila_botones.pack(pady=34)
        boton_otra = Boton(fila_botones, "↺  JUGAR DE NUEVO", ORO,
                           self.pantalla_inicio, ancho=18)
        boton_otra.etiqueta.pack(side="left", padx=8)
        boton_salir = Boton(fila_botones, "✕  SALIR", "#4a5268",
                            self.ventana.destroy, ancho=12)
        boton_salir.etiqueta.pack(side="left", padx=8)


# =============================================================================
#  PARTE 3 · arrancamos
#  mainloop() deja la ventana abierta, esperando clics. Sin esa línea, la
#  ventana se abre y se cierra al instante.
# =============================================================================

juego = ArenaDeCombate()
juego.ventana.mainloop()
