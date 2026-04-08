# 🚀 Smart CV Filter - Guía de Usuario

Bienvenido a **Smart CV Filter**, tu asistente inteligente para la clasificación automática de currículums. Este programa utiliza Inteligencia Artificial local para analizar la afinidad de los candidatos con el puesto que buscas, garantizando la **privacidad total** de los datos.

---

## 🛠️ Cómo empezar

1. **Prepara los CVs**: Coloca todos los currículums que quieras analizar (PDF, DOCX o TXT) en una carpeta en tu ordenador (por ejemplo, en una carpeta en el Escritorio).
2. **Ejecuta el programa**: Haz doble clic en `SmartCVFilter.exe`.
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

---

## 📂 ¿Dónde están mis resultados?

Una vez terminado el proceso, el programa creará automáticamente una carpeta llamada `procesos_seleccion` en el mismo lugar donde está el ejecutable. Dentro encontrarás una carpeta con la fecha y el nombre del puesto, organizada así:

*   **📁 RECLUTADOS**: Candidatos que cumplen con el perfil (Ordenados por puntuación, los mejores primero).
*   **📁 DUDAS**: Candidatos que cumplen parcialmente o requieren revisión.
*   **📁 DESCARTADOS**: Perfiles que no encajan con los requisitos.

> **Nota:** Los archivos han sido renombrados con su puntuación (Score) para que siempre veas a los mejores candidatos al principio de la lista en tu carpeta.

---

## 🔒 Privacidad y Seguridad

Este programa es **100% Local**. 
*   **No requiere internet** para analizar los documentos.
*   Los datos de los candidatos **nunca salen de tu ordenador**.
*   Cumple con los estándares de privacidad al no utilizar servicios de IA en la nube.

---

## ⚠️ Notas importantes
*   Asegúrate de no tener los archivos de los CVs abiertos en otros programas (como Word o Adobe Reader) mientras realizas el análisis para evitar errores de movimiento.
*   Si un CV está protegido por contraseña, el sistema no podrá leerlo y lo marcará como error en el log.

---
*Smart CV Filter - Transformando el reclutamiento con IA Ética y Local.*

## 🛠️ Tecnologías Utilizadas

Para garantizar un rendimiento óptimo y la máxima privacidad, el sistema ha sido desarrollado con el siguiente stack tecnológico:

*   **Lenguaje:** [Python 3.10+](https://www.python.org/)
*   **Interfaz Gráfica:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (Interfaz moderna, personalizada y con soporte para modo oscuro).
*   **Motor de IA:** Modelos de **NLP (Procesamiento de Lenguaje Natural)** ejecutados de forma 100% local.
*   **Procesamiento de Documentos:** Librerías especializadas para la extracción de texto en formatos PDF, DOCX y TXT.

## 🚀 Instalación y Uso

1.  **Descarga:** Ve a la sección de [Releases](https://github.com/Tebagl/smart_cv_filter/releases) y descarga el archivo `.zip` correspondiente a tu sistema operativo.
2.  **Descomprimir:** Extrae el contenido en una carpeta local.
3.  **Ejecución:**
    *   **En Windows:** Haz doble clic en `SmartCVFilter.exe`.
    *   **En Linux:** Otorga permisos de ejecución al binario (`chmod +x SmartCVFilter`) y lánzalo.
4.  **Uso:** Selecciona la carpeta de origen de los CVs, pega la descripción del puesto y deja que la IA haga el trabajo por ti.

<img width="1291" height="741" alt="Captura desde 2026-04-08 20-18-09" src="https://github.com/user-attachments/assets/44d3e6b6-6cd6-4a26-9705-a7a0fd1ce4c3" />
<img width="1291" height="741" alt="Captura desde 2026-04-08 20-19-21" src="https://github.com/user-attachments/assets/f07bb0d1-0f20-4974-a14d-cdc1c6a384d0" />
<img width="904" height="595" alt="Captura desde 2026-04-08 22-33-53" src="https://github.com/user-attachments/assets/0d8e523a-18b5-4787-99f5-0a758d0b176b" />




