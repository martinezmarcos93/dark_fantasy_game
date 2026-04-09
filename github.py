import subprocess
import os

def subir_a_github():
    repo_url = "https://github.com/martinezmarcos93/dark_fantasy_game.git"
    
    try:
        # 1. Preparar y hacer commit (esto ya lo hizo bien antes, pero por si acaso)
        print("Preparando archivos...")
        subprocess.run("git add .", shell=True, check=True)
        try:
            subprocess.run('git commit -m "Sincronizando Dark Fantasy Game"', shell=True, check=True)
        except:
            print("Nada nuevo para commit.")

        # 2. Asegurar que estamos en la rama main
        subprocess.run("git branch -M main", shell=True, check=True)

        # 3. TRAER LOS CAMBIOS DE GITHUB (El paso que faltaba)
        # Usamos rebase para que tus archivos se pongan "encima" de los de GitHub
        print("Sincronizando con los archivos de GitHub (Pull)...")
        subprocess.run("git pull origin main --rebase", shell=True, check=True)

        # 4. SUBIR
        print("Subiendo a GitHub...")
        subprocess.run("git push -u origin main", shell=True, check=True)
        
        print("\n¡Listo! Ahora sí debería estar todo arriba.")

    except subprocess.CalledProcessError as e:
        print(f"\nError de Git: {e}")
        print("HINT: Si te sale un error de 'merge conflict', abre tus archivos en VS Code,")
        print("elige qué cambios dejar, guarda y vuelve a correr el script.")

if __name__ == "__main__":
    subir_a_github()