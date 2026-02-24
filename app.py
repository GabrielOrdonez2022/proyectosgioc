import psycopg2
from flask import Flask, jsonify, request


app = Flask(__name__)
# Configurar la conexión a PostgreSQL
app.config['POSTGRES_HOST'] = 'localhost'
app.config['POSTGRES_DB'] = 'personajesminecraft'
app.config['POSTGRES_USER'] = 'gabriel'
app.config['POSTGRES_PASSWORD'] = '1234'
app.config['POSTGRES_PORT'] = '5432'  # Puerto predeterminado de PostgreSQL


def connect_to_database():
   connection = psycopg2.connect(
       host=app.config['POSTGRES_HOST'],
       database=app.config['POSTGRES_DB'],
       user=app.config['POSTGRES_USER'],
       password=app.config['POSTGRES_PASSWORD'],
       port=app.config['POSTGRES_PORT']
   )
   return connection


# Definición de los personajes con IDs
characters = {
   1: {
       'id': 1,
       'name': 'Steve',
       'description': 'El personaje principal de Minecraft.',
       'type':'bueno',
       'characteristic':'humano aventurero'
   },
   2: {
       'id': 2,
       'name': 'Alex',
       'description': 'Una alternativa femenina al personaje principal.',
       'type':'bueno',
       'characteristic':'humano aventurero'
   },
   3: {
       'id': 3,
       'name': 'Creeper',
       'description': 'Una criatura explosiva y temida en Minecraft.',
       'type':'malvado',
       'characteristic':'monstruo que explota'
   },
   4: {
       'id': 4,
       'name': 'Zombie',
       'description': 'Uno de los enemigos comunes en Minecraft.',
       'type':'malvado',
       'characteristic':'hambriento de sangre'
   }
}


# Función para generar el próximo ID disponible
def get_next_id():
   return max(characters.keys()) + 1 if characters else 1


# Rutas de la API
@app.route('/characters', methods=['GET'])
def get_characters():
   conn = connect_to_database()
   cursor = conn.cursor()


   cursor.execute("SELECT * FROM personajes")
   data = cursor.fetchall()


   cursor.close()
   conn.close()


   characters = []
   for row in data:
       character = {
           'id': row[0],
           'name': row[1],
           'description': row[2],
           'type': row[3],
           'characteristic': row[4]
       }
       characters.append(character)


   return jsonify(characters)


@app.route('/characters/<string:name_or_id>', methods=['GET'])
def get_character(name_or_id):
   conn = connect_to_database()
   cursor = conn.cursor()


   if name_or_id.isdigit():
       cursor.execute("SELECT * FROM personajes WHERE id = %s", (int(name_or_id),))
   else:
       cursor.execute("SELECT * FROM personajes WHERE lower(name) = lower(%s)", (name_or_id,))


   character = cursor.fetchone()


   cursor.close()
   conn.close()


   if character:
       character_dict = {
           'id': character[0],
           'name': character[1],
           'description': character[2],
           'type': character[3],
           'characteristic': character[4]
       }
       return jsonify(character_dict)
   else:
       return jsonify({'error': 'Personaje no encontrado'}), 404
@app.route('/characters/<string:name>', methods=['GET'])
def get_character_by_name(name):
   conn = connect_to_database()
   cursor = conn.cursor()


   cursor.execute("SELECT * FROM personajes WHERE lower(name) = lower(%s)", (name,))


   character = cursor.fetchone()


   cursor.close()
   conn.close()


   if character:
       character_dict = {
           'id': character[0],
           'name': character[1],
           'description': character[2],
           'type': character[3],
           'characteristic': character[4]
       }
       return jsonify(character_dict)
   else:
       return jsonify({'error': 'Personaje no encontrado'}), 404




@app.route('/characters/<string:name_or_id>', methods=['PUT'])
def update_character(name_or_id):
   update_data = request.json


   try:
       conn = connect_to_database()
       cursor = conn.cursor()


       if name_or_id.isdigit():
           cursor.execute("SELECT * FROM personajes WHERE id = %s", (int(name_or_id),))
       else:
           cursor.execute("SELECT * FROM personajes WHERE lower(name) = lower(%s)", (name_or_id,))


       character = cursor.fetchone()


       if character:
           # Actualizar los campos individuales si están presentes en los datos enviados
           if 'name' in update_data:
               update_name = update_data['name']
               cursor.execute("UPDATE personajes SET name = %s WHERE id = %s", (update_name, character[0]))


           if 'description' in update_data:
               update_description = update_data['description']
               cursor.execute("UPDATE personajes SET description = %s WHERE id = %s", (update_description, character[0]))


           if 'type' in update_data:
               update_type = update_data['type']
               cursor.execute("UPDATE personajes SET type = %s WHERE id = %s", (update_type, character[0]))


           if 'characteristic' in update_data:
               update_characteristic = update_data['characteristic']
               cursor.execute("UPDATE personajes SET characteristic = %s WHERE id = %s", (update_characteristic, character[0]))


           conn.commit()


           cursor.close()
           conn.close()


           updated_character = {
               'id': character[0],
               'name': update_data.get('name', character[1]),
               'description': update_data.get('description', character[2]),
               'type': update_data.get('type', character[3]),
               'characteristic': update_data.get('characteristic', character[4])
           }
           return jsonify(updated_character), 200
       else:
           return jsonify({'error': 'Personaje no encontrado'}), 404
   except Exception as e:
       return jsonify({'error': str(e)}), 500




@app.route('/characters/<string:name_or_id>', methods=['DELETE'])
def delete_character(name_or_id):
   conn = connect_to_database()
   cursor = conn.cursor()


   if name_or_id.isdigit():
       character_id = int(name_or_id)
       cursor.execute("SELECT * FROM personajes WHERE id = %s", (character_id,))
   else:
       cursor.execute("SELECT * FROM personajes WHERE lower(name) = lower(%s)", (name_or_id,))


   character = cursor.fetchone()


   if character:
       cursor.execute("DELETE FROM personajes WHERE id = %s", (character[0],))
       conn.commit()


       cursor.close()
       conn.close()


       deleted_character = {
           'id': character[0],
           'name': character[1],
           'description': character[2],
           'type': character[3],
           'characteristic': character[4]
       }
       return jsonify(deleted_character), 200
   else:
       return jsonify({'error': 'Personaje no encontrado'}), 404


@app.route('/characters', methods=['POST'])
def create_character():
   new_character_data = request.json


   try:
       conn = connect_to_database()
       cursor = conn.cursor()


       # Verificar si se proporcionan los datos necesarios para crear un personaje
       required_fields = ['name', 'description', 'type', 'characteristic']
       if not all(field in new_character_data for field in required_fields):
           return jsonify({'error': 'Datos incompletos para crear un personaje'}), 400


       cursor.execute("INSERT INTO personajes (name, description, type, characteristic) VALUES (%s, %s, %s, %s) RETURNING id",
                      (new_character_data['name'], new_character_data['description'], new_character_data['type'], new_character_data['characteristic']))
       new_character_id = cursor.fetchone()[0]  # Capturando el ID recién insertado
       conn.commit()


       cursor.close()
       conn.close()


       created_character = {
           'id': new_character_id,  # Incluir el ID en la respuesta
           'name': new_character_data['name'],
           'description': new_character_data['description'],
           'type': new_character_data['type'],
           'characteristic': new_character_data['characteristic']
       }
       return jsonify(created_character), 201  # Código 201 para indicar que se ha creado el recurso
   except Exception as e:
       return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
   app.run(port=5000)

