# Arena de Combate · el mismo juego, tres veces

Tres versiones del **mismo** videojuego, para ver cómo un proyecto crece sin
tirar nada de lo aprendido.

```
VERSIÓN 1                VERSIÓN 2                VERSIÓN 3
Arena de Combate    →    Arena de Combate    →    Arena de Combate
CONSOLA                  TKINTER                  PYGAME
```

La versión 1 es la implementación modelo del TP `tp-arena-de-combate.html`.
Las otras dos son **la misma lógica** con más interfaz encima.

---

## Cómo se ejecutan

| Versión | Comando | Necesita |
|---|---|---|
| 1 · Consola | `python3 juego_consola.py` | nada (Python puro) |
| 2 · Tkinter | `python3 juego_tkinter.py` | tkinter (viene con Python) |
| 3 · Pygame | `python3 juego_pygame.py` | `pip install pygame` |

> **Si la versión 2 no abre** y dice `ModuleNotFoundError: No module named '_tkinter'`,
> ese Python fue compilado sin Tk. En macOS con Homebrew se arregla con
> `brew install python-tk@3.13`; en Linux, con `sudo apt install python3-tk`.
> Las versiones 1 y 3 no se ven afectadas.

### En la compu donde se preparó esto

Ya está todo listo: hay un entorno en `POO-profe/.venv` con **tkinter y pygame**
funcionando. Los tres juegos se corren con ese Python.

**Desde VS Code (lo más cómodo para la clase)**

1. Abrí el archivo que quieras mostrar.
2. Abajo a la derecha, donde dice la versión de Python, elegí el intérprete
   `.venv` (aparece como *Python 3.13.15 ('.venv': venv)*). Se hace una sola vez.
3. Botón ▶ *Run Python File*.

**Desde la terminal**

```bash
cd ~/Desktop/POO-profe/arena-de-combate
../.venv/bin/python juego_consola.py
../.venv/bin/python juego_tkinter.py
../.venv/bin/python juego_pygame.py
```

**Por qué no alcanza con escribir `python3`:** en esta compu `python3` es el de
pyenv 3.12.3, que se instaló sin tkinter y sin pygame. Y el Python del sistema
(`/usr/bin/python3`) trae un Tk viejo que en macOS 15 directamente hace crashear
la app ("error inesperado… ¿desea reiniciar?"). Por eso usamos el `.venv`, que
sale del Python de Homebrew y tiene las dos librerías al día.

---

## VERSIÓN 1 · `juego_consola.py`

El TP, tal cual. Se juega escribiendo números en la terminal.

**Las clases**

| Clase | Atributos | Métodos |
|---|---|---|
| `Personaje` | `nombre`, `vida`, `vida_maxima` | `recibir_danio()`, `esta_vivo()`, `mostrar_info()` |
| `Arma` | `nombre`, `danio` | `usar()` |
| `Pocion` | `nombre`, `cura` | `usar()` |
| `Jugador(Personaje)` | `arma`, `nivel`, `experiencia` | `atacar()`, `curarse()`, `ganar_experiencia()`, `subir_nivel()` |
| `Enemigo(Personaje)` | `danio` | `atacar()` |
| `Goblin(Enemigo)` | — | `atacar()` |
| `Dragon(Enemigo)` | — | `atacar()` |

```
                 Personaje
          nombre · vida · vida_maxima
        recibir_danio() · esta_vivo()
              ▲                 ▲
           ES UN             ES UN
              │                 │
          Jugador            Enemigo
      arma · nivel · exp       danio
           ◆                  ▲     ▲
      TIENE UN            ES UN   ES UN
           │                  │     │
      Arma / Pocion        Goblin  Dragon
```

**Dónde está cada concepto de POO**

| Concepto | Dónde |
|---|---|
| Herencia | `class Jugador(Personaje)`, `class Enemigo(Personaje)`, `class Goblin(Enemigo)` |
| `super()` | `super().__init__(nombre, vida)` en `Jugador` y en `Enemigo` |
| Composición | `self.arma = arma`, y después `self.arma.usar()` |
| Polimorfismo | `Goblin.atacar()` devuelve `danio`; `Dragon.atacar()` devuelve `danio + 15` |
| `return` | `esta_vivo()` (lo usa el `if`), `atacar()` y `usar()` (entregan el daño) |
| Encapsulación | el `if self.vida < 0` dentro de `recibir_danio()`, y el tope de `curarse()` |
| `print()` | `mostrar_info()` y los mensajes del menú: eso lo lee una persona |

