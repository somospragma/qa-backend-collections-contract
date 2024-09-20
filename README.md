<h1 align="center">
  <br>
  <a href="http://www.amitmerchant.com/electron-markdownify"><img src="https://f.hubspotusercontent20.net/hubfs/2829524/Copia%20de%20LOGOTIPO_original-2.png"></a>
  <br>
  qa-backend-collections-contract
  <br>
</h1>

<h4 align="center">Proyecto base de <a href="https://github.com/somospragma/qa-backend-postman-collections-contract" target="_blank">Pragma</a>.</h4>


<p align="center">
  <a href="https://swagger.io/docs/">
    <img alt="Swagger Validator" src="https://img.shields.io/swagger/valid/3.0.svg">

  </a>
  <a href="https://www.mysql.com/">
    <img src="https://img.shields.io/badge/Database-MySQL-blue.svg" alt="MySQL">
  </a>
  <a href="https://www.postgresql.org/">
    <img src="https://img.shields.io/badge/Database-PostgreSQL-blue.svg" alt="PostgreSQL">
  </a>
  <a href="https://www.w3schools.com/sql/">
    <img src="https://img.shields.io/badge/SQL-Fundamentals-lightgrey.svg" alt="SQL">
  </a>
  <a href="https://cucumber.io/">
    <img src="https://img.shields.io/badge/Cucumber-BDD-green.svg" alt="Cucumber">
  </a>
  <a href="https://serenity-bdd.info/">
    <img src="https://img.shields.io/badge/Serenity-Reporting-blueviolet.svg" alt="Serenity">
  </a>
  <a href="https://www.selenium.dev/">
    <img src="https://img.shields.io/badge/Selenium-Web_Testing-brightgreen.svg" alt="Selenium">
  </a>
</p>

Redacta aca una breve descripcion del proyecto...

<p align="center">
  <a href="#topicos">Topicos</a> •
  <a href="#tecnologias">Tecnologias</a> •
  <a href="#consideraciones">Consideraciones</a> •
  <a href="#descarga">Descarga</a> •
  <a href="#instalación-y-ejecución">Instalación y ejecución</a> •
  <a href="#autores">Autores</a> •
  <a href="#relacionados">Relacionados</a> •
  <a href="#roadmap">Roadmap</a>
</p>

## Topicos

* Contratos
* Swagger
* OpenApi
* Postman
* Python

## Funcionalidades

- Descarga especificaciones OpenAPI/Swagger en formato JSON desde una URL proporcionada.
- Extrae datos relevantes de las especificaciones.
- Genera un archivo CSV con los datos extraídos.
- Crea una colección de Postman a partir de los datos extraídos.
- Genera un archivo de entorno para Postman.


## Tecnologias
### This project required:
- Python 3.x
- Paquetes de Python: `requests`, `json`, `csv`, `os`, `datetime`, `urllib`

Nota: 
Puedes instalar las dependencias necesarias ejecutando:

```bash
pip install requests
```

## Consideraciones
Para hacer uso de la herramienta es necesario conocer sobre: 
- SWAGGER desplegado sobre la web o en local con versiones 2.0 o OpenApi 3.0.1 o 3.0.2
- POSTMAN como importar collections y environments
- El script no trae body completo o ejemplos de este, es una oportunidad de mejora y es debido en los lineamientos de la documentacion y version de esta
- Verificar los datos de los environments generados
- Verificar tipo de autorizacion necesaria en las peticiones


## Descarga
Para clonar está aplicación desde la linea de comando:

```bash
git clone https://github.com/somospragma/qa-backend-postman-collections-contract.git
cd qa-backend-postman-collections-contract
git remote remove origin
git remote add origin URL_DE_TU_NUEVO_REPOSITORIO
git push -u origin master
```
Nota: Asegúrate de reemplazar URL_DE_TU_NUEVO_REPOSITORIO con la URL del repositorio que creaste en tu cuenta de GitHub.

Puedes descargar el proyecto en el enlace [download](https://github.com/somospragma/qa-backend-postman-collections-contract) 

## Instalación y ejecución

Para ejecutar está aplicación, necesitas [Python](https://www.python.org/) por lo general en algunos equipos viene instalado por linea de comandos o bien puedes hacer uso de extensiones del IDE [Visual studio Code](https://code.visualstudio.com/) 


### Ejecuta el script Python con:
``` bash
python3 crear_collection.py
```
El script se conforma de 2 pasos

### 1. Levantamiento de informacion
- Es necesario ingresar un nombre para el proyecto
- Despues de ingresar el nombre es necesario compartir la url del json del contrato de swagger/OpenApi 

### Ejemplo

url archivo = https://petstore3.swagger.io/api/v3/openapi.json

se encuentra en https://petstore3.swagger.io/#/
![OpenApi](image.png)


url archivo = https://petstore.swagger.io/v2/swagger.json

se encuentra en https://petstore.swagger.io/#/
![2.0](image-1.png)


### 2. Resultados Generados:
- CSV: Los datos extraídos se guardarán en un archivo CSV en la carpeta data-out.
- Colección de Postman: La colección generada se guardará en un archivo JSON en la carpeta data-out.
- Archivo de Entorno de Postman: El archivo de entorno se guardará en la misma carpeta data-out.


## Autores


| [<img src="https://gitlab.com/uploads/-/system/user/avatar/13437423/avatar.png?width=400" width=115><br><sub>Mauro L. Ibarra P.</sub>](https://gitlab.com/mauro.ibarrap) <br/> | [<img src="https://secure.gravatar.com/avatar/23b2db02403d79ebd356e8e8356758ec?s=192&d=identicon" width=115><br><sub>Otro autor</sub>](https://gitlab.com/) | 
:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|


## Relacionados

- [proyecto-base-serenity-bdd-screenplay-browsers-and-utilities](https://github.com/somospragma/qa-web-proyecto-base-serenity-bdd-screenplay-browsers-and-utilities)


## Roadmap

- [Guia QA](https://github.com/amitmerchant1990/pomolectron) - (En construcción) Una guia de proyectos Orientados a la Calidad de Software

