# 🚀 Smart CV Filter - Guía de Usuario

Bienvenido a **Smart CV Filter**, tu asistente inteligente para la clasificación automática de currículums. Este programa utiliza Inteligencia Artificial local para analizar la afinidad de los candidatos con el puesto que buscas, garantizando la **privacidad total** de los datos.

---

## ⚡ REQUISITO INDISPENSABLE: Configuración de la IA

Para que el programa funcione correctamente, debe tener instalado el motor de IA **Ollama** y el modelo **Gemma 2b**. Siga estos pasos antes de ejecutar la aplicación:

1. **Instalar Ollama**: Descargue e instale el motor desde [ollama.com](https://ollama.com/).
2. **Descargar Modelo Gemma 2b**:
   * Abra una terminal (Símbolo del sistema, PowerShell o Terminal de Linux).
   * Ejecute el siguiente comando:
     ```bash
     ollama pull gemma2:2b
     ```
3. **Verificación**: Una vez finalizada la descarga, el modelo estará listo para ser utilizado por Smart CV Filter de forma automática.

---

## 🛠️ Cómo empezar

1. **Prepara los CVs**: Coloca todos los currículums que quieras analizar (PDF, DOCX o TXT) en una carpeta en tu ordenador.
2. **Ejecuta el programa**: Haz doble clic en `SmartCVFilter.exe` (o el binario correspondiente en Linux).
3. **Configura el proceso**:
   * **Puesto**: Escribe el nombre del cargo (ej: "Analista de Datos").
   * **Fecha**: Se rellena automáticamente, pero puedes cambiarla si lo deseas.

---

## 📖 Instrucciones de Uso

### Paso 1: Seleccionar la carpeta de entrada
Haz clic en el botón **"Explorar"** y busca la carpeta donde guardaste los currículums. El programa leerá todos los archivos compatibles que encuentre dentro.

### Paso 2: Definir el perfil buscado (Job Description)
En el cuadro de texto central, pega la descripción del puesto o los requisitos clave. 
> **Tip:** Puedes hacer clic derecho dentro del cuadro para usar la opción **"📋 Pegar Texto"**.

### Paso 3: ¡Clasificar!
Haz clic en el botón **"🚀 CLASIFICAR CVS"**. Verás en la consola inferior cómo la IA analiza cada perfil en tiempo real. 
*Nota: La primera ejecución puede tardar unos segundos adicionales mientras se carga el modelo en memoria.*

---

## 📂 ¿Dónde están mis resultados?

Una vez terminado el proceso, el programa creará automáticamente una carpeta llamada `procesos_seleccion` en el mismo lugar donde está el ejecutable. Dentro encontrarás una carpeta con la fecha y el nombre del puesto, organizada así:

* **📁 RECLUTADOS**: Candidatos que cumplen con el perfil (Ordenados por puntuación, los mejores primero).
* **📁 DUDAS**: Candidatos que cumplen parcialmente o requieren revisión.
* **📁 DESCARTADOS**: Perfiles que no encajan con los requisitos.

> **Nota:** Los archivos han sido renombrados con su puntuación (Score) para que siempre veas a los mejores candidatos al principio de la lista.

---

## 🔒 Privacidad y Seguridad

Este programa es **100% Local**. 
* **No requiere internet** para analizar los documentos.
* Los datos de los candidatos **nunca salen de tu ordenador**.
* Cumple con los estándares de privacidad al no utilizar servicios de IA en la nube.

---

## ⚠️ Notas importantes
* **Hardware**: Se recomienda disponer de al menos 8GB de RAM para un rendimiento fluido del modelo Gemma 2b.
* **Archivos en uso**: Asegúrate de no tener los archivos de los CVs abiertos en otros programas (como Word o Adobe Reader) durante el análisis.
* **Errores**: Si un CV está protegido por contraseña, el sistema no podrá leerlo y lo marcará como error en el log.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** [Python 3.10+](https://www.python.org/)
* **Interfaz Gráfica:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
* **Motor de IA:** [Ollama](https://ollama.com/) ejecutando **Gemma 2b** localmente.
* **Procesamiento de Documentos:** PyMuPDF (fitz) y python-docx.

---

## 🚀 Instalación y Ejecución

1. **Descarga:** Ve a la sección de [Releases](https://github.com/Tebagl/smart_cv_filter/releases) y descarga el archivo correspondiente.
2. **Descomprimir:** Extrae el contenido en una carpeta local.
3. **Ejecución**:
   * **Windows**: Ejecuta `SmartCVFilter.exe`.
   * **Linux**: `chmod +x SmartCVFilter` y ejecutar `./SmartCVFilter`.

---
*Smart CV Filter - Transformando el reclutamiento con IA Ética y Local.*

<img width="1293" height="725" alt="Captura desde 2026-04-13 21-39-14" src="https://github.com/user-attachments/assets/b853be37-99e8-4d56-842d-9b8b70a3f536" />
<img width="1293" height="725" alt="Captura desde 2026-04-13 21-38-44" src="https://github.com/user-attachments/assets/74bb4f3c-917f-490b-86be-c07f6bed3907" />
<img width="1293" height="725" alt="Captura desde 2026-04-13 19-52-02" src="https://github.com/user-attachments/assets/3a87e9e4-79a4-42e1-b64d-73fd3c938ec2" />
<img width="1294" height="743" alt="Captura desde 2026-04-14 11-27-41" src="https://github.com/user-attachments/assets/f6694eea-0a5a-447a-970a-a807df205a15" />
<img width="1294" height="743" alt="Captura desde 2026-04-14 11-28-37" src="https://github.com/user-attachments/assets/fec08e1f-21a8-4efb-9f2f-f6abfbd5e29d" />