**Cómo funciona**

Un menú de 5 opciones (ver información, atacar, poción, experiencia, salir).
Atacar hace dos cosas: el héroe le pide el daño al arma y el enemigo se lo
resta; si el enemigo sigue vivo, contraataca. La partida termina con `GAME OVER`
si cae el héroe, o con victoria si cae el enemigo. Cualquier opción que no
exista cae en el `else` y avisa: ésa es la validación de la entrada.

> **Sobre el balance:** con los números del TP (héroe 150 de vida, dragón 90 de
> vida y 35 de daño) el héroe gana en 4 ataques. Para ver la pantalla de derrota,
> subile la vida al dragón: `Dragon("Dragón rojo", 400, 20)`. Eso es balancear un
> juego, y es la propuesta de la etapa 9 del TP.

---

## VERSIÓN 2 · `juego_tkinter.py`

El mismo combate, ahora con ventana. **Las clases no cambian de forma**: siguen
la misma herencia, la misma composición y el mismo polimorfismo.

**Lo que agrega la clase 3**

- `import` de tres librerías: `random`, `time` y `tkinter`.
- `random.randint()` → el arma hace daño variable (un rango, no un número fijo).
- `random.randint()` → 20 % de golpes críticos, que pegan el doble.
- `random.choice()` → decide quién ataca primero.
- `random.shuffle()` → mezcla el orden de los rivales.
- `time.time()` → cronometra cuánto duró el combate.
- `ventana.after()` → el contraataque tarda un momento y las barras de vida
  bajan suave. **En una interfaz no se usa `time.sleep()`**: congelaría la
  ventana entera. Ése es el detalle que conviene mostrar en clase.

**Lo que agrega la interfaz**

Pantalla de inicio (nombre + elección de arma), arena dibujada en un `Canvas`,
barras de vida y de experiencia, números de daño flotantes, registro de
mensajes, y pantallas de victoria y derrota con estadísticas.

**Cómo se reparte el trabajo**

- Las clases del juego (arriba del archivo) saben de vida, daño y niveles.
- La clase `ArenaDeCombate` (abajo) sólo dibuja y traduce clics en órdenes.
- El puente es siempre el mismo: un botón llama a un método que ya existía.
  `danio = self.heroe.atacar()` es exactamente la línea de la versión 1.

Se pelea contra 3 rivales seguidos (`Goblin`, `Esqueleto` y `Dragon`), así que
acá sí se llega a la subida de nivel.

---

## VERSIÓN 3 · `juego_pygame.py`

Un juego de acción completo, con el mismo árbol de clases.

**Controles:** `W A S D` o flechas para moverse · mouse para apuntar ·
clic o barra espaciadora para atacar · `P` o `ESC` para pausar.

**Lo que suma Pygame**

| | |
|---|---|
| ventana y FPS | `set_mode()`, `Clock.tick(60)` |
| superficies | el escenario se dibuja una vez y se pega entero en cada cuadro |
| dibujo | todos los personajes salen de `pygame.draw` (no hay imágenes externas) |
| animaciones | cada personaje es una **lista de imágenes** + `get_ticks()` |
| sprites y grupos | `Personaje` hereda de `pygame.sprite.Sprite`; los enemigos viven en un `Group` |
| colisiones | `groupcollide()`, `spritecollide()` y `Rect.colliderect()` contra los muros |
| teclado y mouse | `key.get_pressed()` para moverse, eventos para disparar |
| sonido y música | `mixer.Sound` para los efectos, `mixer.music` para el loop de fondo |
| estados | menú · controles · transición · jugando · pausa · victoria · derrota |
| HUD | vida, experiencia, nivel, puntaje, oleada y **minimapa** |
| efectos | partículas, números de daño, temblor de pantalla, tinte rojo al recibir daño |
| niveles | 3 mapas distintos, con 3 oleadas cada uno y un **jefe final** |

