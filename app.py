from flask import Flask, request, jsonify
import os
import base64
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
import psycopg2
import bcrypt  # Assurez-vous d'importer bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

import os



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


# Dossier pour stocker les photos
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# Connexion à la base de données PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='geomecano',
            user='postgres',  # Utilisateur PostgreSQL
            password='root'  # Remplacez par votre mot de passe PostgreSQL
        )
        return conn
    except Exception as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None

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
    if conn is None:
        return jsonify({'error': 'Erreur de connexion à la base de données.'}), 500

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
    if conn is None:
        return jsonify({'error': 'Erreur de connexion à la base de données.'}), 500

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
    if conn is None:
        return jsonify({'error': 'Erreur de connexion à la base de données.'}), 500

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    # Vérifiez si l'utilisateur existe et si le mot de passe correspond
    if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):  # Vérifier le mot de passe avec bcrypt
        access_token = create_access_token(identity={'id': user[0], 'name': user[1], 'email': user[3], 'phone': user[7], 'role': user[5]})
        return jsonify({'token': access_token}), 200
    return jsonify({'message': 'Email ou mot de passe incorrect.'}), 401

@app.route('/api/user', methods=['GET'])
@jwt_required()
def get_user():
    current_user = get_jwt_identity()  # Récupérer l'identité de l'utilisateur à partir du token
    return jsonify(current_user), 200  # Renvoie les informations de l'utilisateur


@app.route('/api/login/atelier', methods=['POST'])
def login_atelier():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Erreur de connexion à la base de données.'}), 500

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workshops WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    # Vérifiez si l'utilisateur existe et si le mot de passe correspond
    if user and bcrypt.checkpw(password.encode('utf-8'), user[10].encode('utf-8')):  # Vérifier le mot de passe avec bcrypt
        access_token = create_access_token(identity={'id': user[0], 'name': user[1], 'adresse': user[2], 'phone_number': user[3], 'email': user[4],'website': user[5],'role': user[5],'role': user[5]})
        return jsonify({'token': access_token}), 200
    return jsonify({'message': 'Email ou mot de passe incorrect.'}), 401


@app.route('/api/atelier', methods=['GET'])
@jwt_required()
def get_user_atelier():
    current_user = get_jwt_identity()  # Récupérer l'identité de l'utilisateur à partir du token
    return jsonify(current_user), 200  # Renvoie les informations de l'utilisateur




########################################################################################################################


@app.route('/api/ateliers', methods=['GET'])
def get_ateliers():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Erreur de connexion à la base de données.'}), 500

    cur = conn.cursor()
    cur.execute('SELECT id, name, address, phone_number, email, website, opening_hours, latitude, longitude FROM workshops')
    ateliers = cur.fetchall()
    cur.close()
    conn.close()

    atelier_list = []
    for atelier in ateliers:
        atelier_dict = {
            'id': atelier[0],
            'name': atelier[1],
            'address': atelier[2],
            'phone_number': atelier[3],
            'email': atelier[4],
            'website': atelier[5],
            'opening_hours': atelier[6],
            'latitude': atelier[7],
            'longitude': atelier[8]
        }
        atelier_list.append(atelier_dict)

    return jsonify(atelier_list)


