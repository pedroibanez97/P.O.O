# Programación Orientada a Objetos

Presentaciones interactivas de POO, pensadas para estudiantes que hasta ahora
solo trabajaron con Python.

## 🔗 Abrir las presentaciones

**https://pedroibanez97.github.io/P.O.O/**

Ese link es la página de inicio con todas las clases. Se abre en cualquier
navegador, en compu o en celular. No hay que instalar nada.

| Clase | Tema | Link directo |
|-------|------|--------------|
| 1 | Pensar en objetos | https://pedroibanez97.github.io/P.O.O/clase-1.html |
| 2 | Relacionar objetos | https://pedroibanez97.github.io/P.O.O/clase-2.html |
| TP | Arena de Combate (integrador) | https://pedroibanez97.github.io/P.O.O/tp-arena-de-combate.html |
| TP | Apunte del TP (para imprimir) | https://pedroibanez97.github.io/P.O.O/apunte-tp-arena-de-combate.pdf |

---

## Para los alumnos

Usá las flechas del teclado para avanzar, o tocá la pantalla si estás en el celular.

Muchas diapositivas tienen una **pregunta antes de la respuesta**: pensala primero,
después avanzá para ver si coincidías.

| Tecla | Qué hace |
|-------|----------|
| `→` o espacio | Avanzar |
| `←` | Volver |
| `O` | Ver el índice completo y saltar a una parte |
| `F` | Pantalla completa |

La **tarea** está en las últimas diapositivas de cada clase.

El **trabajo práctico integrador** (Arena de Combate) es una guía aparte: se avanza con los botones
de abajo o con `←` `→`, y el progreso se guarda solo en esa computadora.

---

## Para el profesor

Cada diapositiva tiene notas de guion: qué mostrar, qué preguntar, qué respuesta
esperar y en qué momento revelar. Se abren con la tecla `N`.

| Tecla | Qué hace |
|-------|----------|
| `N` | Abrir/cerrar las notas del profesor |
| `O` | Índice por bloque |
| `L` | Bloquear el avance por clic (para señalar con el mouse sin pasar de diapositiva) |
| `F` | Pantalla completa |
| `↓` `↑` | Saltar de diapositiva entera, sin pasar por los reveals |

El reloj de la barra inferior arranca solo en el primer avance; se reinicia con un clic.

Las diapositivas marcadas con **◇ opcional** se pueden saltear si vas corto de tiempo,
sin perder el hilo. Cada una explica en sus notas qué hacer en su lugar.

### Clase 1 · Pensar en objetos

De los datos y las funciones sueltos a los objetos. 52 diapositivas.

| Bloque | Contenido |
|--------|-----------|
| 1 | Cambiamos la forma de pensar — de datos y funciones sueltos a objetos |
| 2 | Pensar en objetos — atributos, métodos, clase vs. objeto |
| 3 | Python — primera clase, `__init__`, `self`, métodos que modifican el objeto |
| 4 | Los 4 pilares — encapsulación, herencia, polimorfismo y abstracción, con código |
| 5 | Diseñemos un videojuego — los cuatro pilares aplicados entre todos |
| 6 | Cierre y tarea |

Duración estimada: 70–95 minutos de exposición, más el tiempo de las actividades.

### Clase 2 · Relacionar objetos

Continuación directa de la clase 1: ya sabemos pensar en objetos, ahora los
hacemos trabajar juntos. 56 diapositivas.

| Bloque | Contenido |
|--------|-----------|
| 1 | Recuperamos lo aprendido — qué objetos hay acá, quiz relámpago |
| 2 | `super()` — el problema de repetir código y cómo el hijo agrega lo suyo |
| 3 | Herencia en varios niveles — lo heredado se transmite hacia abajo |
| 4 | `print()` vs `return` — mostrar no es lo mismo que entregar |
| 5 | Objetos dentro de objetos — ES UN (herencia) vs TIENE UN (composición) |
| 6 | Lo juntamos todo — Personaje → Jugador que tiene un Arma, paso a paso |
| 7 | Desafío final, resumen, tarea y cierre |

Duración estimada: 75–100 minutos de exposición, más el tiempo de las actividades.

### TP integrador · Arena de Combate

Trabajo práctico que cierra las dos clases: los alumnos construyen un juego de combate por turnos
en Python, de a una etapa por vez. Individual o en parejas de hasta dos personas.

| Etapa | Qué se construye | Concepto que entra |
|-------|------------------|--------------------|
| 0 | La misión | cómo se trabaja |
| 1 | Encontrar los objetos | objeto, atributos, métodos |
| 2 | Tabla de diseño | qué va en cada clase |
| 3 | `Personaje` | `__init__`, `self`, `return`, encapsulación |
| 4 | `Arma` | clase vs objeto, `print()` vs `return` |
| 5 | `Jugador` | herencia, `super()`, composición |
| 6 | `Enemigo` | segunda clase hija |
| 7 | `Guerrero` | herencia de varios niveles |
| 8 | `Dragon` y `Goblin` | polimorfismo |
| 9 | La pelea | el `while`, todo junto |
| 10 | Experiencia y niveles | información y comportamiento nuevos |
| 11 | El menú y el programa completo | `Pocion`, `input()`, `if`/`elif` |
| 12 | Desafíos de ampliación | 5 niveles, de fácil a difícil |
| 13 | Cierre | checklist, reflexión, entrega y rúbrica |

Cada etapa arranca con una **pregunta antes de la respuesta** y las soluciones quedan bloqueadas
hasta que el alumno intenta la actividad. Incluye 38 actividades corregidas automáticamente
(elegir, clasificar, ordenar, unir, completar código, predecir), tres simuladores que corren en el
navegador (la vida en negativo, el combate y la subida de nivel), la consigna de entrega y la rúbrica.

Se puede hacer en casa, entero, sin el profesor al lado.

**El apunte imprimible.** El mismo trabajo práctico en formato apunte, con el diseño de los apuntes de
las clases 1 y 2: `apunte-tp-arena-de-combate.html` (con botón de imprimir) y su PDF ya generado, de
37 páginas. Además de la consigna y el código, suma una sección de **teoría de repaso** con diez fichas
(clase y objeto, atributos y métodos, `__init__`, `self`, herencia, `super()`, varios niveles,
`print()` vs `return`, composición y polimorfismo), una de **ayudas** con los seis errores frecuentes
(síntoma → causa → cómo salir), las soluciones de todos los ejercicios al final y un **machete de una
carilla**.

Para regenerar el PDF después de editar el HTML: abrirlo y usar el botón *Imprimir / Guardar PDF*
(A4, sin encabezados).

---

## Uso sin internet

Descargá el `.html` de la clase y abrilo con doble clic. Funciona igual; lo único
que cambia es la tipografía, que se carga desde internet.

## Archivos

| Archivo | Qué es |
|---------|--------|
| `index.html` | Página de inicio con el listado de clases |
| `clase-1.html` | Presentación de la clase 1 |
| `clase-2.html` | Presentación de la clase 2 |
| `tp-arena-de-combate.html` | Trabajo práctico integrador (guía interactiva) |
| `apunte-tp-arena-de-combate.html` | Apunte imprimible del TP |
| `apunte-tp-arena-de-combate.pdf` | El mismo apunte, ya en PDF (37 páginas) |

Cada presentación es un único archivo HTML, sin dependencias más allá de las
tipografías de Google Fonts.
