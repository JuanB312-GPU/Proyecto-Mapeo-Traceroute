# Proyecto de Mapeo de Trazas con Flask

Este proyecto permite mapear trazas de IPs o dispositivos en un mapa interactivo usando Flask y Folium. Las trazas pueden ser visualizadas en tiempo real en un navegador, donde se agrupan geogr�ficamente si est�n cercanas entre s�, y se muestran en un mapa interactivo.

## Caracter�sticas

- **Mapeo Interactivo**: Utiliza Folium para mostrar un mapa con las ubicaciones geogr�ficas de las IPs o dispositivos.
- **Agrupamiento de Marcadores**: Cuando varias IPs o dispositivos est�n muy cerca geogr�ficamente, se agrupan en un solo marcador.
- **Flask para Backend**: El proyecto usa Flask para servir la aplicaci�n web y manejar las solicitudes.
- **Cargar trazas**: Los datos de trazas pueden ser cargados desde un archivo o a trav�s de una API.

## Requisitos Previos

Aseg�rate de tener instalados los siguientes paquetes antes de comenzar:

- Python 3.x
- Flask
- Folium

Puedes instalarlos usando pip:

```bash
pip install flask folium
