from flask import Flask, request, jsonify
import os
import base64
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
import psycopg2
import bcrypt  # Assurez-vous d'importer bcrypt

app = Flask(__name__)
CORS(app)  # Autorise toutes les origines

# Générer une clé secrète aléatoire à chaque démarrage
def generate_secret_key():
    return base64.urlsafe_b64encode(os.urandom(24)).decode('utf-8')

app.config['JWT_SECRET_KEY'] = generate_secret_key()  # Génération de la clé secrète
jwt = JWTManager(app)

@app.route('/secure-endpoint', methods=['GET'])
@jwt_required()  # Assurez-vous d'importer et d'utiliser jwt_required
def secure_endpoint():
    return {"message": "Vous êtes connecté !"}

# Connexion à la base de données PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='geomecano',
        user='postgres',  # Utilisateur PostgreSQL
        password='root'  # Remplacez par votre mot de passe PostgreSQL
    )
    return conn

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('name')  # Utiliser 'name' pour le nom d'utilisateur
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')  # Récupérer le numéro de téléphone
    role = data.get('role', 'client')  # Définir un rôle par défaut si non spécifié

    # Hacher le mot de passe
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insérer l'utilisateur dans la base de données
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO users (username, password, email, phone, role) VALUES (%s, %s, %s, %s, %s)',
        (username, hashed_password.decode('utf-8'), email, phone, role)  # Décoder le hachage en utf-8
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Utilisateur enregistré avec succès!'}), 201

@app.route('/api/workshops', methods=['POST'])
def register_workshop():
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    phone = data.get('phone')
    email = data.get('email')
    website = data.get('website')
    password = data.get('password')  # Récupérer le mot de passe

    # Hacher le mot de passe
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insérer l'atelier dans la base de données
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO workshops (name, address, phone_number, email, website, password) VALUES (%s, %s, %s, %s, %s, %s)',
        (name, address, phone, email, website, hashed_password.decode('utf-8'))
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Atelier enregistré avec succès!'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    # Vérifiez si l'utilisateur existe et si le mot de passe correspond
    if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):  # Vérifier le mot de passe avec bcrypt
        access_token = create_access_token(identity={'id': user[0], 'name': user[1], 'email': user[3], 'phone': user[4], 'role': user[5]})
        return jsonify({'token': access_token}), 200
    return jsonify({'message': 'Email ou mot de passe incorrect.'}), 401

@app.route('/api/user', methods=['GET'])
@jwt_required()
def get_user():
    current_user = get_jwt_identity()
    return jsonify(current_user), 200

if __name__ == '__main__':
    app.run(port=8080)
