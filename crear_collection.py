import json
import csv
import requests
import os
from datetime import datetime
from urllib.parse import urlparse

# Constantes para versiones compatibles de OpenAPI
VERSIONS_COMPATIBLES_OPENAPI_3 = {'3.0.1', '3.0.2'}
VERSION_SWAGGER_2 = '2.0'

class CarpetaManager:
    @staticmethod
    def crear_carpetas(ruta):
        """Crea las carpetas necesarias para los datos de entrada y salida."""
        carpeta_recursos = os.path.join(ruta, 'data-in')
        carpeta_builds = os.path.join(ruta, 'data-out')
        try:
            os.makedirs(carpeta_recursos, exist_ok=True)
            os.makedirs(carpeta_builds, exist_ok=True)
            print(f'Se han creado las carpetas "{carpeta_recursos}" y "{carpeta_builds}" en {ruta}')
        except Exception as e:
            print(f'Error al crear las carpetas: {e}')

class JSONDownloader:
    @staticmethod
    def descargar_json(url, nombre_archivo):
        """Descarga un archivo JSON desde una URL dada."""
        try:
            response = requests.get(url)
            response.raise_for_status()  # Levanta una excepción para errores HTTP
            with open(nombre_archivo, 'wb') as archivo:
                archivo.write(response.content)
            print(f"El archivo {nombre_archivo} ha sido descargado correctamente.")
        except requests.RequestException as e:
            print(f"No se pudo descargar el archivo: {e}")

class JSONExtractor:
    @staticmethod
    def extract_data_2v(json_data):
        """Extrae datos de la especificación Swagger 2.0."""
        extracted_data = []
        for url, details in json_data.items():
            method = list(details.keys())[0]
            summary = details[method].get("summary", "")
            parameters = details[method].get("parameters", [])
            
            body_parameters = "none"
            path_parameters = []
            query_parameters = []

            for param in parameters:
                if param.get("in") == "body":
                    body_parameters = param.get("name", "")
                elif param.get("in") == "path":
                    path_parameters.append(param.get("name", ""))
                elif param.get("in") == "query":
                    query_parameters.append(param.get("name", ""))

            extracted_data.append([
                url, summary, method, len(parameters),
                body_parameters, path_parameters, len(path_parameters),
                query_parameters, len(query_parameters)
            ])

        return extracted_data

    @staticmethod
    def extract_data_3v(json_data):
        """Extrae datos de la especificación OpenAPI 3.0.x."""
        extracted_data = []
        for url, details in json_data.items():
            method = list(details.keys())[0]
            summary = details[method].get("operationId", "")
            parameters = details[method].get("parameters", [])
            
            body_parameters = "none"
            path_parameters = []
            query_parameters = []

            for param in parameters:
                if param.get("in") == "body":
                    body_parameters = param.get("name", "")
                elif param.get("in") == "path":
                    path_parameters.append(param.get("name", ""))
                elif param.get("in") == "query":
                    query_parameters.append(param.get("name", ""))

            extracted_data.append([
                url, summary, method, len(parameters),
                body_parameters, path_parameters, len(path_parameters),
                query_parameters, len(query_parameters)
            ])

        return extracted_data

class RegistroManager:
    @staticmethod
    def obtener_valor_ref(obj):
        """Obtiene el valor del campo $ref de un objeto JSON."""
        for key, value in obj.items():
            if isinstance(value, dict):
                result = RegistroManager.obtener_valor_ref(value)
                if result:
                    return result
            elif key == '$ref':
                return value

    @staticmethod
    def crear_registro(name, method, path, url, description, querys=None, body=None, variables=None, headers=None):
        """Crea un registro para la colección de Postman."""
        _path = str(path.replace("{", ":").replace("}", ""))
        return {
            "name": name,
            "request": {
                "method": method,
                "description": description,
                "header": headers if headers else [],
                **({"body": body} if body else {}),
                "url": {
                    "raw": str(url + _path),
                    "host": url.split("."),
                    "path": _path.split("/")[1:],
                    "variable": variables if variables else [],
                    "query": querys if querys else []
                }
            },
            "response": []
        }

    @staticmethod
    def crear_registro_tags(tag, registro):
        """Crea un registro de tag para la colección de Postman."""
        return {
            "name": tag,
            "item": registro
        }

def es_version_openapi_3(version):
    """Verifica si la versión dada es compatible con OpenAPI 3.x."""
    return version in VERSIONS_COMPATIBLES_OPENAPI_3

