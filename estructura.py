import os

def generar_estructura(ruta_proyecto, archivo_salida):
    carpetas_excluir = ['__pycache__', 'app.egg-info', 'venv']
    
    with open(archivo_salida, 'w') as f:
        for raiz, directorios, archivos in os.walk(ruta_proyecto):
            # Excluir carpetas
            directorios[:] = [d for d in directorios if d not in carpetas_excluir]
            
            nivel = raiz.replace(ruta_proyecto, '').count(os.sep)
            indent = '  ' * (nivel)
            f.write(f'{indent}{os.path.basename(raiz)}/\n')
            
            for archivo in archivos:
                f.write(f'{indent}  {archivo}\n')

# Configura la ruta del proyecto y el archivo de salida
ruta_proyecto = '.'
archivo_salida = 'estructura.txt'

generar_estructura(ruta_proyecto, archivo_salida)
