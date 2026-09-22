# =============================================================================
#  ARENA DE COMBATE  ·  VERSIÓN 1 · CONSOLA
#  Trabajo práctico integrador de Programación Orientada a Objetos
#
#  Cómo se ejecuta:   python3 juego_consola.py
#  No necesita instalar nada: es Python puro, como pide el TP.
# =============================================================================
#
#  EL MÉTODO (el mismo de la etapa 1, y el mismo para cualquier problema):
#
#      Pensar el problema
#           ↓
#      Identificar los objetos
#           ↓
#      Definir atributos y métodos
#           ↓
#      Pensar las relaciones
#           ↓
#      Diseñar las clases
#           ↓
#      Escribir código        ← recién acá se toca el teclado
#           ↓
#      Probar → detectar errores → mejorar
#
# -----------------------------------------------------------------------------
#  1) ANALIZAR EL PROBLEMA
#     Un combate por turnos: un héroe con un arma pelea contra un enemigo.
#     Cada golpe baja vida. El que se queda sin vida, pierde. Si el héroe gana,
#     recibe experiencia y puede subir de nivel. También puede curarse.
#
#  2) IDENTIFICAR LOS OBJETOS
#     Personaje, Jugador, Enemigo, Arma, Pocion.
#     La vida, el nivel y la experiencia NO son objetos: son datos que viven
#     adentro de un objeto (son atributos).
#
#  3) DISEÑO DE LAS CLASES  (esta tabla se escribió antes que el código)
#
#     Clase       Atributos                 Métodos
#     ---------------------------------------------------------------------
#     Personaje   nombre, vida,             recibir_danio(), esta_vivo(),
#                 vida_maxima               mostrar_info()
#     Arma        nombre, danio             usar()
#     Pocion      nombre, cura              usar()
#     Jugador     arma, nivel, experiencia  atacar(), curarse(),
#                                           ganar_experiencia(), subir_nivel()
#     Enemigo     danio                     atacar()
#
#     En Jugador y en Enemigo NO se repiten nombre ni vida: los heredan.
#
#  4) LAS RELACIONES
#
#                      Personaje
#                   nombre · vida · vida_maxima
#                 recibir_danio() · esta_vivo()
#                       ▲            ▲
#                   ES UN         ES UN
#                       │            │
#          Jugador ◆────┘            └──── Enemigo
#          arma · nivel · exp                danio
#             │                                ▲       ▲
#        TIENE UN                            ES UN   ES UN
#             │                                │       │
#             ▼                              Goblin  Dragon
#           Arma / Pocion
#
# =============================================================================


# =============================================================================
#  5) LAS CLASES
# =============================================================================

class Personaje:
    """La clase de arriba: acá va SOLO lo que comparten todos los personajes."""

    def __init__(self, nombre, vida):
        self.nombre = nombre
        self.vida = vida
        self.vida_maxima = vida          # hasta acá se puede curar

    def recibir_danio(self, cantidad):
        self.vida = self.vida - cantidad
        if self.vida < 0:                # ← ENCAPSULACIÓN: el objeto cuida su
            self.vida = 0                #   propio dato. Nunca vida negativa.

    def esta_vivo(self):
        return self.vida > 0             # ← RETURN: lo necesita el programa
                                         #   (lo usa el while y los if)

    def mostrar_info(self):
        # Acá va print y no return: este texto lo lee una persona.
        print(self.nombre, "- Vida:", self.vida, "/", self.vida_maxima)


class Arma:
    """No hereda de nadie: un arma NO ES UN personaje."""

    def __init__(self, nombre, danio):
        self.nombre = nombre
        self.danio = danio

    def usar(self):
        return self.danio                # ← RETURN: ese número hay que
                                         #   restárselo a la vida del enemigo


class Pocion:
    """Casi idéntica a Arma: guarda un número y lo entrega cuando se la usa."""

    def __init__(self, nombre, cura):
        self.nombre = nombre
        self.cura = cura

    def usar(self):
        return self.cura