def es_version_swagger_2(version):
    """Verifica si la versión dada es Swagger 2.0."""
    return version == VERSION_SWAGGER_2

def procesar_json(json_data):
    """Procesa los datos JSON de acuerdo a la versión de OpenAPI o Swagger."""
    if es_version_swagger_2(json_data.get("swagger")):
        extracted_data = JSONExtractor.extract_data_2v(json_data["paths"])
        return extracted_data, '2.0'
    elif es_version_openapi_3(json_data.get("openapi")):
        extracted_data = JSONExtractor.extract_data_3v(json_data["paths"])
        return extracted_data, '3.0.x'
    else:
        print('No es una versión compatible con Swagger 2.0 o OpenAPI 3.x')
        return None, None

class PostmanEnvironmentGenerator:
    @staticmethod
    def generar_entorno(nombre_proyecto, values, ruta='./data-out'):
        """
        Genera un archivo JSON con las variables de entorno para Postman.

        :param nombre_proyecto: Nombre del proyecto, que será parte del nombre del entorno.
        :param values: Lista de diccionarios con las variables de entorno (key, value, type, enabled).
        :param ruta: Ruta donde se guardará el archivo JSON generado.
        """
        # Definición del entorno
        entorno = {
            "name": f"{nombre_proyecto}_environment",
            "values": values,
            "_postman_variable_scope": "environment",
            "_postman_exported_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "_postman_exported_using": "Postman/10.24.24"
        }

        # Nombre del archivo JSON
        nombre_archivo = f'{ruta}/{nombre_proyecto}_environment.json'

        # Guardar el entorno en un archivo JSON
        try:
            with open(nombre_archivo, 'w') as archivo:
                json.dump(entorno, archivo, indent=2)
            print(f"El archivo de entorno se ha generado exitosamente en {nombre_archivo}.")
        except Exception as e:
            print(f"No se pudo generar el archivo de entorno: {e}")

def agregar_variable_entorno(values, key, value, type, enabled=True):
    """
    Agrega un diccionario con la estructura específica a una lista.

    :param values: Lista donde se agregarán los diccionarios.
    :param key: Clave del diccionario.
    :param value_type: Valor para 'value' y 'type'.
    :param enabled: Booleano que indica si el valor está habilitado. Por defecto es True.
    """
    nuevo_valor = {
        "key": key,
        "value": value,
        "type": type,
        "enabled": enabled
    }
    values.append(nuevo_valor)

def extraer_dominio(url):
    """
    Extrae el dominio de la URL sin el esquema y el path.

    :param url: URL completa desde la cual se extraerá el dominio.
    :return: Dominio extraído.
    """
    # Analizar la URL
    parsed_url = urlparse(url)
    dominio = parsed_url.netloc
    return dominio

