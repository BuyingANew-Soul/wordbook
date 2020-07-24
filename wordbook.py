"""
:Simple word dictionary. All resources will be created by user.
:Using sqlite for storing the data
:User can add words with their meaning and example
:Later user will be able to practise
"""
import sqlite3
import random
import os


class Word:

    """
    :this class is the basic structure for the words.
    """
    def __init__(self, word, meaning, example1, example2, syn, ant):
        self.word = word
        self.meaning = meaning
        self.example1 = example1
        self.example2 = example2
        self.syn = syn
        self.ant = ant

    def show_current_word(self):
        print("word: {}\nmeaning: {}\nexample -> {}\n        -> {}\nsyn : {}\nant : {}".format(self.word,
                                                                                               self.meaning,
                                                                                               self.example1,
                                                                                               self.example2,
                                                                                               self.syn,
                                                                                               self.ant))

    def __repr__(self):
        return "..Word object.. this word is : {}".format(self.word)

    def __str__(self):
        return "{}\n{}".format(self.word, self.meaning)


def add_new_word(connector, cursor):
    """
    :param connector: db connector
    :param cursor: db connector's cursor for executing queries
    :return: takes values from user and saves them to the db
    """

    while True:
        os.system('cls')
        word = input("The word is : ").lower()
        meaning = input("Meaning : ")
        exm1 = input("Give a example: ")
        exm2 = input("Please give another one: ")
        syn = input("Synonyms : ")
        ant = input("Antonyms : ")

        new_word = Word(word, meaning, exm1, exm2, syn, ant)
        print("You have just added the following word to the database: ")
        new_word.show_current_word()   # this method is in the word Class. not showing the word from db

        adding_word_in_db(connector, cursor, new_word)   # here I'm adding the word to the db using this function

        more = input("Do you want to add more word?")
        if more == "n" or more == "no":
            break
        elif more == "y" or more == "yes":
            continue


def adding_word_in_db(connector, cursor, word):
    """
    :param connector: db connector
    :param cursor: db cursor for running queries
    :param word: word from add_new_word function, where user inputted the word related data
    :return: adds the words to db
    """

    with connector:
        cursor.execute('''CREATE TABLE IF NOT EXISTS words
                         (id integer primary key autoincrement, 
                          word text, 
                          meaning text, 
                          exm1 text, 
                          exm2 text, 
                          syn text, 
                          ant text)''')

    with connector:
        cursor.execute("INSERT INTO words VALUES" 
                       "(?,?,?,?,?,?,?)",
                       (None,
                        word.word,
                        word.meaning,
                        word.example1,
                        word.example2,
                        word.syn,
                        word.ant))


def show_word(con, cur, word_id):
    """
    :param con: db connector
    :param cur: db cursor for running queries
    :param word_id: taking word id to show the word
    :return: printing out the word with related info
    """

    with con:
        cur.execute("SELECT * FROM words WHERE id= ?", (word_id,))
        list_row = cur.fetchall()   # fetchall() returns a list of tuples
        tup = list_row[0]           # as the list is containing one tuple only, taking the tuple out of the list
    print("\nword : {}\nmeaning : {}\n\nexample : \n{}\n{}\n\nsynonym : {}\nantonym : {}\n"
          .format(tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))      # leaving the 0'th index as it contains id


def delete_word(connector, cursor):
    """
    :param connector: db connector
    :param cursor: db cursor for running queries
    :return: deletes a word from db
    """

    del_word = input("Type in the word you want to delete: ").lower()
    with connector:
        cursor.execute("SELECT word FROM words WHERE word = ?", (del_word,))
        if cursor.fetchone() is None:
            print("The word \'{}\' is not in the wordbook!".format(del_word))
        else:
            cursor.execute("DELETE FROM words WHERE word = ?", (del_word,))
            print("The word \'{}\' has been deleted".format(del_word))


