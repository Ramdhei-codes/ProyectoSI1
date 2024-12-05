# Proyecto Bomberman con Algoritmos de Búsqueda No Informada

Este proyecto implementa una simulación de **Bomberman** utilizando **algoritmos de búsqueda no informada** como **Búsqueda por Anchura (BFS)**, **Búsqueda por Profundidad (DFS)** y **Búsqueda por Costo Uniforme (UCS)**. Está desarrollado utilizando **Mesa**, un framework para simulaciones basadas en agentes.

## Descripción General

El objetivo del proyecto es simular el comportamiento de **Bomberman**, que se mueve en un mapa 2D en busca de la salida, utilizando diferentes **algoritmos de búsqueda no informada**. El mapa contiene diversos obstáculos como **metales** y **rocas** que Bomberman debe evitar. La salida está oculta debajo de una roca especial, y el objetivo de Bomberman es encontrar la salida.

Los algoritmos de búsqueda utilizados son:
- **Búsqueda por Anchura (BFS)**
- **Búsqueda por Profundidad (DFS)**
- **Búsqueda por Costo Uniforme (UCS)**

Los usuarios pueden seleccionar el algoritmo a utilizar desde la **interfaz gráfica** antes de comenzar la simulación.

## Características

- Carga de **mapas personalizados** desde archivos de texto.
- **Posicionamiento dinámico** de Bomberman en el mapa basado en la casilla marcada como `C_b`.
- Visualización en tiempo real de las **casillas exploradas** por los algoritmos, con numeración que refleja el orden de visita.
- Selección dinámica de **algoritmos de búsqueda** desde la interfaz gráfica.
- **Simulación autónoma** donde Bomberman recorre el mapa sin intervención del usuario.

## Instalación

Sigue los siguientes pasos para instalar el proyecto:

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/proyecto-bomberman.git
cd proyecto-bomberman
```


### 2. Ejecutar 

```bash
py main.py 
```
