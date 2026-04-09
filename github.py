import subprocess
import os

def subir_a_github():
    # Tu configuración específica
    repo_url = "https://github.com/martinezmarcos93/dark_fantasy_game.git"
    user_name = "Marcos"
    user_email = "marcos.e.martinez@hotmail.com.ar"
    
    try:
        # 1. Configurar identidad (por si acaso no quedó guardado)
        print("Configurando usuario...")
        subprocess.run(f'git config --global user.name "{user_name}"', shell=True, check=True)
        subprocess.run(f'git config --global user.email "{user_email}"', shell=True, check=True)

        # 2. Inicializar repositorio si no existe la carpeta .git
        if not os.path.exists(".git"):
            print("Inicializando repositorio local...")
            subprocess.run("git init", shell=True, check=True)

        # 3. Añadir archivos al stage
        print("Preparando archivos...")
        subprocess.run("git add .", shell=True, check=True)

        # 4. Hacer el commit
        # Usamos un bloque try/except aquí por si no hay cambios nuevos que subir
        try:
            subprocess.run('git commit -m "Subida de archivos de Dark Fantasy Game"', shell=True, check=True)
        except subprocess.CalledProcessError:
            print("No hay cambios nuevos para commit, continuando...")

        # 5. Configurar la rama principal a 'main'
        subprocess.run("git branch -M main", shell=True, check=True)

        # 6. Gestionar el remoto (borra el anterior si existe para evitar errores de 'already exists')
        print("Conectando con GitHub...")
        subprocess.run("git remote remove origin", shell=True, stderr=subprocess.DEVNULL)
        subprocess.run(f"git remote add origin {repo_url}", shell=True, check=True)

        # 7. Subir los archivos
        print("Subiendo a GitHub... (Es posible que se abra una ventana para autenticar)")
        subprocess.run("git push -u origin main", shell=True, check=True)
        
        print("\n¡Éxito! Tu código ya debería estar en: " + repo_url)

    except subprocess.CalledProcessError as e:
        print(f"\nError de Git: {e}")
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")

if __name__ == "__main__":
    subir_a_github()