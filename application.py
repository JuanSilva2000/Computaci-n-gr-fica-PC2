from flask import Flask, request, jsonify, render_template
import boto3
import base64
import os
from datetime import datetime
from flask_cors import CORS
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

application = Flask(__name__)
CORS(application, resources={r"/*": {"origins": "*"}})  # Permitir llamadas desde navegador

# Configuración de AWS
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_BUCKET = os.getenv("AWS_BUCKET", "figuras-grafica")

# Cliente S3
s3 = boto3.client('s3', region_name=AWS_REGION)

# Ruta principal para mostrar el formulario
@application.route('/')
def index():
    return render_template('index.html')

# Ruta para guardar la imagen
@application.route('/guardar', methods=['POST'])
def guardar():
    data = request.get_json()
    etiqueta = data.get('etiqueta', 'desconocida')
    imagen_b64 = data.get('imagen', '').split(',')[1]  # Eliminar el prefijo data:image/png;base64,
    imagen_bin = base64.b64decode(imagen_b64)

    nombre_objeto = f"{etiqueta}/{etiqueta}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}.png"

    try:
        s3.put_object(
            Bucket=AWS_BUCKET,
            Key=nombre_objeto,
            Body=imagen_bin,
            ContentType='image/png'
        )
        return jsonify({"mensaje": f"{nombre_objeto} guardado en S3"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Punto de entrada local (no usado en Elastic Beanstalk)
if __name__ == '__main__':
    application.run(debug=True, port=5000)



