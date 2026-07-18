import os
import sys
import time
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors import CellExecutionError

notebooks_order = [
    # Paso 1: Dimensiones (orden indistinto)
    "dim_usuario.ipynb",
    "dim_fecha.ipynb",
    "dim_geografia.ipynb",
    "dim_hora.ipynb",
    "dim_mensajero.ipynb",
    "dim_novedades.ipynb",
    "dim_proveedor.ipynb",
    "dim_sede.ipynb",
    # Paso 2: Transformacion intermedia
    "trans_servicios.ipynb",
    # Paso 3: Tablas de hechos (en este orden obligatorio)
    "hecho_servicios.ipynb",
    "hecho_novedades.ipynb"
]

def run_notebook(nb_filename):
    print(f"\n=========================================")
    print(f"Executing: {nb_filename}")
    print(f"=========================================")
    
    start_time = time.time()
    
    # Read the notebook
    with open(nb_filename, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
        
    # Configure execution to use the newly installed venv-mensajeria kernel
    ep = ExecutePreprocessor(timeout=600, kernel_name="venv-mensajeria")
    
    try:
        # Run the notebook in the current directory context
        ep.preprocess(nb, {"metadata": {"path": "."}})
        
        # Save the executed notebook back in-place
        with open(nb_filename, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
            
        elapsed = time.time() - start_time
        print(f"SUCCESS: {nb_filename} executed in {elapsed:.2f} seconds.")
        return True
    except CellExecutionError as cell_err:
        print(f"\nCRITICAL ERROR in {nb_filename}:")
        print(cell_err)
        return False
    except Exception as e:
        print(f"\nUnexpected error running {nb_filename}: {e}")
        return False

def main():
    start_all = time.time()
    print("Starting execution of Jupyter Notebooks pipeline...")
    
    failed_notebooks = []
    
    for nb in notebooks_order:
        success = run_notebook(nb)
        if not success:
            print(f"\nPipeline execution aborted due to failure in: {nb}")
            failed_notebooks.append(nb)
            sys.exit(1)
            
    total_elapsed = time.time() - start_all
    print(f"\n=========================================")
    print(f"All notebooks executed successfully!")
    print(f"Total pipeline time: {total_elapsed:.2f} seconds.")
    print(f"=========================================")
    sys.exit(0)

if __name__ == "__main__":
    main()