class Jugador(Personaje):                # ← HERENCIA: un Jugador ES UN Personaje

    def __init__(self, nombre, vida, arma):
        super().__init__(nombre, vida)   # ← SUPER(): "padre, encargate vos
                                         #   de nombre y vida"
        self.arma = arma                 # ← COMPOSICIÓN: un Jugador TIENE UN
                                         #   Arma. El atributo es otro objeto.
        self.nivel = 1                   # todos arrancan en nivel 1...
        self.experiencia = 0             # ...y con 0 de experiencia

    def atacar(self):
        return self.arma.usar()          # el jugador NO sabe cuánto pega:
                                         # le pregunta a su arma

    def curarse(self, pocion):
        self.vida = self.vida + pocion.usar()
        if self.vida > self.vida_maxima: # otra vez encapsulación:
            self.vida = self.vida_maxima # la vida nunca pasa del máximo

    def ganar_experiencia(self, cantidad):
        self.experiencia = self.experiencia + cantidad
        print(self.nombre, "ganó", cantidad, "de experiencia")
        if self.experiencia >= 100:
            self.subir_nivel()           # el objeto se encarga solo

    def subir_nivel(self):
        self.nivel = self.nivel + 1
        self.experiencia = self.experiencia - 100   # lo que sobra no se pierde
        self.vida_maxima = self.vida_maxima + 20
        self.vida = self.vida_maxima
        print(self.nombre, "subió al nivel", self.nivel)


class Enemigo(Personaje):                # ← HERENCIA: un Enemigo ES UN Personaje

    def __init__(self, nombre, vida, danio):
        super().__init__(nombre, vida)
        self.danio = danio               # el enemigo no usa arma: pega él mismo

    def atacar(self):
        return self.danio


# --- POLIMORFISMO -----------------------------------------------------------
# Las dos clases entienden la misma orden, atacar(), y cada una contesta a su
# manera. Ninguna escribe __init__: lo heredan tal cual de Enemigo, porque no
# agregan ningún atributo nuevo.

class Goblin(Enemigo):
    def atacar(self):
        return self.danio                # igual que el padre: podría no escribirse


class Dragon(Enemigo):
    def atacar(self):
        return self.danio + 15           # el dragón pega más fuerte


# =============================================================================
#  6) CREAMOS LOS OBJETOS
#     La clase describe. El objeto existe.
# =============================================================================

espada = Arma("Espada", 25)
pocion = Pocion("Poción chica", 30)
heroe = Jugador("Aria", 150, espada)        # 150 de vida: el dragón pega fuerte
enemigo = Dragon("Dragón rojo", 90, 20)     # 20 + 15 = 35 de daño por golpe


# =============================================================================
#  7) EL MENÚ: la forma de usar el sistema que construimos
#     Ojo: el menú NO es el trabajo práctico. Lo importante son las clases.
# =============================================================================

while True:
    print()
    print("=== ARENA DE COMBATE ===")
    print("1. Ver información")
    print("2. Atacar")
    print("3. Usar poción")
    print("4. Ver experiencia")
    print("5. Salir")
    opcion = input("Elegí una opción: ")

    if opcion == "1":
        heroe.mostrar_info()
        enemigo.mostrar_info()

    elif opcion == "2":
        danio = heroe.atacar()                  # el jugador le pide el daño al arma
        enemigo.recibir_danio(danio)            # el enemigo se lo resta a su vida
        print(heroe.nombre, "atacó con", heroe.arma.nombre, "e hizo", danio, "de daño")

        if enemigo.esta_vivo():                 # un enemigo muerto no contraataca
            golpe = enemigo.atacar()
            heroe.recibir_danio(golpe)
            print(enemigo.nombre, "contraatacó e hizo", golpe, "de daño")
        else:
            print(enemigo.nombre, "fue derrotado")
            heroe.ganar_experiencia(50)

    elif opcion == "3":
        heroe.curarse(pocion)
        print(heroe.nombre, "usó", pocion.nombre, "- Vida:", heroe.vida)

    elif opcion == "4":
        print("Nivel:", heroe.nivel, "- Experiencia:", heroe.experiencia, "/ 100")

    elif opcion == "5":
        print("¡Hasta la próxima!")
        break

    else:
        # Validación de la entrada: cualquier otra cosa que escriba la persona
        # cae acá y el programa sigue funcionando.
        print("Esa opción no existe")

    # ---- Final de la partida: se revisa después de cada vuelta del menú ----
    if not heroe.esta_vivo():
        print("GAME OVER")
        break

    if not enemigo.esta_vivo():
        print("¡GANASTE! Venciste a", enemigo.nombre)
        break
