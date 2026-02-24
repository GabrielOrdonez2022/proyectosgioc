![Img minecraft](https://github.com/GabrielOrdonez2022/api-personajes-minecraft/assets/103681795/77d3968d-b0af-41c6-9876-0107b7f4c043)
# api-personajes-minecraft
Api de personajes de minecraft creada con python y uso de pgadmin 4

Pasos:
   
Instalar postgresql en linux mint
#Comandos de instalación de Postgresql y Pgadmin4

Sistema operativo:

![linux mint](https://github.com/GabrielOrdonez2022/api-personajes-minecraft/assets/103681795/b0904707-de2d-4dbc-b027-45f2b47bc0e0)

![Postgresql y pgadmin4](https://github.com/GabrielOrdonez2022/api-personajes-minecraft/assets/103681795/d174927f-ca6e-4e20-b0f5-51fb3e9d3726)


1)sudo apt-get update
2)sudo apt install postgresql postgresql-contrib
3)sudo su - postgres
4)psql
5)create user gabriel with password '1234';
6)create database personajesminecraft with owner gabriel;
7)alter user gabriel with superuser;
8)poner “exit” para salir (x2 veces)
Instalación de pgadmin
1)sudo curl https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo apt-key add
2)sudo sh -c '. /etc/upstream-release/lsb-release && echo "deb https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$DISTRIB_CODENAME pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
3)sudo apt install PgAdmin4
------------------------------------------------------------------------------------------------------------------------------------------------------
Dentro de PgAdmin4
1) Add New Server (Añadir nuevo servidor)
2) Ubicar de preferencia el mismo nombre de base de datos al servidor
3) Luego dirígete al segundo menú "Connection"
4) En Host name/address ubicar localhost
5) En username y password ubicar (el usuario y contraseña creados en la consola)
6) Guardamos (save)
   
Una vez creada la respectiva conexión en PgAdmin4
1) Visualizarás dentro del server la base de datos que se creó por medio de la consola
2) Una vez abierta la DB, dirígete a Schemas, luego a tables y crea una tabla llamada personajes
3) Dentro se deberá crear una tabla con los siguientes campos con su tipo de datos correspondiente, tal como la siguiente:
![Tipo de datos de campos de tabla personajes](https://github.com/GabrielOrdonez2022/api-personajes-minecraft/assets/103681795/15405868-dda6-4d87-b599-8a9065b7ce87)

Nota: Id siempre será clave primaria, y en este caso el tipo de dato es serial (para que me cree una secuencia y no tenga que escribirlo manualmente al utilizar el método post)
5) Luego de guardar la tabla, se creará una secuencia como:

![Secuencia creada automáticamente](https://github.com/GabrielOrdonez2022/api-personajes-minecraft/assets/103681795/e6c01718-2c4d-4cea-a76d-6b4d0d750f6a)

------------------------------------------------------------------------------------------------------------------------------------------------------
Descargar Postman del sitio web oficial

![Postman](https://github.com/GabrielOrdonez2022/api-personajes-minecraft/assets/103681795/e2f65a29-5b7d-4b1c-a214-3412ec190378)

https://www.postman.com/downloads/
 
1) Descomprimir el archivo
sudo tar -xzf postman-linux-x64.tar.gz -C /opt
2) sudo ln -s /opt/Postman/Postman /usr/bin/postman
3) sudo nano /usr/share/applications/postman.desktop
[Desktop Entry]
Type=Application
Name=Postman
Icon=/opt/Postman/app/resources/app/asserts/icon.png
Exec="/opt/Postman/Postman"
Comment=Postman Desktop App
Categories=Development;Code;
4) Buscar el acceso directo y ejecutar Postman	
------------------------------------------------------------------------------------------------------------------------------------------------------

Una vez instalado pgadmin4 y postman, realizar lo siguiente:
1) cd Documentos (de preferencia)
2) mkdir personajes-minecraft
3) cd personajes-minecraft
5) pip3 install virtualenv
6) virtualenv .
7) source bin/activate
8) pip install psycopg2-binary    → dentro del entorno virtual 
9) python3 -m pip install Flask   → dentro del entorno virtual 
10) Crear app.py dentro de la carpeta personajes-minecraft usando un IDE (por ejemplo: visual code)
11) Adjuntar código dentro de app.py
12) flask run
13) Abrir Postman y probar el URL https://127.0.0.1:5000/characters
  Y podremos hacer las siguientes consultas, con estos cuatro métodos (get, post, put y delete)

------------------------------------------------------------------------------------------------------------------------------------------------------
Método get:
  http://localhost:5000/characters -> para obtener todos los personajes (método get)
  http://localhost:5000/characters/10 -> para obtener personaje por su id (método get)
  http://localhost:5000/characters/Steve -> para obtener personaje por su id (método get)
------------------------------------------------------------------------------------------------------------------------------------------------------
Método post:
  http://localhost:5000/characters -> para crear personajes de minecraft (método post)
  Dentro de body/Raw debe ir los campos con su respectivo contenido a crear
  {
      "name": "Skeleton",
      "description": "Guerrero nato con espada",
      "type": "inmortal",
      "characteristic": "Demonio del inframundo revivido"
  }
  ------------------------------------------------------------------------------------------------------------------------------------------------------
Método put:
http://localhost:5000/characters/1 -> para actualizar buscando por id (método put)
Dentro de body/Raw debe ir los campos con su respectivo contenido a actualizar
  {
      "name": "Skeleton",
      "description": "Guerrero nato con espada",
      "type": "inmortal",
      "characteristic": "Demonio del inframundo revivido"
  }
http://localhost:5000/characters/Skeleton -> para actualizar buscando por nombre (método put)
Dentro de body/Raw debe ir los campos con su respectivo contenido a actualizar
  {
      "name": "Skeleton",
      "description": "Guerrero nato con espada",
      "type": "inmortal",
      "characteristic": "Demonio del inframundo revivido"
  }
 ------------------------------------------------------------------------------------------------------------------------------------------------------ 
  Método delete:
1. http://localhost:5000/characters/Skeleton -> eliminar buscando por nombre (método delete)
2. http://localhost:5000/characters/11 -> eliminar buscando por id (método delete)






