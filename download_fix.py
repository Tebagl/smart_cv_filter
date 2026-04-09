from sentence_transformers import SentenceTransformer
import os

# Definimos la ruta donde queremos guardar los archivos físicos
# Esto evitará los "enlaces simbólicos" vacíos que vimos en tu VS Code
save_path = os.path.join(os.getcwd(), "models", "cv_model")

print("Iniciando descarga del modelo real (aprox. 450MB)...")
try:
    # 1. Descarga el modelo a la caché temporal
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    # 2. Crea la carpeta si no existe
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # 3. Guarda los archivos físicos reales en la carpeta del proyecto
    model.save(save_path)
    
    print(f"\n✅ ¡ÉXITO! El modelo se ha guardado en: {save_path}")
    print("Ahora deberías ver archivos como 'pytorch_model.bin' o 'model.safetensors' con peso real.")

except Exception as e:
    print(f"\n❌ Error durante la descarga: {e}")