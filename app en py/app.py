from flask import Flask, render_template, request, redirect, url_for, session
import json, os

app = Flask(__name__)
app.secret_key = "clave_secreta"  # Necesaria para manejar sesiones

def guardar_datos(datos):
    with open("datos.json", "w") as f:
        json.dump(datos, f, indent=4)


def cargar_datos():
    if os.path.exists("datos.json"):
        with open("datos.json", "r") as f:
            return json.load(f)
    return []

# Ruta principal
@app.route("/")
def home():
    return render_template("index.html")  # Muestra index.html

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        # Guardar datos
        email = request.form["email"]
        password = request.form["password"]
        rol = request.form.get("rol", "usuario")  # Por defecto "usuario"
        
        datos = cargar_datos()
        datos.append({"email": email, "password": password, "rol": rol})  # usar "email" para que coincida con login
        guardar_datos(datos)
        
        # Redirigir a login
        return redirect(url_for("home"))  # o a tu página de login
    else:
        # Mostrar formulario
        return render_template("registro.html")

#LOGIN

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    datos = cargar_datos()
    for user in datos:
        if user["email"] == email and user["password"] == password:
            session["email"] = email
            session["rol"] = user.get("rol", "usuario").lower()

            if session["rol"] == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("usuario_dashboard"))

    return "Credenciales inválidas", 401


@app.route("/admin")
def admin_dashboard():
    if session.get("rol") != "admin":
        return "No autorizado", 403
    return render_template("admin_dashboard.html")

@app.route("/usuario")
def usuario_dashboard():
    if session.get("rol") != "usuario":
        return "No autorizado", 403
    return render_template("usuario_dashboard.html")



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
