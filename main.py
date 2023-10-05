import random
import mysql.connector

mydb = mysql.connector.connect(
    host= , # your host
    user= , # your username
    passwd= , # your db password
    database= # your db name
)

mycursor = mydb.cursor()

# list of all characters that can be used to create the password
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?<>:()/!\%*$£€+=&|-_^@"

while 1:
    password_length = int(input('Quelle taille voulez-vous que votre mot de passe fasse ? : '))
    password = ""

    for char in range(0, password_length):
        password_char = random.choice(chars)
        password += password_char

    print('Voilà votre mot de passe ! :', password)

    add_to_bdd = str(input('Voulez-vous ajouter ce mdp à votre bdd ? (o: oui, n: non): '))

    if add_to_bdd == 'o':
        username = str(input('Quel est le nom d\'utilisateur associé à ce mdp ? : '))
        location = str(input('A quoi correspondent ce mdp et ce username ? : '))

        # query to insert the values into the db
        sql = 'insert into passwords (password, username, location) values (%s, %s, %s)'
        vals = (password, username, location)
        mycursor.execute(sql, vals)

        mydb.commit()
        print(mycursor.rowcount, " identifiant ajouté")