**Lo que sigue siendo del TP**

`Personaje` → `Jugador` / `Enemigo`, `super()`, `self.arma = arma`,
`atacar()` que devuelve un número, `recibir_danio()` con su `if`, `esta_vivo()`,
`ganar_experiencia()` y `subir_nivel()` (que además llama a `arma.mejorar()`,
la pista de la etapa 10).

**El polimorfismo, ahora en serio:** el bucle principal hace
`for enemigo in self.enemigos: enemigo.actualizar(...)` y cada clase se comporta
distinto — el `Goblin` corre de frente, el `Esqueleto` mantiene distancia y tira
huesos, el `Dragon` escupe tres bolas de fuego y el `JefeFinal` suelta una ronda
en todas las direcciones. **En ese `for` no hay un solo `if`** preguntando qué
tipo de enemigo es.

---

## Los recursos (`assets/`)

```
assets/
├── generar_sonidos.py     ← fabrica los .wav con Python puro
├── sonidos/*.wav          ← 10 efectos
└── musica/arena.wav       ← loop de 8 segundos
```

Nada se bajó de internet: **no hay problemas de licencia y no falta ningún
archivo**. Los gráficos se dibujan con `pygame.draw` al arrancar el juego y los
sonidos los generó `generar_sonidos.py` con las librerías `wave` y `math`. Si
los `.wav` no estuvieran, el juego igual corre: se queda mudo y sigue andando.

---

## Comparación de las tres versiones

```
VERSIÓN 1 · Consola  → aprendemos POO y lógica.
VERSIÓN 2 · Tkinter  → incorporamos librerías e interfaz gráfica.
VERSIÓN 3 · Pygame   → construimos una experiencia de videojuego completa.
```

**Qué se mantiene en las tres**

Las clases y sus relaciones. `Personaje` arriba con lo común; `Jugador` y
`Enemigo` heredando; `super()` para no repetir; `Arma` y `Pocion` metidas
adentro por composición; `atacar()` y `usar()` devolviendo el daño con `return`;
`recibir_danio()` cuidando que la vida no baje de cero; y cada enemigo
respondiendo `atacar()` a su manera.

**Qué aparece en cada etapa**

| | Versión 1 | Versión 2 | Versión 3 |
|---|---|---|---|
| Interfaz | `print()` e `input()` | ventana, botones, Canvas | ventana de juego a 60 FPS |
| Azar | no | daño variable, críticos, quién empieza | + drops, oleadas, patrones |
| Tiempo | no | `after()` y cronómetro | `Clock`, temporizadores, animaciones |
| Personaje | un dato en memoria | un dibujo en la pantalla | un sprite que se mueve y choca |
| Enemigos | 1 por partida | 3, uno tras otro | 47 en 9 oleadas + jefe final |
| Mapa | no hay | un escenario de fondo | 3 niveles con obstáculos y minimapa |
| Sonido | no | no | 10 efectos + música |
| Fin de partida | GAME OVER / victoria | pantallas con estadísticas | + puntaje, tiempo y reinicio |

Es el mismo conocimiento, tres veces, cada vez con más herramientas alrededor.

---

## Para seguir (y que empiecen a preguntar "¿y si yo agrego…?")

- Un arma nueva: es **una línea**, y no toca la clase `Jugador`.
- Un enemigo nuevo: heredá de `Enemigo` y escribile su `atacar()`. El `for` del
  combate no se toca. Probalo: agregá un `Fantasma` en 5 líneas.
- Un nivel nuevo en Pygame: agregá un `Nivel` más a la lista de `crear_niveles()`.
- Un `Inventario` (desafío 4 del TP), una `Tienda` con monedas (desafío 5),
  pociones con usos limitados en las tres versiones.
- ¿Y si el enemigo esquiva? ¿Y si el arma tiene munición? ¿Y si hay dos
  jugadores? Todas esas preguntas se contestan igual: *¿qué objetos hay, qué
  información tienen, qué pueden hacer y cómo se relacionan?*
