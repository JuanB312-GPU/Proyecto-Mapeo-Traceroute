from flask import Flask, render_template, request, render_template_string
import folium as maps
from folium.plugins import MarkerCluster
import pandas as pd
import requests

# Variables globales.
hops = []
num_hops = 0
initial_ip = ''
final_ip = ''
country = ''
time = 0

# Formatea los saltos para mandarlos a pantalla.
def format_hops(hops):
    
    hops_concatenated = []
    for index,hop in enumerate(hops):
        concatenated_hop = '{}. '.format(index+1) + hop
        hops_concatenated.append(concatenated_hop)
        
    if hops[-1] == "Desconocido":
       hops_concatenated[-1] = hops_concatenated[-1] + "-giy initPunto Muerto"
        
    hops = hops_concatenated
    

    
    return hops
    

# Lee la data en el archivo de excel.
def read_data():
    
    df = pd.read_excel("data/coordinates.xlsx")
    
    return df

# Obtiene los datos iniciales para el sitio web.
def generator_datalists(df):
    
    websites = [df.iloc[0,0],df.iloc[1,0],df.iloc[2,0]]
    servers = df.columns.tolist()
    del servers[0]
    
    return servers,websites
    
# Realiza las consultas de trazas.
def ip_information(server,website):
    
    latitudes = [] 
    longitudes = [] 
    data = []
    
    df = read_data()
    
    # Obtener el tiempo promedio.
    time_cell = df.loc[4, server] 
    time_list = time_cell.split(",")
    time = time_list[website]
    
    # Obtener estado de salida.
    country = df.loc[3, server] 
    
    # Obtiene todas los saltos.
    string_cell = df.loc[website, server] 
    ip_list = string_cell.split(",")
    num_hops = len(ip_list)
    
    hops = []
    for index,hop in enumerate(ip_list):
        if hop == " vacio":
            hop = "Desconocido"
        hops.append(hop)
    hops = [cell.strip() for cell in hops]
    
    # Se ignoran los saltos nulos, para la consulta a la API.
    ip_list = [item for item in ip_list if item != " vacio"]
    # Se quitan espacios en blanco.
    ip_list = [cell.strip() for cell in ip_list]
    
    # Ip inicial y final
    initial_ip = ip_list[0]
    final_ip = ip_list[-1]
    
    # Se realiza la consulta a la API.
    queries = [{"query": ip} for ip in ip_list]
    ip_ping = requests.post("http://ip-api.com/batch", json=queries).json()
    for index,ip_info in enumerate(ip_ping):
        pindex = hops.index(ip_info['query'])
        if ip_info['status'] != 'fail':    
            latitudes.append(ip_info['lat'])
            longitudes.append(ip_info['lon'])
            data.append([ip_info['query'],ip_info['country'],ip_info['as'], pindex])
        else:
            hops[index] = hops[index] + ' (Privada)'
        
    routes(latitudes,longitudes,data)
    
    return {
        'num_hops': num_hops,
        'initial_ip': initial_ip,
        'final_ip': final_ip,
        'country': country,
        'time': time,
        'hops': format_hops(hops)
    }

# Se encarga de generar un html que contiene el mapa interactivo.
def routes(latitudes,longitudes,data):
  
    map = maps.Map(location=[latitudes[0],longitudes[0]], zoom_start=5)
    
    # Crear un MarkerCluster, usado para agrupar ubicaciones muy cercanas entre si.
    marker_cluster = MarkerCluster().add_to(map)
    stations = [] 
    
    for i in range (len(latitudes)):
        if latitudes[i] != 0:    
            stations.append([latitudes[i],longitudes[i]])
        
    # Rellena los marcadores.
    for index,latitude in enumerate(latitudes):        
            if latitude!=0:
                maps.Marker([latitude, 
                           longitudes[index]],
                          popup=('Salto #{}'.format(data[index][3]+1) + '\n IP:{}'.format(data[index][0]) + '\n Estado: {}'.format(data[index][1]) +
                                 '\n Nombre: {}'.format(data[index][2]))
                          ,icon = maps.Icon(color='blue',icon_color='white',prefix='fa', icon='globe')
                          ).add_to(marker_cluster)
                
    maps.PolyLine(stations, color='red', dash_array='5', opacity='.85', tooltip='Server Tunneling').add_to(map)
        
    map.save("templates/mapa.html")
    
app = Flask(__name__)

@app.route('/mapa')
def map_html():
    with open("templates/mapa.html", "r", encoding="utf-8") as f:
        mapa_html = f.read()
    return render_template_string(mapa_html)

@app.route('/inicio', methods = ['GET','POST'])
def initial():
    
    # Llamado de la data inicial, servidores y sitios web para elegir.
    servers_list, websites_list =  generator_datalists(read_data())
    message = 'Ingrese los datos por favor'
    
    # Operaciones en caso de entrada de datos.
    if request.method == 'POST':
            
        server = request.form['Server']
        website = websites_list.index(request.form['Website'])
        info = ip_information(server,website)
        message = request.form['Server'] + ' - ' + request.form['Website']
        return render_template('index.html', options_sever = servers_list , options_web = websites_list, message = message,
                           num_hops=info['num_hops'], 
                           initial_ip=info['initial_ip'], 
                           final_ip=info['final_ip'], 
                           country=info['country'], 
                           time=info['time'], 
                           hops=info['hops']
                           )
    
    # Salida del sitio web en su forma base.
    return render_template('index.html', options_sever = servers_list , options_web = websites_list, message = message) 