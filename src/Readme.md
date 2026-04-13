# 🚀 Smart CV Filter - Guía de Usuario

Bienvenido a **Smart CV Filter**, tu asistente inteligente para la clasificación automática de currículums. Este programa utiliza Inteligencia Artificial local para analizar la afinidad de los candidatos con el puesto que buscas, garantizando la **privacidad total** de los datos.

---

## ⚡ REQUISITO INDISPENSABLE (Antes de empezar)

Para que el programa pueda "pensar", necesita tener instalado el motor de IA **Ollama** y el modelo **Gemma 2b**. Sigue estos 3 pasos rápidos:

1.  **Instala Ollama**: Descárgalo gratis desde [ollama.com](https://ollama.com/) e instálalo como cualquier otro programa.
2.  **Descarga el Modelo**: Abre una terminal (Símbolo del sistema o PowerShell en Windows) y escribe el siguiente comando:
    ```bash
    ollama pull gemma2:2b
    ```
3.  **Listo**: Una vez termine la descarga, ya puedes cerrar la terminal y abrir **Smart CV Filter**.

---

## 🛠️ Cómo empezar

1.  **Prepara los CVs**: Coloca todos los currículums que quieras analizar (PDF, DOCX o TXT) en una carpeta en tu ordenador (por ejemplo, en una carpeta en el Escritorio).
2.  **Ejecuta el programa**: Haz doble clic en `SmartCVFilter.exe`.
3.  **Configura el proceso**:
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
> **Nota:** La primera vez puede tardar un poco más mientras la IA se carga en la memoria RAM.

---

## 📂 ¿Dónde están mis resultados?

Una vez terminado el proceso, el programa creará automáticamente una carpeta llamada `procesos_seleccion` en el mismo lugar donde está el ejecutable. Dentro encontrarás una carpeta con la fecha y el nombre del puesto, organizada así:

* **📁 RECLUTADOS**: Candidatos que cumplen con el perfil (Ordenados por puntuación, los mejores primero).
* **📁 DUDAS**: Candidatos que cumplen parcialmente o requieren revisión.
* **📁 DESCARTADOS**: Perfiles que no encajan con los requisitos.

> **Nota:** Los archivos han sido renombrados con su puntuación (Score) para que siempre veas a los mejores candidatos al principio de la lista en tu carpeta (ej: `85_cv_juan.pdf`).

---

## 🔒 Privacidad y Seguridad

Este programa es **100% Local**.
* **No requiere internet** para analizar los documentos.
* **Sin Nube**: Los datos de los candidatos **nunca salen de tu ordenador** o de la red de la academia.
* **IA Ética**: Cumple con los estándares de privacidad al no utilizar servicios de terceros.

---

## ⚠️ Notas importantes
* **Memoria RAM**: Se recomienda cerrar programas pesados durante el análisis para que la IA trabaje con fluidez.
* **Archivos Abiertos**: Asegúrate de no tener los archivos de los CVs abiertos en otros programas (como Word o Adobe Reader) mientras realizas el análisis.
* **Contraseñas**: Si un CV está protegido, el sistema no podrá leerlo y lo marcará como error.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.10+
* **Interfaz Gráfica:** CustomTkinter
* **Motor de IA:** Ollama con modelo **Gemma 2b**.
* **Procesamiento:** PyMuPDF, python-docx.

---
*Smart CV Filter - Transformando el reclutamiento con IA Ética y Local.*