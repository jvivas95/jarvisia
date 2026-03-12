# Jarvisia

Asistente de voz en Python con reconocimiento de voz offline (Vosk), sintesis de voz (pyttsx3) y acciones de automatizacion

## Requisitos

### Requisitos de software

- Python 3.12 o inferior
- Windows (el proyecto esta configurado para comandos y rutas de Windows)
- pip actualizado

### Requisitos de sistema (importante para audio)

- Driver de microfono correctamente instalado
- PortAudio (requerido por PyAudio)

Nota: Si falla la instalacion de PyAudio en Windows, puede ser por la versión de Python 3.14

## Instalacion

1. Clona o descarga este repositorio.
2. Entra a la carpeta del proyecto.
3. Crea un entorno virtual.
4. Activa el entorno virtual.
5. Instala dependencias.

Comandos recomendados en PowerShell:

```powershell
python -m venv entorno
.\entorno\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Dependencias Python

Se instalan desde [requirements.txt](requirements.txt):

- vosk
- PyAudio
- pyttsx3
- pywhatkit
- requests

## Modelo de voz Vosk

Este proyecto espera el modelo en la carpeta [model/](model/), ya incluida en este repo.

Si en algun momento cambias de modelo, asegurate de mantener esta estructura minima:

- [model/am/final.mdl](model/am/final.mdl)
- [model/conf/model.conf](model/conf/model.conf)
- [model/graph/HCLG.fst](model/graph/HCLG.fst)

## Ejecucion

Con el entorno virtual activo:

```powershell
python index.py
```

## Funciones incluidas

- Activacion por voz con palabras clave (ej: "hola jarvis")
- Apertura de calculadora
- Apertura de Cursor (ruta local configurable)
- Busquedas en Google
- Reproduccion en YouTube
- Envio de mensajes por WhatsApp
- Chistes aleatorios desde JokeAPI

## Configuracion rapida

Puedes ajustar estos valores en [index.py](index.py):

- `USERNAME`
- `BOTNAME`

Y estas rutas en [functions/os_ops.py](functions/os_ops.py):

- `calculator`
- `cursor`

## Notas

- El envio de WhatsApp usa `pywhatkit` y puede requerir sesion iniciada en WhatsApp Web.
- `pyttsx3` usa `sapi5` en Windows.
- Para mejorar reconocimiento, usa un microfono estable y minimiza ruido ambiente.
