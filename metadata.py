import subprocess


resultado = subprocess.run(["exiftool", "Person/1.jpg"], capture_output=True, text=True)
print(resultado.stdout)