# =============================================================================
#  GENERADOR DE SONIDOS  ·  Arena de Combate
#
#  Los sonidos y la música del juego NO se bajaron de ningún lado: los fabrica
#  este script con Python puro (las librerías wave, math, struct y random, que
#  ya vienen instaladas). Así no hay problemas de licencia y no falta ningún
#  archivo.
#
#  Cómo se ejecuta (solo hace falta si querés volver a generarlos):
#      python3 generar_sonidos.py
#
#  Deja los .wav en assets/sonidos/ y assets/musica/.
# =============================================================================

import math
import os
import random
import struct
import wave

FRECUENCIA = 22050          # muestras por segundo
CARPETA = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------- herramientas

def guardar(nombre_archivo, muestras):
    """Escribe una lista de números entre -1 y 1 como archivo .wav mono."""
    ruta = os.path.join(CARPETA, nombre_archivo)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    archivo = wave.open(ruta, "w")
    archivo.setnchannels(1)
    archivo.setsampwidth(2)              # 16 bits
    archivo.setframerate(FRECUENCIA)
    datos = b"".join(struct.pack("<h", int(max(-1.0, min(1.0, m)) * 32000))
                     for m in muestras)
    archivo.writeframes(datos)
    archivo.close()
    print("  ", nombre_archivo, "->", round(len(muestras) / FRECUENCIA, 2), "seg")


def silencio(segundos):
    return [0.0] * int(segundos * FRECUENCIA)


def onda(frecuencia, segundos, forma="cuadrada", volumen=0.5, caida=6.0,
         frecuencia_final=None):
    """Genera una nota. forma: cuadrada, sierra, seno o ruido."""
    total = int(segundos * FRECUENCIA)
    muestras = []
    fase = 0.0
    for i in range(total):
        avance = i / total
        f = frecuencia
        if frecuencia_final is not None:
            f = frecuencia + (frecuencia_final - frecuencia) * avance
        fase = fase + f / FRECUENCIA
        ciclo = fase - int(fase)
        if forma == "cuadrada":
            valor = 1.0 if ciclo < 0.5 else -1.0
        elif forma == "sierra":
            valor = 2.0 * ciclo - 1.0
        elif forma == "seno":
            valor = math.sin(2 * math.pi * ciclo)
        else:                                     # ruido
            valor = random.uniform(-1.0, 1.0)
        envolvente = math.exp(-caida * avance)
        muestras.append(valor * envolvente * volumen)
    return muestras


def mezclar(*pistas):
    """Suma varias listas de muestras (las que suenan al mismo tiempo)."""
    largo = max(len(p) for p in pistas)
    salida = [0.0] * largo
    for pista in pistas:
        for i in range(len(pista)):
            salida[i] = salida[i] + pista[i]
    return salida


def unir(*pistas):
    """Pega listas una detrás de la otra (las que suenan una tras otra)."""
    salida = []
    for pista in pistas:
        salida.extend(pista)
    return salida


# ------------------------------------------------------------------- efectos

def hacer_efectos():
    print("Efectos:")

    guardar("sonidos/disparo.wav",
            mezclar(onda(880, 0.10, "cuadrada", 0.35, 22, 260),
                    onda(1500, 0.06, "ruido", 0.10, 30)))

    guardar("sonidos/golpe.wav",
            mezclar(onda(180, 0.16, "cuadrada", 0.40, 16, 60),
                    onda(400, 0.10, "ruido", 0.25, 26)))

    guardar("sonidos/critico.wav",
            unir(onda(1200, 0.07, "cuadrada", 0.35, 12, 900),
                 mezclar(onda(220, 0.22, "sierra", 0.45, 10, 70),
                         onda(600, 0.14, "ruido", 0.25, 18))))

    guardar("sonidos/danio.wav",
            mezclar(onda(140, 0.26, "sierra", 0.45, 9, 50),
                    onda(300, 0.12, "ruido", 0.20, 20)))

    guardar("sonidos/enemigo_muere.wav",
            mezclar(onda(520, 0.34, "cuadrada", 0.35, 7, 90),
                    onda(900, 0.20, "ruido", 0.18, 12)))

    guardar("sonidos/pocion.wav",
            unir(onda(660, 0.07, "seno", 0.35, 5),
                 onda(880, 0.07, "seno", 0.35, 5),
                 onda(1320, 0.18, "seno", 0.35, 6)))

    guardar("sonidos/subir_nivel.wav",
            unir(onda(523, 0.09, "cuadrada", 0.32, 4),
                 onda(659, 0.09, "cuadrada", 0.32, 4),
                 onda(784, 0.09, "cuadrada", 0.32, 4),
                 onda(1046, 0.30, "cuadrada", 0.34, 5)))

    guardar("sonidos/boton.wav", onda(1200, 0.05, "cuadrada", 0.22, 25))

    guardar("sonidos/victoria.wav",
            unir(onda(523, 0.13, "cuadrada", 0.34, 3),
                 onda(659, 0.13, "cuadrada", 0.34, 3),
                 onda(784, 0.13, "cuadrada", 0.34, 3),
                 onda(1046, 0.16, "cuadrada", 0.34, 3),
                 onda(784, 0.10, "cuadrada", 0.30, 3),
                 onda(1046, 0.55, "cuadrada", 0.36, 3)))

    guardar("sonidos/derrota.wav",
            unir(onda(392, 0.18, "sierra", 0.34, 3),
                 onda(330, 0.18, "sierra", 0.34, 3),
                 onda(262, 0.20, "sierra", 0.34, 3),
                 onda(196, 0.70, "sierra", 0.36, 3)))


# -------------------------------------------------------------------- música

NOTAS = {"do": 262, "re": 294, "mi": 330, "fa": 349, "sol": 392,
         "la": 440, "si": 494, "do5": 523, "mi5": 659, "la5": 880}


def hacer_musica():
    """Un loop corto de 8 segundos: bajo + arpegio + batería simple."""
    print("Música:")
    pulso = 0.25                      # duración de una corchea
    # cuatro acordes: La menor, Fa, Do, Sol
    acordes = [("la", ["la", "do5", "mi5"]),
               ("fa", ["fa", "la", "do5"]),
               ("do", ["do", "mi", "sol"]),
               ("sol", ["sol", "si", "re"])]

    bajo = []
    arpegio = []
    bateria = []
    for raiz, notas_acorde in acordes:
        for paso in range(8):                       # 8 corcheas por acorde
            frecuencia_bajo = NOTAS[raiz] / 2
            bajo.extend(onda(frecuencia_bajo, pulso, "cuadrada", 0.22, 3.0))

            nota = notas_acorde[paso % len(notas_acorde)]
            arpegio.extend(onda(NOTAS[nota], pulso, "cuadrada", 0.13, 5.0))

            if paso % 4 == 0:                        # bombo
                golpe = onda(120, pulso, "seno", 0.5, 18, 45)
            elif paso % 4 == 2:                      # redoblante
                golpe = onda(300, pulso, "ruido", 0.16, 26)
            else:                                    # hi-hat
                golpe = onda(900, pulso, "ruido", 0.05, 60)
            bateria.extend(golpe)

    guardar("musica/arena.wav", mezclar(bajo, arpegio, bateria))


if __name__ == "__main__":
    print("Generando los recursos de audio de Arena de Combate...")
    hacer_efectos()
    hacer_musica()
    print("Listo. Los archivos quedaron en assets/")