def find_word(connector, cursor):
    """
    :param connector: db connector
    :param cursor: db cursor for running queries
    :return: finds a word in the database
    """

    while True:
        find = input("Type in the word fo find: ").lower()
        with connector:
            cursor.execute("SELECT word FROM words WHERE word = ?", (find,))
            if cursor.fetchone() is None:       # fetchone() return a None if there is no value
                print("\nThe word \'{}\' is not in the wordbook!".format(find))
            else:
                cursor.execute("SELECT id FROM words WHERE word = ?", (find,))
                id_word = cursor.fetchone()
                show_word(connector, cursor, id_word[0])

        more = input("Need to find more?").lower()
        if more == "y" or more == "yes":
            continue
        elif more == "n" or more == "no":
            os.system('cls')
            break


def word_count(con, cur):
    """
    :param con: db connector
    :param cur: db cursor
    :return: returns total number of words in the db
    """

    with con:
        cur.execute("SELECT COUNT(*) FROM words")
        count = cur.fetchone()
        return count[0]


def practise(connector, cursor):
    """
    :param connector: db connector
    :param cursor: db cursor for running queries
    :return: gives the user words randomly to check if he/she can remember, else shows hints, else shows everything
             about the word
    """

    print("\n***Type 'exit' whenever you want to exit practicing***\n")
    while True:
        os.system('cls')

        with connector:
            c.execute("SELECT id FROM words")           # selecting all id's from the db
            all_id = c.fetchall()                       # this returns a list of tuples containing ids
            random_id = random.choice(all_id)           # randomly selecting one tuple from the list
            word_id = random_id[0]                      # unpacking the tuple
            cursor.execute("SELECT word FROM words WHERE id= ?", (word_id,))
            word = cursor.fetchone()
            print("Try this one: ")
            print(10 * " ", end="")
            print(word[0])
            print("\n")
            print("\nPress 1 : I got this one, move on..")
            print("Press 2 : Not sure, give me an example")
            print("Press 3 : Show me the meaning and uses\n")

            while True:
                choice = input()
                if choice == "1":
                    break
                elif choice == "2":
                    print(10 * " ", end="")
                    cursor.execute("SELECT exm1 FROM words WHERE id= ?", (word_id,))
                    hint = cursor.fetchone()
                    print(hint[0])

                    now = input("\nHave you got this now? yes = y or no = n \n")
                    if now == "y" or now == "yes":
                        break
                    elif now == "n" or now == "no":
                        show_word(connector, cursor, word_id)
                        break
                    else:
                        continue
                elif choice == "3":
                    print(10 * " ", end="")
                    show_word(connector, cursor, word_id)
                    break
                elif choice == 'exit':
                    break
                else:
                    print("\nPlease choose from any option pressing 1,2 or 3")
                    continue

        print("\nPress enter to continue practicing..")
        print("Type 'exit' or 'e' to exit practicing")
        more = input()
        if more.lower() == "exit" or more.lower() == 'e':
            os.system('cls')
            break
        else:
            os.system('cls')
            continue


def check_duplicate():
    pass


if __name__ == '__main__':
    os.system('cls')
    print(10 * " ", end="")
    print(10 * "#")
    print(10 * " ", end="")
    print(" WordBook")
    print(10 * " ", end="")
    print(10 * "#")

    conn = sqlite3.connect("wordbook.db")
    c = conn.cursor()

    total_words = word_count(conn, c)
    print("\nThere are {} words in your vocabulary!\n".format(total_words))

    while True:
        option = input("##Press 1, to Add new word\n"
                       "##Press 2, for Practice\n"
                       "##Press 3 for Delete a word\n"
                       "##Press 4 for Find a word\n"
                       "(e for exit) ")

        if option == "1":
            add_new_word(conn, c)
            os.system('cls')
        elif option == "2":
            practise(conn, c)
            os.system('cls')
        elif option == "3":
            delete_word(conn, c)

        elif option == "4":
            os.system('cls')
            find_word(conn, c)

        elif option == "e":
            break

    c.close()