@app.route('/api/ateliers/<int:id>', methods=['GET'])
def get_atelier(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Erreur de connexion à la base de données.'}), 500

    cur = conn.cursor()
    cur.execute('SELECT id, name, address, phone_number, email, website, opening_hours, latitude, longitude FROM workshops WHERE id = %s', (id,))
    atelier = cur.fetchone()
    cur.close()
    conn.close()

    if atelier is None:
        return jsonify({'error': 'Atelier not found'}), 404

    atelier_dict = {
        'id': atelier[0],
        'name': atelier[1],
        'address': atelier[2],
        'phone_number': atelier[3],
        'email': atelier[4],
        'website': atelier[5],
        'opening_hours': atelier[6],
        'latitude': atelier[7],
        'longitude': atelier[8]
    }

    return jsonify(atelier_dict)

@app.route('/api/ateliers/services', methods=['GET'])
def get_ateliers_by_services():
    service_id = request.args.get('service_id')
    
    if not service_id:
        return jsonify({'error': 'Service ID is required'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Erreur de connexion à la base de données.'}), 500

    cursor = conn.cursor()
    
    # Récupérer les ateliers associés à un service spécifique
    cursor.execute(
        '''
        SELECT w.id, w.name, w.address, w.phone_number, w.email, w.website, w.opening_hours, w.latitude, w.longitude
        FROM workshops w
        JOIN services ws ON w.id = ws.workshop_id
        WHERE ws.service_id = %s
        ''', (service_id,)
    )
    ateliers = cursor.fetchall()
    cursor.close()
    conn.close()

    if not ateliers:
        return jsonify([])  # Retourner une liste vide si aucun atelier n'est trouvé

    atelier_list = []
    for atelier in ateliers:
        atelier_dict = {
            'id': atelier[0],
            'name': atelier[1],
            'address': atelier[2],
            'phone_number': atelier[3],
            'email': atelier[4],
            'website': atelier[5],
            'opening_hours': atelier[6],
            'latitude': atelier[7],
            'longitude': atelier[8]
        }
        atelier_list.append(atelier_dict)

    return jsonify(atelier_list)


@app.route('/api/services', methods=['GET'])
def get_services():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Erreur de connexion à la base de données.'}), 500

    cur = conn.cursor()
    
    # Correction de la requête SQL pour récupérer les services
    cur.execute('SELECT * FROM services')
    services = cur.fetchall()
    cur.close()
    conn.close()

    services_list = []
    for service in services:
        service_dict = {
            'id': service[0],
            'name': service[1],
            'description': service[2],
            'workshop_id': service[3],
        }
        services_list.append(service_dict)

    return jsonify(services_list)

##############################################################################################################

@app.route('/api/reservations', methods=['POST'])
def create_reservation():
    data = request.json

    # Vérifier que les données nécessaires sont présentes
    required_keys = ['user_id', 'atelier_id', 'date', 'time', 'services', 'message']
    if not all(key in data for key in required_keys):
        return jsonify({"message": "Données manquantes"}), 400

    # Vérifier que les services est une liste non vide
    if not isinstance(data['services'], list) or not data['services']:
        return jsonify({"message": "Les services doivent être une liste non vide"}), 400

    # Validation des types
    if not isinstance(data['user_id'], int) or not isinstance(data['atelier_id'], int):
        return jsonify({"message": "user_id et atelier_id doivent être des entiers"}), 400

    # Convertir la liste des services en chaîne
    try:
        services_str = ','.join(map(str, data['services']))
    except Exception:
        return jsonify({"message": "Erreur lors de la conversion des services"}), 400

    # Connexion à la base de données
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Préparer la commande SQL
        sql = """
        INSERT INTO reservations (user_id, atelier_id, date, time, services, message)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        # Exécuter la commande SQL
        cursor.execute(sql, (
            data['user_id'],
            data['atelier_id'],
            data['date'],
            data['time'],
            services_str,
            data.get('message', '')
        ))
        conn.commit()  # Valider les changements dans la base de données
        return jsonify({"message": "Réservation créée avec succès"}), 201
    except Exception as e:
        print(f"Erreur : {e}")  # Afficher l'erreur dans la console pour le débogage
        return jsonify({"message": "Erreur lors de la création de la réservation"}), 500
    finally:
        cursor.close()  # Fermer le curseur
        conn.close()    # Fermer la connexion



@app.route('/api/services/<int:workshop_id>', methods=['GET'])
def get_services_id(workshop_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"message": "Erreur de connexion à la base de données."}), 500

    cursor = conn.cursor()

    # Préparer la commande SQL
    sql = "SELECT id, name FROM services WHERE workshop_id = %s"
    try:
        cursor.execute(sql, (workshop_id,))
        services = cursor.fetchall()
        services_list = [{"id": row[0], "name": row[1]} for row in services]
        return jsonify(services_list), 200
    except Exception as e:
        return jsonify({"message": "Erreur lors de la récupération des services", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/reservations', methods=['GET'])
def get_reservations():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservations")
        reservations = cursor.fetchall()
        result = [
            {
                "id": row[0],
                "user_id": row[1],
                "atelier_id": row[2],
                "date": row[3],
                "time": row[4],
                "services": row[5].split(','),  # Convertir en liste
                "message": row[6]
            } for row in reservations
        ]
        return jsonify(result), 200
    except Exception:
        return jsonify({"message": "Erreur lors de la récupération des réservations"}), 500
    finally:
        cursor.close()
        conn.close()

#######################################################################################################

@app.route('/api/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user_data = request.get_json()
        user_id = user_id  # Assurez-vous que l'id de l'utilisateur est fourni

        if not user_id:
            return jsonify({"message": "L'identifiant de l'utilisateur est requis."}), 400

        # Connexion à la base de données
        conn = get_db_connection()
        cursor = conn.cursor()

        # Exécuter la commande SQL pour mettre à jour les informations de l'utilisateur
        cursor.execute("""
            UPDATE users
            SET username = %s, email = %s, phone = %s
            WHERE id = %s
        """, (user_data['name'], user_data['email'], user_data['phone'], user_id))

        conn.commit()

        return jsonify({"message": "Informations de l'utilisateur mises à jour avec succès."}), 200
    except Exception as e:
        print(e)  # Pour le débogage
        return jsonify({"message": "Erreur lors de la mise à jour des informations de l'utilisateur."}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/atelier/<int:user_id>', methods=['PUT'])
def update_atelier(user_id):
    try:
        user_data = request.get_json()
        user_id = user_id  # Assurez-vous que l'id de l'utilisateur est fourni

        if not user_id:
            return jsonify({"message": "L'identifiant de l'utilisateur est requis."}), 400

        # Connexion à la base de données
        conn = get_db_connection()
        cursor = conn.cursor()

        # Exécuter la commande SQL pour mettre à jour les informations de l'utilisateur
        cursor.execute("""
            UPDATE workshops
            SET name = %s, email = %s, phone_number = %s, address  = %s, website = %s
            WHERE id = %s
        """, (user_data['name'], user_data['email'], user_data['phone'],user_data['address'],user_data['website'], user_id))

        conn.commit()

        return jsonify({"message": "Informations de l'utilisateur mises à jour avec succès."}), 200
    except Exception as e:
        print(e)  # Pour le débogage
        return jsonify({"message": "Erreur lors de la mise à jour des informations de l'utilisateur."}), 500
    finally:
        cursor.close()
        conn.close()

#################################################################################################################


import os

@app.route('/api/user/<int:user_id>/profile-picture', methods=['PUT'])
def update_profile_picture(user_id):
    if 'profile_picture' not in request.files:
        return jsonify({"message": "Aucun fichier n'a été téléchargé."}), 400
    
    profile_picture = request.files['profile_picture']

    if profile_picture.filename == '':
        return jsonify({"message": "Nom de fichier invalide."}), 400

    # Générer un chemin pour sauvegarder la photo
    upload_folder = 'uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    file_path = os.path.join(upload_folder, f'user_{user_id}_profile.jpg')
    
    try:
        profile_picture.save(file_path)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Mettre à jour le chemin de la photo de profil dans la base de données
        cursor.execute("UPDATE users SET photo = %s WHERE id = %s", (file_path, user_id))
        conn.commit()

        return jsonify({"message": "Photo de profil mise à jour avec succès.", "profilePictureUrl": file_path}), 200

    except Exception as e:
        print(f"Erreur lors de la mise à jour de la photo de profil: {e}")
        return jsonify({"message": "Erreur lors de la mise à jour de la photo de profil."}), 500

    finally:
        cursor.close()
        conn.close()

@app.route('/api/user/<int:user_id>/profile-picture', methods=['GET'])
def get_profile_picture(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT photo FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        
        if result:
            # Supposons que result[0] contient le chemin de la photo
            profile_picture_url = result[0] 
            # Si vous stockez le chemin relatif dans la base de données
            if profile_picture_url:
                # Assurez-vous que l'URL est accessible
                profile_picture_url = f'/uploads/user_{user_id}_profile.jpg'
                return jsonify({"profilePictureUrl": profile_picture_url}), 200
            else:
                return jsonify({"message": "Photo de profil non trouvée."}), 404
        else:
            return jsonify({"message": "Utilisateur non trouvé."}), 404

    except Exception as e:
        print(e)
        return jsonify({"message": "Erreur lors de la récupération de la photo de profil."}), 500

    finally:
        cursor.close()
        conn.close()



@app.route('/api/reservations/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    try:
        # Connexion à la base de données
        conn = get_db_connection()
        cursor = conn.cursor()

        # Exécuter la commande SQL pour supprimer la réservation
        cursor.execute("DELETE FROM reservations WHERE id = %s", (reservation_id,))
        conn.commit()

        return jsonify({"message": "Réservation supprimée avec succès."}), 200
    except Exception as e:
        print(e)  # Pour le débogage
        return jsonify({"message": "Erreur lors de la suppression de la réservation."}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/reservations/<int:user_id>', methods=['GET'])
def recuperer_reservations(user_id):
    try:
        # Connexion à la base de données
        conn = get_db_connection()
        cursor = conn.cursor()

        # Exécuter la commande SQL pour récupérer toutes les réservations de l'utilisateur
        cursor.execute("SELECT * FROM reservations WHERE user_id = %s", (user_id,))
        reservations = cursor.fetchall()  # Récupérer toutes les réservations

        if not reservations:
            return jsonify({"message": "Aucune réservation trouvée pour cet utilisateur."}), 404

        # Préparer les résultats
        results = []
        for reservation in reservations:
            results.append({
                "id": reservation[0],  # Assurez-vous que l'index correspond à votre schéma
                "date": reservation[3],  # Exemple d'index
                "time": reservation[4],  # Exemple d'index
                "details": reservation[5] , # Exemple d'index
                "message": reservation[6]

            })

        return jsonify(results), 200

    except Exception as e:
        print(e)  # Pour le débogage
        return jsonify({"message": "Erreur lors de la récupération des réservations."}), 500

    finally:
        cursor.close()
        conn.close()



##################################################################################################################################################


@app.route('/api/selectusers', methods=['GET'])
def get_users_select():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, role, phone, created_at FROM users;')
    users = cursor.fetchall()
    
    users_list = []
    for user in users:
        users_list.append({
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'role': user[3],
            'phone': user[4],
            'created_at': user[5].isoformat()  # Formatage de la date
        })
    
    cursor.close()
    conn.close()
    return jsonify(users_list)

@app.route('/api/rese', methods=['GET'])
def get_res():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        reservations = cursor.fetchall()
        result = [
            {
                "id": row[0],
                "user_id": row[1],
                "atelier_id": row[2],
                "date": row[3],
                "time": row[4],
                "services": row[5].split(','),  # Convertir en liste
                "message": row[6]
            } for row in reservations
        ]
        return jsonify(result), 200
    except Exception:
        return jsonify({"message": "Erreur lors de la récupération des réservations"}), 500
    finally:
        cursor.close()
        conn.close()


# Route pour supprimer un utilisateur par son ID
@app.route('/api/selectusers/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s;', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Utilisateur supprimé avec succès'}), 200

##############################################################################################################################################

# Route pour ajouter un nouveau service
@app.route('/services', methods=['POST'])
def create_service():
    data = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO services (name, description, workshop_id)
            VALUES (%s, %s, %s) RETURNING id;
            """,
            (data['name'], data['description'], data['workshop_id'])
        )
        new_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"id": new_id, "name": data['name'], "description": data['description'], "workshop_id": data['workshop_id']}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour récupérer tous les services d'un atelier
@app.route('/services/workshop/<int:workshop_id>', methods=['GET'])
def get_services_ateliers(workshop_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM services WHERE workshop_id = %s;", (workshop_id,))
        services = cursor.fetchall()
        services_list = []
        for service in services:
            services_list.append({
                "id": service[0],
                "name": service[1],
                "description": service[2],
                "workshop_id": service[3]
            })
        cursor.close()
        conn.close()
        return jsonify(services_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

    


# Route pour mettre à jour un service existant
@app.route('/services/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    data = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE services
            SET name = %s, description = %s, workshop_id = %s
            WHERE id = %s;
            """,
            (data['name'], data['description'], data['workshop_id'], service_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"id": service_id, "name": data['name'], "description": data['description'], "workshop_id": data['workshop_id']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour supprimer un service
@app.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM services WHERE id = %s;", (service_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

###################################################################################################################################

@app.route('/api/rendezvous/<int:user_id>', methods=['GET'])
def recuperer_rdv_reservations(user_id):
    try:
        # Connexion à la base de données
        conn = get_db_connection()
        cursor = conn.cursor()

        # Exécuter la commande SQL pour récupérer toutes les réservations de l'utilisateur
        cursor.execute("SELECT * FROM reservations WHERE atelier_id = %s", (user_id,))
        reservations = cursor.fetchall()  # Récupérer toutes les réservations

        if not reservations:
            return jsonify({"message": "Aucune réservation trouvée pour cet utilisateur."}), 404

        # Préparer les résultats
        results = []
        for reservation in reservations:
            results.append({
                "id": reservation[0],  # Assurez-vous que l'index correspond à votre schéma
                "date": reservation[3],  # Exemple d'index
                "time": reservation[4],  # Exemple d'index
                "details": reservation[5] , # Exemple d'index
                "message": reservation[6],
                "user_id": reservation[1],
                "atelier_id": reservation[2],
                "services": reservation[5]
            })

        return jsonify(results), 200

    except Exception as e:
        print(e)  # Pour le débogage
        return jsonify({"message": "Erreur lors de la récupération des réservations."}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/api/rendezvous/<int:rendezvous_id>', methods=['DELETE'])
def annuler_rdv(rendezvous_id):
    try:
        data = request.get_json()
        reason = data.get('reason', '')  # Obtenir la raison de l'annulation

        conn = get_db_connection()
        cursor = conn.cursor()

        # Supprimer le rendez-vous
        cursor.execute("DELETE FROM reservations WHERE id = %s RETURNING user_id, atelier_id", (rendezvous_id,))
        result = cursor.fetchone()
        conn.commit()  # Valider les modifications
        return jsonify({"message": "Rendez-vous annulé avec succès."}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Erreur lors de l'annulation du rendez-vous."}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/api/notifications', methods=['POST'])
def create_notification():
    data = request.get_json()
  
    # Vérifiez que toutes les données nécessaires sont présentes
    if not all(key in data for key in ['message', 'type', 'user_id', 'created_at','workshop_id', 'workshop_messages']):
        return jsonify({"message": "Données manquantes."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insérer la notification dans la base de données
        cursor.execute(
            """
            INSERT INTO notifications (message, type, user_id, created_at, workshop_id, workshop_messages)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
            """,
            (data['message'], data['type'], data['user_id'], data['created_at'], data['workshop_id'], data['workshop_messages'])
        )
        
        notification_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Notification créée avec succès!", "id": notification_id}), 201
    except Exception as e:
        print(f"Erreur lors de l'insertion de la notification: {str(e)}")
        return jsonify({"message": "Erreur lors de la création de la notification."}), 500

@app.route('/api/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    print(data)
    # Vérifiez que toutes les données nécessaires sont présentes
    if not all(key in data for key in ['subject', 'message', 'user_id', 'workshop_id', 'created_at']):
        return jsonify({"message": "Données manquantes."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insérer le message dans la base de données
        cursor.execute(
            """
            INSERT INTO contactmessages (subject, message, user_id, workshop_id, created_at)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
            """,
            (data['subject'], data['message'], data['user_id'], data['workshop_id'], data['created_at'])
        )
        
        message_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Message créé avec succès!", "id": message_id}), 201
    except Exception as e:
        print(f"Erreur lors de l'insertion du message: {str(e)}")
        return jsonify({"message": "Erreur lors de la création du message."}), 500


#####################################################################################################################################

@app.route('/api/atelier/photos', methods=['POST'])
def upload_photos():
    data = request.json
    photos = data.get('photos', [])
    atelier_id = 47  # Remplacez par l'ID de l'atelier concerné ou récupérez-le dynamiquement

    if not photos:
        return jsonify({"error": "Aucune photo à télécharger"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    for photo in photos:
        cur.execute(
            "UPDATE ateliers SET photo = %s WHERE id = %s",
            (photo, atelier_id)
        )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Photos téléchargées avec succès", "photos": photos}), 200



@app.route('/upload/<string:specific_id>', methods=['POST'])
def upload_image(specific_id):
    data = request.json
    image_data = data.get('image_data')

    if image_data:
        conn = get_db_connection()  # Assurez-vous d'avoir une fonction pour récupérer la connexion
        cur = conn.cursor()

        try:
            # Mettre à jour la colonne 'photo' avec l'image en Base64 pour l'atelier spécifique
            cur.execute(
                "UPDATE workshops SET photo = %s WHERE id = %s",
                (image_data, specific_id)
            )
            conn.commit()

            return jsonify({"message": "Image uploaded successfully!"}), 201
        except Exception as e:
            conn.rollback()  # Annuler en cas d'erreur
            return jsonify({"error": str(e)}), 500
        finally:
            cur.close()  # Fermez le curseur après l'exécution
            conn.close()  # Fermez la connexion à la base de données
    else:
        return jsonify({"error": "No image data provided"}), 400

################################################################################################################

import uuid

# Route pour ajouter une photo de profil
@app.route('/api/atelier/profile-picture', methods=['POST'])
def add_profile_picture():
    if 'profile_picture' not in request.files:
        return jsonify({"message": "Aucun fichier n'a été téléchargé."}), 400
    
    profile_picture = request.files['profile_picture']

    if profile_picture.filename == '':
        return jsonify({"message": "Nom de fichier invalide."}), 400

    # Définir le dossier d'upload
    upload_folder = '/home/delkael/Téléchargements/projet2/mecano_project/public/uploads'
    
    # Créer le dossier s'il n'existe pas
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    # Utiliser l'ID de l'atelier qui peut être passé via le corps de la requête
    workshop_id = request.form.get('workshop_id')  # Assurez-vous d'envoyer `workshop_id` dans la requête
    
    # Générer un nom de fichier unique avec un UUID
    unique_id = uuid.uuid4()
    file_path = os.path.join(upload_folder, f'workshop_{workshop_id}_profile_{unique_id}.jpg')
    
    try:
        profile_picture.save(file_path)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insérer le chemin de la photo de profil dans la base de données
        cursor.execute("INSERT INTO photos_atelier (file_path, workshop_id) VALUES (%s, %s) RETURNING id", (file_path, workshop_id))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Photo de profil ajoutée avec succès.", "profilePictureUrl": file_path}), 201
    except Exception as e:
        return jsonify({"message": "Erreur lors de l'ajout de la photo.", "error": str(e)}), 500


# Route pour récupérer toutes les photos
@app.route('/api/atelier/photos/<int:workshop_id>', methods=['GET'])
def get_photos(workshop_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, file_path FROM photos_atelier WHERE workshop_id = %s", (workshop_id,))
    photos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Formater les résultats pour les envoyer en JSON
    return jsonify([
        {"id": photo[0], "file_path": photo[1]}
        for photo in photos
    ]), 200

# Route pour supprimer une photo par ID
@app.route('/api/atelier/photos/<int:photo_id>/<int:workshop_id>', methods=['DELETE'])
def delete_photo_atelier(photo_id, workshop_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Récupérer le chemin de la photo avant de la supprimer
    cursor.execute("SELECT file_path FROM photos_atelier WHERE id = %s", (photo_id,))
    photo = cursor.fetchone()
    
    if photo is None:
        return jsonify({"message": "Photo non trouvée."}), 404
    
    # Supprimer la photo du système de fichiers
    file_path = photo[0]
    if os.path.exists(file_path):
        os.remove(file_path)

    # Supprimer l'entrée de la base de données
    cursor.execute("DELETE FROM photos_atelier WHERE workshop_id = %s AND id = %s", (workshop_id, photo_id))
    conn.commit()
    
    cursor.close()
    conn.close()
    
############################################################################################################################


@app.route('/api/discussions/<int:workshop_id>/messages', methods=['GET'])
def get_discussions(workshop_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Modifiez la requête SQL pour filtrer par workshop_id
    cursor.execute("""
       SELECT * FROM notifications WHERE workshop_id = %s;
    """, (workshop_id,))
    
    # Récupérez les résultats et transformez-les en une liste de dictionnaires
    discussions = cursor.fetchall()
    result = []
    
    for notification in discussions:
        notification_dict = {
            'id': notification[0],
            'message': notification[1],
            'type': notification[2],
            'user_id': notification[3],
            'created_at': notification[4],
            'workshop_id': notification[5],
            'workshop_messages': notification[6],
        }
        result.append(notification_dict)

    cursor.close()
    conn.close()
    
    return jsonify(result)  # Renvoie le résultat sous forme de JSON



@app.route('/api/messages/<int:user_id>', methods=['GET'])
def get_messages(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT workshop_messages, users_messages, created_at
        FROM contactmessages
        WHERE user_id = %s
    """, (user_id,))
    
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Transforme les résultats en une liste de dictionnaires
    result = [{'workshop_messages': msg[0], 'users_messages': msg[1], 'created_at': msg[2]} for msg in messages]
    
    return jsonify(result)

@app.route('/api/messages', methods=['POST'])
def send_message():
    conn = get_db_connection()
    cursor = conn.cursor()

    data = request.get_json()
    workshop_id = data.get('workshop_id')
    user_id = data.get('user_id')
    users_messages = data.get('users_messages')

    cursor.execute("""
        INSERT INTO contactmessages (workshop_id, user_id, users_messages)
        VALUES (%s, %s, %s)
    """, (workshop_id, user_id, users_messages))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'status': 'Message envoyé!'}), 201


###############################################################################################################

@app.route('/api/notifications/<int:workshop_id>', methods=['GET'])
def get_notifications(workshop_id):
    print(f"Fetching notifications for workshop ID: {workshop_id}")  # Debug message
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT *
            FROM notifications
            WHERE workshop_id = %s
        """, (workshop_id,))
        
        notifications = cursor.fetchall()
        print(f"Fetched notifications: {notifications}")  # Debug message
    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
    
    return jsonify(notifications)


#########################################################################################################################################


@app.route('/register/admin', methods=['POST'])
def register_admin():
    data = request.json
    nom = data.get('nom')
    mot_de_passe = data.get('mot_de_passe')
    role = data.get('role', 'admin')  # Défaut au rôle 'admin'

    if not nom or not mot_de_passe:
        return jsonify({"message": "Nom et mot de passe sont obligatoires"}), 400

    # Hacher le mot de passe
    hashed_password = generate_password_hash(mot_de_passe)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO admin (nom, mot_de_passe, role) VALUES (%s, %s, %s)",
            (nom, hashed_password, role)
        )
        conn.commit()
        return jsonify({"message": "Admin inscrit avec succès"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/login/admin', methods=['POST'])
def login_admin():
    data = request.json
    nom = data.get('nom')
    mot_de_passe = data.get('mot_de_passe')

    if not nom or not mot_de_passe:
        return jsonify({"message": "Nom et mot de passe sont obligatoires"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, nom, mot_de_passe FROM admin WHERE nom = %s", (nom,))
        admin = cursor.fetchone()

        if admin and check_password_hash(admin[2], mot_de_passe):
            return jsonify({"message": "Connexion réussie", "admin_id": admin[0]}), 200
        else:
            return jsonify({"message": "Nom ou mot de passe incorrect"}), 401
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/admin/<int:admin_id>', methods=['GET'])
def get_admin_data(admin_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, nom, role FROM admin WHERE id = %s", (admin_id,))
        admin = cursor.fetchone()

        if admin:
            admin_data = {
                "id": admin[0],
                "nom": admin[1],
                "role": admin[2]
            }
            return jsonify(admin_data), 200
        else:
            return jsonify({"message": "Admin non trouvé"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/users/all', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, username, email, role, created_at, phone FROM users")
        users = cursor.fetchall()

        users_list = []
        for user in users:
            users_list.append({
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "role": user[3],
                "created_at": user[4],
                "phone": user[5]
            })

        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user_all(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.json
    try:
        cursor.execute("""
            UPDATE users
            SET username = %s, email = %s, role = %s, phone = %s
            WHERE id = %s RETURNING id
        """, (data['username'], data['email'], data['role'], data['phone'], user_id))
        updated_id = cursor.fetchone()

        if updated_id:
            conn.commit()
            return jsonify({"message": "Utilisateur mis à jour avec succès"}), 200
        else:
            return jsonify({"message": "Utilisateur non trouvé"}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({"message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/users', methods=['POST'])
def add_user():
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.json
    try:
        cursor.execute("""
            INSERT INTO users (username, email, role, phone)
            VALUES (%s, %s, %s, %s) RETURNING id
        """, (data['username'], data['email'], data['role'], data['phone']))
        user_id = cursor.fetchone()[0]
        conn.commit()

        # Récupérer l'utilisateur ajouté
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        user_dict = {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "role": user[3],
            "phone": user[4],
            "created_at": user[5].strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify(user_dict), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()





if __name__ == '__main__':
    app.run(port=8080)
