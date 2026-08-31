# VELUM — Referencia de color

Fondo principal **Blanco Hueso `#F4F0EE`**. El sistema es claro: el azul ancla, el oro acentúa.

## Valores

| Token | ES | EN | HEX | RGB | CMYK | Uso |
|---|---|---|---|---|---|---|
| `blanco-hueso` | Blanco Hueso | Bone White | `#F4F0EE` | 244, 240, 238 | 0 / 2 / 2 / 4 | Fondo principal. Toda superficie parte de aquí. |
| `azul-velum` | Azul Velum | Velum Blue | `#0B1D34` | 11, 29, 52 | 79 / 44 / 0 / 80 | Tinta principal, paneles oscuros y piezas de firma. |
| `oro-velum` | Oro Velum | Velum Gold | `#D4AF37` | 212, 175, 55 | 0 / 17 / 74 / 17 | Acento único: la estrella, un filete, una palabra. |
| `crema` | Crema | Cream | `#E8DCC0` | 232, 220, 192 | 0 / 5 / 17 / 9 | Superficie cálida: etiquetas, estuches, paneles suaves. |
| `azul-medio` | Azul Medio | Mid Blue | `#20344D` | 32, 52, 77 | 58 / 32 / 0 / 70 | Segundo azul. Bloques, sellos, fondos secundarios. |
| `oro-oscuro` | Oro Oscuro | Deep Gold | `#B8912B` | 184, 145, 43 | 0 / 21 / 77 / 28 | El oro cuando funciona como texto sobre fondo claro. |
| `gris-perla` | Gris Perla | Pearl Grey | `#DADDE3` | 218, 221, 227 | 4 / 3 / 0 / 11 | La V sobre fondos oscuros. Líneas y detalles. |
| `gris` | Gris | Grey | `#55585F` | 85, 88, 95 | 11 / 7 / 0 / 63 | Texto secundario y pies sobre hueso. |
| `negro` | Negro | Black | `#1A1A1A` | 26, 26, 26 | 0 / 0 / 0 / 90 | Tinta alternativa, una tinta, grabado. |

## Proporción

| Peso | Color | Papel |
|---|---|---|
| 60% | Blanco Hueso | Superficie. Fondo y espacio negativo. |
| 22% | Azul Velum | Ancla. Tipografía, paneles y piezas de firma. |
| 10% | Crema | Calidez. Etiquetas, estuches, paneles suaves. |
| 5% | Oro Velum | Acento. Una sola aparición por pieza. |
| 3% | Azul Medio | Apoyo. Sellos y bloques secundarios. |

## Contraste (WCAG) — texto sobre fondo

| texto \ fondo | `blanco-hueso` | `azul-velum` | `oro-velum` | `crema` | `azul-medio` | `oro-oscuro` | `gris-perla` | `gris` | `negro` |
|---|---|---|---|---|---|---|---|---|---|
| `blanco-hueso` | 1.0 fail | 14.96 AAA | 1.86 fail | 1.20 fail | 11.17 AAA | 2.60 fail | 1.20 fail | 6.29 AA | 15.37 AAA |
| `azul-velum` | 14.96 AAA | 1.0 fail | 8.06 AAA | 12.45 AAA | 1.34 fail | 5.75 AA | 12.45 AAA | 2.38 fail | 1.03 fail |
| `oro-velum` | 1.86 fail | 8.06 AAA | 1.0 fail | 1.55 fail | 6.02 AA | 1.40 fail | 1.55 fail | 3.39 AA-lg | 8.28 AAA |
| `crema` | 1.20 fail | 12.45 AAA | 1.55 fail | 1.0 fail | 9.30 AAA | 2.17 fail | 1.00 fail | 5.23 AA | 12.79 AAA |
| `azul-medio` | 11.17 AAA | 1.34 fail | 6.02 AA | 9.30 AAA | 1.0 fail | 4.29 AA-lg | 9.30 AAA | 1.78 fail | 1.38 fail |
| `oro-oscuro` | 2.60 fail | 5.75 AA | 1.40 fail | 2.17 fail | 4.29 AA-lg | 1.0 fail | 2.17 fail | 2.42 fail | 5.90 AA |
| `gris-perla` | 1.20 fail | 12.45 AAA | 1.55 fail | 1.00 fail | 9.30 AAA | 2.17 fail | 1.0 fail | 5.24 AA | 12.79 AAA |
| `gris` | 6.29 AA | 2.38 fail | 3.39 AA-lg | 5.23 AA | 1.78 fail | 2.42 fail | 5.24 AA | 1.0 fail | 2.44 fail |
| `negro` | 15.37 AAA | 1.03 fail | 8.28 AAA | 12.79 AAA | 1.38 fail | 5.90 AA | 12.79 AAA | 2.44 fail | 1.0 fail |

AA = 4.5:1 para texto corrido. AAA = 7:1. AA-lg = 3:1, solo 24 px+ o 19 px en negrita.

> El Oro Velum `#D4AF37` **no pasa AA sobre hueso** (2.0:1). Como texto sobre fondo claro se usa
> Oro Oscuro `#B8912B`; el Oro Velum queda para gráficos, filetes y la estrella.

## Reglas

1. El hueso es el punto de partida de toda pieza; el azul entra como ancla, no como fondo por defecto.
2. El oro nunca cubre una superficie grande: es acento.
3. El logotipo va siempre en un solo color de la paleta.
4. Sobre foto o textura, el logotipo se coloca en la zona más limpia.
5. Hueso y crema no compiten: una pieza elige una superficie clara y la sostiene.
