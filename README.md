# hidroUH

Plugin de QGIS que permite estimar el caudal superficial generado por un evento de precipitación a nivel de cuenca (de forma agregada o mediante la esquematización de la cuenca en subcuencas). Para ello, utiliza el método del número del curva (CN) del Soil Conservation Service (SCS) para aproximar la fase de pérdidas (separación entre la Precipitación Neta (Pn) y la precipitación que no genera escorrentía superficial), el hidrograma unitario del SCS para conversión lluvia-escorrentía y el méteodo de Múskingum para la translación en cauce.

To report failures or make suggestions, please contact [fjgomariz@um.es](mailto:fjgomariz@um.es  "fjgomariz@um.es ") 

**Acknowledgments**: This work was supported by the Spanish Agencia Estatal de Investigación (Grant number TED2021-131131B-I00).

<img src="img/logoINUAMA.png" width="400px" height="auto">

- **Autores**: , Gabriel Molina-Pérez y Carmen Valdivieso-Ros
- **Version**: 0.1
- **Fecha**: 30 de Mayo de e2025

## 1. Plugin installation and requirements

Para instalar el plugin se debe descargar en formato zip desde este repositorio, tras lo cuál se instalará en QGIS a través del menú *Plugin -> Manage and Install Plugin ...* Una vez dentro de la ventana de gestión de plugin, se instalará con la opción *Install from ZIP*.

Tras su instalación se puede acceder a través del menú Plugin (Fig.1) o con el botón de la barra de herramientas <img src="img/icon.png" width="15px" height="auto">

<img src="img/access.png" width="400px" height="auto">


###Requeriments



## 2. Using plugin

La interfaz de usuario del plugin se divide en tres secciones: Model, donde se introducen los datos de entrada requeridos para su ejecución, Results, que muestra un resumen de los resultados (los resultados de detalle se generarán en el directorio de salida del plugin), y Help, con una manual de ayuda. 

### 2.1. Model (input data)

En la primera pestaña (Fig.1) se deben introducir los datos de entrada (el <span style=" color:#ff0000;"> *</span> indica que son necesarios, mientras que el resto son optativos).

<img src="img/form1.png" width="500px" height="auto">

Los archivos de entrada con datos en forma de capa vectorial y/o serie temporal son:

- **Subbasins**: Layer tipo polígono cargado previamente en QGIS de la cuenca (o subcuencas). En esta capa se incluirán os parámetros en forma de columna, representando las características de éstas. Los elementos tipo *ComboBox* (listas deplegables) de la zona *Parameters* representan el nombre de las columnas que se introducirán como parámetros del modelo.
- **Precipitation (mm/h)**: Archivo tipo csv con la precipitación de entrada. El formato que debe tener es: Una primera columna almacenando la fecha y hora, y tantas columnas como subcuencas se quieran incluir en el modelo, incluyendo como nombre de ésta el código de la cuenca o subcuenca. El separador de columnas será *comma* y el símbolo decimal *point*.
- **Flow (m3/s by hour)**: Archivo en formato csv (con las mismas especificaciones del anterior) que almacena 

En cuanto a los parámetros, se incluyen los siguientes:

- **Subbasins area (km2)**: 30 de Mayo de e2025
- **Subbasins length flowpath (km)**: 30 de Mayo de e2025
- **Min. height in lenth flowpath (m)** and **Max. height in length flowpath (m)**: Altitud máxima y mínima (en metros) del cauce principal o línea de flujo máxima de la subcuenca.
- **Curve Number (CN)**: Valor de número de curva medio de la subcuenca.
- **Antecedent wet** radio buttons : Opción que sirve para corregir el número de curva en función de las condiciones antecedentes de humedad en el suelo (por defecto se marca la opción *Normal*, que suele corresponder con los valores tabulados de número de curva y capas espaciales existentes).
- **Subbasins ID**: 30 de Mayo de e2025
- **Subbasins ID**: 30 de Mayo de e2025
- **Subbasins ID**: 30 de Mayo de e2025
- **Subbasins ID**: 30 de Mayo de e2025
- **Subbasins ID**: 30 de Mayo de e2025
- **Subbasins ID**: 30 de Mayo de e2025 



### 2.2. Results

## 3. Methods

### 3.1. Loss

### 3.2. Transform

### 3.3. Routing

## References




### License

[hydroUH](https://github.com/fdfsfjgomariz/hidroUH) © 2025 by [Francisco Gomariz-Castillo](https://portalinvestigacion.um.es/investigadores/333183/detalle) is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)
