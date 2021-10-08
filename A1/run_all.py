import subprocess

# Change the path of your Virtual Environment
VENV = "C:\\Users\\vasur\\Documents\\GitHub\\COMP6791\\A1\\venv\\Scripts\\python.exe"

subprocess.run(VENV+" pipeline1_extract_raw_text.py",shell=True)
subprocess.run(VENV+" pipeline2_tokenizer.py",shell=True)
subprocess.run(VENV+" pipeline3_convert_to_lowercase.py",shell=True)
subprocess.run(VENV+" pipeline4_apply_stemmer.py",shell=True)
subprocess.run(VENV+" pipeline5_stop_words_remover.py",shell=True)

