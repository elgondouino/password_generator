import random
import mysql.connector
from cryptography.fernet import Fernet

mydb = mysql.connector.connect(
    host='your_host',
    user='your_username',
    passwd='your_db_password',
    database='your_db_name'
)

mycursor = mydb.cursor()

crypter = Fernet('your_key')

# list of all characters that can be used to create the password
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?<>:()/!\%*$£€+=&|-_^@"

while 1:
    print("1. Générer un mot de passe aléatoire")
    print("2. Chercher un mot de passe")
    menu_choice = input("Que voulez-vous faire ? : ")

    if menu_choice == '1':
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
            bytes_pw = bytes(password, 'utf-8')
            crypted_password = crypter.encrypt(bytes_pw)
            sql = 'insert into passwords (password, username, location) values (%s, %s, %s)'
            vals = (crypted_password, username, location)
            mycursor.execute(sql, vals)

            mydb.commit()

            print(mycursor.rowcount, " identifiant ajouté")

    elif menu_choice == '2':
        location_choice = input("Quels identifiants cherchez-vous ? : ")
        sql = "select username, password from passwords where location = %s"
        mycursor.execute(sql, (location_choice,))

        result = mycursor.fetchone()
        print('Identifiant: ', result[0])
        print('Mot de passe: ', crypter.decrypt(result[1]).decode())