from flask import Flask, request, jsonify
import os
import base64
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
import psycopg2
import bcrypt  # Assurez-vous d'importer bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

import os
import requests


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

    # Définir le dossier d'upload
    upload_folder = '/home/delkael/Téléchargements/projet2/mecano_project/public/upload'
    
    # Créer le dossier s'il n'existe pas
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    # Chemin du fichier de photo de profil
    file_path = os.path.join(upload_folder, f'user_{user_id}_profile.jpg')
    
    # Vérifier et supprimer l'ancien fichier s'il existe
    if os.path.exists(file_path):
        os.remove(file_path)
    
    try:
        # Sauvegarder le nouveau fichier
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
    if not all(key in data for key in ['message', 'type', 'user_id', 'created_at','workshop_id', 'workshop_messages','rdv_id']):
        return jsonify({"message": "Données manquantes."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insérer la notification dans la base de données
        cursor.execute(
            """
            INSERT INTO notifications (message, type, user_id, created_at, workshop_id, workshop_messages, rdv_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
            """,
            (data['message'], data['type'], data['user_id'], data['created_at'], data['workshop_id'], data['workshop_messages'],data['rdv_id'])
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
            SELECT message, type, workshop_messages 
            FROM notifications
            WHERE rdv_id = %s
        """, (workshop_id,))
        
        # Récupérer tous les résultats
        notifications = cursor.fetchall()
        print(f"Fetched notifications: {notifications}")  # Debug message
        
        # Stocker les résultats dans des variables
        messages = [notification[0] for notification in notifications]
        types = [notification[1] for notification in notifications]
        workshop_messages = [notification[2] for notification in notifications]
 
    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
    
    # Vous pouvez retourner les variables ou les structurer comme vous le souhaitez
    return jsonify({
        "messages": messages,
        "types": types,
        "workshop_messages": workshop_messages
    })



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

@app.route('/api/workshops/<int:id>', methods=['PUT'])
def update_workshop(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.json
    name = data.get('name')
    address = data.get('address')
    phone_number = data.get('phone_number')
    email = data.get('email')
    website = data.get('website')

    try:
        cursor.execute("""
            UPDATE workshops
            SET name = %s, address = %s, phone_number = %s, email = %s, website = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (name, address, phone_number, email, website, id))
        
        conn.commit()
        return jsonify({'message': 'Atelier mis à jour avec succès'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/workshops', methods=['GET'])
def get_workshops():
    conn = get_db_connection()
    cursor = conn.cursor()
       
    try:
        
        cursor.execute("SELECT * FROM workshops")
        workshops = cursor.fetchall()
       
        
        return jsonify(workshops)
    
    except psycopg2.Error as e:
        print(f'Erreur lors de la récupération des ateliers : {e}')
        return jsonify({'error': 'Erreur lors de la récupération des ateliers'}), 500

###################################################################################################################

# API pour recevoir et stocker les informations de contact
@app.route('/api/contact', methods=['POST'])
def submit_contact():
    data = request.json
    
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')

    if not (name and email and subject and message):
        return jsonify({"error": "All fields are required."}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO contacts (name, email, subject, message) VALUES (%s, %s, %s, %s)",
            (name, email, subject, message)
        )
        conn.commit()
        return jsonify({"message": "Contact information submitted successfully!"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@app.route('/api/support/tickets', methods=['GET'])
def get_support_tickets():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, name, email, subject, message FROM contacts ORDER BY created_at DESC")
        tickets = cur.fetchall()
        return jsonify(tickets), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@app.route('/api/support/respond', methods=['POST'])
def respond_to_ticket():
    data = request.json
    contact_id = data.get('contact_id')
    response_text = data.get('response')

    if not (contact_id and response_text):
        return jsonify({"error": "Missing contact ID or response text"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO responses (contact_id, response) VALUES (%s, %s)",
            (contact_id, response_text)
        )
        conn.commit()
        return jsonify({"message": "Response recorded successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@app.route('/api/workshops/<int:workshop_id>/status', methods=['PUT'])
def update_workshop_status(workshop_id):
    data = request.get_json()
    is_blocked = data.get('is_blocked')

    if is_blocked is None:
        return jsonify({"error": "Missing is_blocked field"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Calculez is_visible comme l'inverse de is_blocked
        is_visible = not is_blocked

        # Exécutez la requête SQL pour mettre à jour la colonne is_visible
        cur.execute(
            "UPDATE workshops SET is_visible = %s WHERE id = %s",
            (is_visible, workshop_id)
        )
        conn.commit()
        return jsonify({"message": "Workshop status updated successfully", "is_visible": is_visible}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()


#################################################################################################################

@app.route('/localisations', methods=['GET'])
def get_localisations():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT workshops_id, latitude, longitude FROM localisation")
    localisations = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Convert to a list of dictionaries
    result = [
        {"id": loc[0], "lat": loc[1], "lon": loc[2]} 
        for loc in localisations
    ]
    
    return jsonify(result)


@app.route('/workshops', methods=['GET'])
def get_workshops_localisation():
    ids = request.args.get('ids', '')
    if not ids:
        return jsonify([])  # Retourne une liste vide si aucun ID n'est fourni

    ids_list = ids.split(',')
    query = 'SELECT * FROM workshops WHERE id IN %s'
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (tuple(ids_list),))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # Formatage des résultats en JSON
        workshops = [
            {
                'id': row[0],
                'name': row[1],
                'address': row[2],
                'phone': row[3],
                'email': row[4],
                'website': row[5],
                'opening_hours': row[6],
                'created_at': row[7],
                'updated_at': row[8],
                'password': row[9],
                'latitude': row[10],
                'longitude': row[11],
                'description': row[12],
                'active': row[13]
            }
            for row in rows
        ]
        return jsonify(workshops)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
    if user and bcrypt.checkpw(password.encode('utf-8'), user[9].encode('utf-8')):  # Vérifier le mot de passe avec bcrypt
        access_token = create_access_token(identity={'id': user[0], 'name': user[1], 'adresse': user[2], 'phone_number': user[3], 'email': user[4],'website': user[5],'role': user[5],'role': user[5]})
        return jsonify({'token': access_token}), 200
    return jsonify({'message': 'Email ou mot de passe incorrect.'}), 401

@app.route('/api/workshops', methods=['POST'])
def add_workshop():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    opening_time = data.get('openingTime')

    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Erreur de connexion à la base de données.'}), 500

    cursor = conn.cursor()

    try:
        # Insertion des données dans la table workshops
        cursor.execute("""
            INSERT INTO workshops (latitude, longitude, opening_time)
            VALUES (%s, %s, %s)
        """, (latitude, longitude, opening_time))
        conn.commit()
        return jsonify({'message': 'Atelier enregistré avec succès !'}), 201
    except Exception as e:
        print(f'Erreur: {e}')
        conn.rollback()
        return jsonify({'error': 'Erreur lors de l\'enregistrement'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/workshop/<int:workshop_id>', methods=['GET'])
def get_workshop_by_id(workshop_id):
    query = 'SELECT * FROM workshops WHERE id = %s'
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (workshop_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            workshop = {
                'id': row[0],
                'name': row[1],
                'address': row[2],
                'phone': row[3],
                'email': row[4],
                'website': row[5],
                'opening_hours': row[6],
                'created_at': row[7],
                'updated_at': row[8],
                'password': row[9],
                'latitude': row[10],
                'longitude': row[11],
                'description': row[12],
                'active': row[13]
            }
            return jsonify(workshop)
        else:
            return jsonify({'error': 'Workshop not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/save-workshop', methods=['POST'])
def save_workshop():
    data = request.json
    workshop_id = data.get('id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    opening_hours = data.get('openingTime')

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        query = 'UPDATE workshops SET latitude = %s, longitude = %s, opening_hours = %s, updated_at = NOW() WHERE id = %s RETURNING *'
        cur.execute(query, (latitude, longitude, opening_hours, workshop_id))
        updated_workshop = cur.fetchone()
        conn.commit()

        if updated_workshop:
            return jsonify({
                'id': updated_workshop[0],
                'name': updated_workshop[1],
                'address': updated_workshop[2],
                'phone_number': updated_workshop[3],
                'email': updated_workshop[4],
                'website': updated_workshop[5],
                'opening_hours': updated_workshop[6],
                'latitude': updated_workshop[10],
                'longitude': updated_workshop[11],
                'updated_at': updated_workshop[8]
            })
        else:
            return jsonify({'error': 'Workshop not found'}), 404

    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred while updating the workshop'}), 500

    finally:
        cur.close()
        conn.close()


@app.route('/api/atelier/opening-time', methods=['GET'])
def get_opening_time():
    try:
        
        # Vous devriez valider le token ici et obtenir l'ID de l'utilisateur

        user_id = 47  # Remplacez ceci par la logique de récupération de l'ID de l'utilisateur à partir du token

        conn = get_db_connection()
        cur = conn.cursor()
        query = 'SELECT opening_time FROM workshops WHERE id = %s'
        cur.execute(query, (user_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result:
            return jsonify({'opening_time': result[0]})
        else:
            return jsonify({'message': 'Atelier non trouvé'}), 404
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'message': 'Erreur serveur'}), 500
####################################################################################

@app.route('/api/rendezvous/user/<int:user_id>', methods=['GET'])
def recuperer_rdv_reservations_users(user_id):
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

######################################################################################################

@app.route('/api/rendezvous/users/<int:rendezvous_id>', methods=['DELETE'])
def annuler_rdv_users(rendezvous_id):
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


@app.route('/api/users/notifications', methods=['POST'])
def create_notification_users():
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

@app.route('/api/rendezvous/users/<int:user_id>', methods=['GET'])
def recuperer_rdv_users(user_id):
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


@app.route('/api/rendezvous/user/<int:rendezvous_id>', methods=['DELETE'])
def annuler_rdv_user(rendezvous_id):
    try:
        
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


# Configuration des variables CinetPay
CINEPAY_API_KEY = os.getenv('1519658666d9e16f2c0819.57979115')
CINEPAY_SITE_ID = os.getenv('5879320')
CINEPAY_NOTIFY_URL = 'http://localhost:8080/notify'
CINEPAY_RETURN_URL = 'http://localhost:8080/thankyou'

@app.route('/api/payment', methods=['POST'])
def process_payment():
    data = request.json

    # Préparer les données pour CinetPay
    payload = {
        "apikey": CINEPAY_API_KEY,
        "site_id": CINEPAY_SITE_ID,
        "transaction_id": data.get('transaction_id'),
        "amount": data.get('amount'),
        "currency": data.get('currency', 'XOF'),
        "description": data.get('description'),
        "notify_url": CINEPAY_NOTIFY_URL,
        "return_url": CINEPAY_RETURN_URL,
        "channels": "ALL",
        "customer_name": data.get('customer_name'),
        "customer_surname": data.get('customer_surname'),
        "customer_phone_number": data.get('customer_phone_number'),
        "customer_email": data.get('customer_email'),
        "customer_address": data.get('customer_address'),
        "customer_city": data.get('customer_city'),
        "customer_country": data.get('customer_country'),
        "customer_state": data.get('customer_state'),
        "customer_zip_code": data.get('customer_zip_code'),
    }

    # Envoyer la requête à l'API CinetPay
    response = requests.post('https://api-checkout.cinetpay.com/v2/payment', json=payload)
    response_data = response.json()

    if response_data['code'] == '201':
        payment_url = response_data['data']['payment_url']
        return jsonify({'payment_url': payment_url})
    else:
        return jsonify({'error': response_data['message']}), 400

@app.route('/notify', methods=['POST'])
def notify():
    # Traiter les notifications de paiement ici
    return jsonify({'status': 'Notification received'})

@app.route('/thankyou')
def thankyou():
    return 'Thank you for your payment!'

if __name__ == '__main__':
    app.run(port=8080)
