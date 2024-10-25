# Proyecto de Mapeo de Trazas con Flask

Este proyecto permite mapear trazas de IPs o dispositivos en un mapa interactivo usando Flask y Folium. Las trazas pueden ser visualizadas en tiempo real en un navegador, donde se agrupan geográficamente si están cercanas entre sí, y se muestran en un mapa interactivo.

## Características

- **Mapeo Interactivo**: Utiliza Folium para mostrar un mapa con las ubicaciones geográficas de las IPs o dispositivos.
- **Agrupamiento de Marcadores**: Cuando varias IPs o dispositivos están muy cerca geográficamente, se agrupan en un solo marcador.
- **Flask para Backend**: El proyecto usa Flask para servir la aplicación web y manejar las solicitudes.
- **Cargar trazas**: Los datos de trazas pueden ser cargados desde un archivo o a través de una API.

## Requisitos Previos

Asegúrate de tener instalados los siguientes paquetes antes de comenzar:

- Python 3.x
- Flask
- Folium

Puedes instalarlos usando pip:

```bash
pip install flask folium