def main():
    # Especifica la ruta donde deseas crear las carpetas
    ruta = './'
    CarpetaManager.crear_carpetas(ruta)

    # Solicitar información al usuario
    nombreProyecto = input("Ingrese el nombre del proyecto: ")
    urlSwaggerDoc = input("Ingrese url del archivo json: ")

    # Nombre del archivo descargado
    nombre_archivo = f'./data-in/swagger_{nombreProyecto}.json'

    # Descargar el archivo JSON
    JSONDownloader.descargar_json(urlSwaggerDoc, nombre_archivo)

    # Leer el archivo JSON
    try:
        with open(nombre_archivo, 'r') as file:
            json_data = json.load(file)
    except FileNotFoundError:
        print("No se pudo encontrar el archivo JSON descargado.")
        return
    except json.JSONDecodeError:
        print("Error al decodificar el archivo JSON.")
        return

    # Procesar JSON
    extracted_data, versionSwagger = procesar_json(json_data)
    if extracted_data is None:
        return

    # Escribir los datos en un archivo CSV
    csv_file = f'./data-out/output_{nombreProyecto}.csv'
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['URL', 'Name ', 'Method', 'Parameters', 'Body', 'Path parameters', 'Paths', 'Query parameters', 'Querys'])
        writer.writerows(extracted_data)

    print("Los datos se han guardado exitosamente en el archivo CSV.")

    # Creación de la colección de Postman
    values_environment =[]
    if versionSwagger == '2.0' :
        agregar_variable_entorno(values_environment, "protocol", json_data['schemes'][0], 'string') 
        agregar_variable_entorno(values_environment, "host", json_data['host'], 'string')
        agregar_variable_entorno(values_environment, "base_url", json_data['basePath'], 'string')
        env = '{{protocol}}://{{host}}{{base_url}}'
    else :
        agregar_variable_entorno(values_environment, "protocol", 'https', 'string')
        agregar_variable_entorno(values_environment, "host", extraer_dominio(urlSwaggerDoc), 'string')
        agregar_variable_entorno(values_environment, "base_url", json_data['servers'][0].get('url'), 'string')
        env = '{{protocol}}://{{host}}{{base_url}}'
    collection = {
        "info": {
            "name": str(nombreProyecto),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
            'description': json_data['info'].get('description', '') + ' Version:' + json_data['info'].get('version', ''),
            'version': json_data['info'].get('version', '')
        },
        "item": []
    }
    registros_por_tag = {}
    
    for urls, methods in json_data['paths'].items():
        # Convertir values_environment a un conjunto de nombres
        names_set = {env_var['key'] for env_var in values_environment}
        for method, details in methods.items():
            summary = details.get('operationId', '')
            variables = []
            queryParams = []
            json_raw = {}
            headers = [{"key": "accept", "value": "*/*"}]
            parameters = details.get('parameters', [])

            # Obtener requestBody si está disponible
            requestBody = details.get('requestBody')
            if requestBody and requestBody.get('required'):
                refBodyDTO = RegistroManager.obtener_valor_ref(requestBody.get('content', {}))
                if refBodyDTO and versionSwagger == '3.0.x':
                    path1 = refBodyDTO.split('#')[1]
                    path2 = path1.split('/')[1]
                    bodyDTO = refBodyDTO.split('/')[-1]
                    json_raw = str(json_data[path2]['schemas'][bodyDTO]['properties'])

            # Procesar parámetros
            for param in parameters:
                if param.get('in') == 'path':
                    registroPathParametro = {'key': param['name'], 'value': '{{'+param['name']+'}}'}
                    variables.append(registroPathParametro)
                elif param.get('in') == 'query':
                    registroQueryParametro = {
                        'key': param['name'],
                        'value': '{{'+param['name']+'}}',
                        'disabled': True
                    }
                    queryParams.append(registroQueryParametro)
                elif param.get('in') == 'body':
                    ref = RegistroManager.obtener_valor_ref(param.get('schema', {}))
                    if param.get('required'):
                        path1 = ref.split('#')[1]
                        path2 = path1.split('/')[1]
                        bodyDTO = ref.split('/')[-1]
                        json_raw = str(json_data[path2][bodyDTO]['properties'])
                # Verificar si el nombre del parámetro no está en el conjunto
                if param['name'] not in names_set and (variables or queryParams):
                    try:
                        agregar_variable_entorno(values_environment, param['name'], 'string', 'string')
                        names_set.add(param['name'])  # Actualizar el conjunto
                    except Exception as e:
                        print(f"No se pudo generar el archivo de entorno: {e}")
                            
            body = {
                "mode": "raw",
                "raw": json_raw.replace("'", "\""),
                "options": {
                    "raw": {
                        "language": "json"
                    }
                }
            } if json_raw else []

            # Descripción del endpoint
            textDescription = details.get("description", '')

            # Procesar tags y crear registros
            tags = details.get('tags', [])
            if len(tags) == 1:
                tag = tags[0]
                if tag not in registros_por_tag:
                    registros_por_tag[tag] = []
                registros_por_tag[tag].append(RegistroManager.crear_registro(summary, method, urls, env, textDescription, queryParams, body, variables, headers))
            else:
                collection["item"].append(RegistroManager.crear_registro(summary, method, urls, env, textDescription, queryParams, body, variables, headers))

    # Agregar registros por tag
    for tag, registros in registros_por_tag.items():
        collection['item'].append(RegistroManager.crear_registro_tags(tag, registros))

    # Convertir a formato JSON y guardar en un archivo
    json_final = json.dumps(collection, indent=2)
    PostmanEnvironmentGenerator.generar_entorno(nombreProyecto, values_environment)
    ruta_colletion = f'./data-out/collection_{nombreProyecto}.json'
    with open(ruta_colletion, 'w') as archivo:
        archivo.write(json_final)

    print(f'Recuerda buscar la colección en la carpeta {ruta_colletion}.')

if __name__ == "__main__":
    main()
