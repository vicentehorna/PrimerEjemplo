from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc
import os

app = Flask(__name__, template_folder='Templates')
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui_cambiala_en_produccion'  # Necesaria para flash messages

def get_db_connection():
    """
    Crea y retorna una conexión a la base de datos SQL Server.
    Lee las credenciales desde variables de entorno con valores por defecto.
    """
    server = os.getenv('DB_SERVER', '179.61.14.224\\SQLEXPRESS')
    database = os.getenv('DB_DATABASE', 'hm_inversiones')
    username = os.getenv('DB_USERNAME', 'sa')
    password = os.getenv('DB_PASSWORD', 'HMplanillas2020')
    
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    
    return pyodbc.connect(connection_string)

@app.route('/')
def hola_mundo():
    return '<h1>¡Hola Mundo!</h1>'

@app.route('/datos')
def mostrar_datos():
    try:
        # Conectar a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Consultar los datos
        cursor.execute('SELECT PayRollType, ShortName FROM PR_PayRollType')
        usuarios = cursor.fetchall()
        
        # Cerrar la conexión
        cursor.close()
        conn.close()
        
        # Renderizar la plantilla con los datos
        return render_template('datos.html', usuarios=usuarios)
        
    except pyodbc.Error as e:
        return f"""
        <html>
        <head>
            <title>Error</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                .error {{
                    color: red;
                    text-align: center;
                    padding: 20px;
                    background-color: white;
                    border: 2px solid red;
                    border-radius: 5px;
                    max-width: 600px;
                    margin: 50px auto;
                }}
            </style>
        </head>
        <body>
            <div class="error">
                <h2>Error de conexión a la base de datos</h2>
                <p>{str(e)}</p>
                <p>Por favor, verifica la configuración de conexión en el código.</p>
            </div>
        </body>
        </html>
        """
    except Exception as e:
        return f"""
        <html>
        <head>
            <title>Error</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                .error {{
                    color: red;
                    text-align: center;
                    padding: 20px;
                    background-color: white;
                    border: 2px solid red;
                    border-radius: 5px;
                    max-width: 600px;
                    margin: 50px auto;
                }}
            </style>
        </head>
        <body>
            <div class="error">
                <h2>Error</h2>
                <p>{str(e)}</p>
            </div>
        </body>
        </html>
        """

@app.route('/buscar')
def buscar():
    try:
        # Obtener el término de búsqueda del parámetro GET
        busqueda = request.args.get('busqueda', '').strip()
        
        # Conectar a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Si hay un término de búsqueda, realizar la consulta
        if busqueda:
            # Búsqueda en la tabla sy_person por person (ID) o name (nombre)
            # Usando LIKE para búsqueda parcial
            query = """
                SELECT TOP 50 person, name 
                FROM sy_person 
                WHERE person LIKE ? OR name LIKE ?
                ORDER BY name
            """
            busqueda_param = f'%{busqueda}%'
            cursor.execute(query, busqueda_param, busqueda_param)
        else:
            # Si no hay búsqueda, mostrar los primeros 50 registros
            cursor.execute('SELECT TOP 50 person, name FROM sy_person ORDER BY name')
        
        resultados_raw = cursor.fetchall()
        
        # Convertir los resultados a una lista de diccionarios
        resultados = []
        for row in resultados_raw:
            resultados.append({
                'id': row.person,
                'nombre': row.name
            })
        
        # Cerrar la conexión
        cursor.close()
        conn.close()
        
        # Renderizar la plantilla con los resultados
        return render_template('buscar.html', resultados=resultados)
        
    except pyodbc.Error as e:
        return f"""
        <html>
        <head>
            <title>Error</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                .error {{
                    color: red;
                    text-align: center;
                    padding: 20px;
                    background-color: white;
                    border: 2px solid red;
                    border-radius: 5px;
                    max-width: 600px;
                    margin: 50px auto;
                }}
            </style>
        </head>
        <body>
            <div class="error">
                <h2>Error de conexión a la base de datos</h2>
                <p>{str(e)}</p>
                <p>Por favor, verifica la configuración de conexión en el código.</p>
            </div>
        </body>
        </html>
        """
    except Exception as e:
        return f"""
        <html>
        <head>
            <title>Error</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                .error {{
                    color: red;
                    text-align: center;
                    padding: 20px;
                    background-color: white;
                    border: 2px solid red;
                    border-radius: 5px;
                    max-width: 600px;
                    margin: 50px auto;
                }}
            </style>
        </head>
        <body>
            <div class="error">
                <h2>Error</h2>
                <p>{str(e)}</p>
            </div>
        </body>
        </html>
        """

@app.route('/agregar', methods=['POST'])
def agregar():
    try:
        # Obtener los datos del formulario
        codigo = request.form.get('codigo', '').strip()
        nombre = request.form.get('nombre', '').strip()
        
        # Validar que ambos campos estén presentes
        if not codigo or not nombre:
            flash('Por favor, complete todos los campos.', 'warning')
            return redirect(url_for('buscar'))
        
        # Conectar a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insertar el nuevo registro en la tabla sy_person
        query = "INSERT INTO sy_person (person, name) VALUES (?, ?)"
        cursor.execute(query, codigo, nombre)
        
        # Confirmar la transacción
        conn.commit()
        
        # Cerrar la conexión
        cursor.close()
        conn.close()
        
        # Mostrar mensaje de éxito
        flash(f'Usuario "{nombre}" (Código: {codigo}) agregado exitosamente.', 'success')
        
        # Redireccionar a la página principal (buscar)
        return redirect(url_for('buscar'))
        
    except pyodbc.Error as e:
        # Mostrar mensaje de error
        flash(f'Error al agregar usuario: {str(e)}', 'danger')
        return redirect(url_for('buscar'))
    except Exception as e:
        # Mostrar mensaje de error genérico
        flash(f'Error inesperado: {str(e)}', 'danger')
        return redirect(url_for('buscar'))

if __name__ == '__main__':
    app.run(debug=True)
