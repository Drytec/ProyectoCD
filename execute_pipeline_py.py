import os
import sys
import time
import subprocess

scripts_order = [
    # Paso 1: Dimensiones (orden indistinto)
    "archivos_py/dim_usuario.py",
    "archivos_py/dim_fecha.py",
    "archivos_py/dim_geografia.py",
    "archivos_py/dim_hora.py",
    "archivos_py/dim_mensajero.py",
    "archivos_py/dim_novedades.py",
    "archivos_py/dim_proveedor.py",
    "archivos_py/dim_sede.py",
    # Paso 2: Transformacion intermedia
    "archivos_py/trans_servicios.py",
    # Paso 3: Tablas de hechos (en este orden obligatorio)
    "archivos_py/hecho_servicios.py",
    "archivos_py/hecho_novedades.py",
    # Paso 4: Consultas finales
    "archivos_py/consultas.py"
]

def run_script(py_filename):
    print(f"\n=========================================")
    print(f"Executing: {py_filename}")
    print(f"=========================================")
    
    start_time = time.time()
    
    # Get the directory of the current pipeline script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    py_path = os.path.join(script_dir, py_filename)
    
    try:
        # Run the python script in the script's directory context using current python interpreter
        subprocess.run(
            [sys.executable, py_path],
            cwd=script_dir,
            check=True
        )
        
        elapsed = time.time() - start_time
        print(f"SUCCESS: {py_filename} executed in {elapsed:.2f} seconds.")
        return True
    except subprocess.CalledProcessError as err:
        print(f"\nCRITICAL ERROR in {py_filename}: Script returned non-zero exit code {err.returncode}.")
        return False
    except Exception as e:
        print(f"\nUnexpected error running {py_filename}: {e}")
        return False

def main():
    start_all = time.time()
    print("Starting execution of Python scripts pipeline...")
    
    failed_scripts = []
    
    for py in scripts_order:
        success = run_script(py)
        if not success:
            print(f"\nPipeline execution aborted due to failure in: {py}")
            failed_scripts.append(py)
            sys.exit(1)
            
    total_elapsed = time.time() - start_all
    print(f"\n=========================================")
    print(f"All Python scripts executed successfully!")
    print(f"Total pipeline time: {total_elapsed:.2f} seconds.")
    print(f"=========================================")
    sys.exit(0)

if __name__ == "__main__":
    main()
