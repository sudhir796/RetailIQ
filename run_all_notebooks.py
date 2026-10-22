import os
import subprocess
import sys

# List of notebooks to run in sequential order
notebooks = [
    "notebooks/00_data_ingestion.ipynb",
    "notebooks/01_data_cleaning.ipynb",
    "notebooks/02_eda.ipynb",
    "notebooks/03_feature_engineering.ipynb",
    "notebooks/04a_sales_forecasting.ipynb",
    "notebooks/04b_customer_segmentation.ipynb",
    "notebooks/05_product_demand.ipynb",
    "notebooks/06_model_evaluation_summary.ipynb"
]

def run_notebook(nb_path):
    print(f"\n==========================================")
    print(f"Executing: {nb_path}...")
    print(f"==========================================")
    
    # We use nbconvert to execute the notebook in place
    command = [
        sys.executable, "-m", "jupyter", "nbconvert",
        "--to", "notebook",
        "--execute",
        "--inplace",
        nb_path
    ]
    
    try:
        # Run the command and pipe output to stdout
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully executed {nb_path}!")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {nb_path}:")
        print(e.stderr)
        return False
    return True

def main():
    # Check if jupyter is installed
    try:
        import jupyter
        import nbconvert
    except ImportError:
        print("Required packages (jupyter, nbconvert) are not installed in this environment.")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)
        
    for nb in notebooks:
        if not os.path.exists(nb):
            print(f"Warning: Notebook {nb} not found. Skipping.")
            continue
        success = run_notebook(nb)
        if not success:
            print("\nPipeline stopped due to error.")
            sys.exit(1)
            
    print("\n==========================================")
    print("Pipeline execution complete! All notebooks have been successfully run.")
    print("==========================================")

if __name__ == "__main__":
    main()
