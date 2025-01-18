import genanki
import os
import csv
import utils
import requests
import py_ankiconnect
import psutil

def create_anki_deck_from_csv(csv_file_path, deck_name="My Deck", output_file="output.apkg"):
    """
    Reads a two-column CSV file and creates an Anki deck, where
    the first column is the front side of the card, and the second column is the back side.

    :param csv_file_path: Full path to the CSV file.
    :param deck_name: Name of the deck to be created.
    :param output_file: Name of the output .apkg file to be generated.
    """

    # Create a deck with a random (unique) deck_id
    # deck_id is just an integer that Anki uses internally to identify the deck,
    # so we'll use a random or arbitrary number here
    deck_id = 1234567890

    # Initialize a genanki deck
    my_deck = genanki.Deck(
        deck_id=deck_id,
        name=deck_name
    )

    # Create a basic model (front / back)
    # This defines how cards will be rendered in Anki.
    # You can customize styling or fields as needed.
    my_model = genanki.Model(
        model_id=1607392319,
        name='Simple Model',
        fields=[
            {'name': 'Front'},
            {'name': 'Back'}
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Front}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
            },
        ]
    )

    # Read the CSV file
    with open(csv_file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)

        for row in reader:
            # Each row is expected to have two columns
            if len(row) < 2:
                continue

            front_text = row[0].strip()
            back_text = row[1].strip()

            note = genanki.Note(
                model=my_model,
                fields=[front_text, back_text]
            )

            # Add the note to the deck
            my_deck.add_note(note)

    # Create a Package and write to file
    my_package = genanki.Package(my_deck)
    # Optionally include media files if needed
    # my_package.media_files = []
    my_package.write_to_file(output_file)

    print(f"Deck '{deck_name}' created and saved as '{output_file}'.")

def delete_imported_decks():
    response = requests.post('http://localhost:8765', json={
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": "tag:imported_by_script"
        }
    })

    if response.status_code == 200:
        result = response.json()
        if result.get('error') is None:
            note_ids = result['result']
            #print(f"delete_imported_decks: note_ids = {note_ids}")

            if note_ids:
                response = requests.post('http://localhost:8765', json={
                    "action": "notesInfo",
                    "version": 6,
                    "params": {
                        "notes": note_ids
                    }
                })

                if response.status_code == 200:
                    result = response.json()
                    #print(f"notesInfo response: {result}")  # Print the response for debugging

                    if result.get('error') is None:
                        # Extract card IDs from the notesInfo response
                        card_ids = [card_id for note in result['result'] for card_id in note['cards']]
                        #print(f"Card IDs: {card_ids}")

                        # Get deck names using the card IDs
                        response = requests.post('http://localhost:8765', json={
                            "action": "cardsInfo",
                            "version": 6,
                            "params": {
                                "cards": card_ids
                            }
                        })

                        if response.status_code == 200:
                            result = response.json()
                            #print(f"cardsInfo response: {result}")  # Print the response for debugging

                            if result.get('error') is None:
                                deck_names = {card['deckName'] for card in result['result']}
                                #print(f"Deck names: {deck_names}")

                                num_of_decks = len(deck_names)
                                for deck_index, deck_name in enumerate(deck_names):
                                    response = requests.post('http://localhost:8765', json={
                                        "action": "deleteDecks",
                                        "version": 6,
                                        "params": {
                                            "decks": [deck_name],
                                            "cardsToo": True
                                        }
                                    })

                                    if response.status_code == 200:
                                        result = response.json()
                                        if result.get('error') is None:
                                            print(f"Successfully deleted deck {deck_name}. Deck {deck_index+1} out of {num_of_decks}")
                                        else:
                                            print(f"Error deleting deck {deck_name}: {result['error']}")
                                    else:
                                        print(f"Failed to connect to AnkiConnect for deleting deck {deck_name}")
                            else:
                                print(f"Error retrieving cards info: {result['error']}")
                        else:
                            print(f"Failed to connect to AnkiConnect for retrieving cards info")
                    else:
                        print(f"Error retrieving notes info: {result['error']}")
                else:
                    print(f"Failed to connect to AnkiConnect for retrieving notes info")
            else:
                print("No cards found with the tag 'imported_by_script'")
        else:
            print(f"Error finding notes: {result['error']}")
    else:
        print(f"Failed to connect to AnkiConnect for finding notes")
    print('\n')

def import_apkg_files(folder_path):
    folder_path = os.path.abspath(folder_path)
    decks_list = os.listdir(folder_path)
    num_of_decks = len(decks_list)

    for index, file in enumerate(decks_list):
        if file.endswith('.apkg'):
            file_path = os.path.join(folder_path, file)

            response = requests.post('http://localhost:8765', json={
                "action": "importPackage",
                "version": 6,
                "params": {
                    "path": file_path
                }
            })

            if response.status_code == 200:
                result = response.json()
                if result.get('error') is None:
                    deck_name = os.path.splitext(file)[0]
                    deck_name_with_extension = deck_name + '.apkg'

                    response = requests.post('http://localhost:8765', json={
                        "action": "findNotes",
                        "version": 6,
                        "params": {
                            "query": f"deck:{deck_name_with_extension}"
                        }
                    })

                    #print(response.text)  # Print the response text for debugging

                    if response.status_code == 200:
                        result = response.json()
                        if result.get('error') is None:
                            note_ids = result['result']
                            #print(f"import_apkg_files: note_ids = {note_ids}")

                            if note_ids:
                                response = requests.post('http://localhost:8765', json={
                                    "action": "addTags",
                                    "version": 6,
                                    "params": {
                                        "notes": note_ids,
                                        "tags": "imported_by_script"
                                    }
                                })

                                if response.status_code == 200:
                                    tag_result = response.json()
                                    if tag_result.get('error') is None:
                                        print(f"Successfully tagged notes in deck {deck_name} (deck {index+1} out of {num_of_decks})")
                                    else:
                                        print(f"Error tagging notes in {deck_name}: {tag_result['error']}")
                                else:
                                    print(f"Failed to connect to AnkiConnect for tagging notes in {deck_name}")
                            else:
                                print(f"No notes found in deck {deck_name}")
                        else:
                            print(f"Error finding notes in {deck_name}: {result['error']}")
                    else:
                        print(f"Failed to connect to AnkiConnect for finding notes in {deck_name}")
                else:
                    print(f"Error importing {file_path}: {result['error']}")
            else:
                print(f"Failed to connect to AnkiConnect for {file_path}")
    print('\n')


def is_anki_running():
    """
    Checks if Anki is running by looking at the list of active processes.
    Returns True if Anki is found, False otherwise.
    """
    # The exact name may vary by OS (e.g., "anki.exe" on Windows).
    possible_names = ["anki", "anki.exe"]

    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in possible_names:
            return True

    return False

def main():
    current_folder = os.getcwd()
    csv_file_name = 'cards.csv'
    decks_folder_name = 'anki_decks'

    csv_full_path = os.path.join(current_folder, csv_file_name)
    decks_folder_full_path = os.path.join(current_folder, decks_folder_name)

    utils.create_empty_folder(decks_folder_full_path)


    deck_extension = 'apkg'

    deck_name = 'cpr3'
    deck_name_with_extension = deck_name + '.' + deck_extension
    output_deck_file_full_path = os.path.join(decks_folder_full_path, deck_name_with_extension)

    create_anki_deck_from_csv(csv_full_path, deck_name=deck_name, output_file=output_deck_file_full_path)

    if is_anki_running():
        delete_imported_decks()
        import_apkg_files(decks_folder_full_path)
        anki = py_ankiconnect.PyAnkiconnect()
        anki("sync")
        print('Successfully synchronized Anki')
        print('Finished running the code. You may use Anki now')
    else:
        print("Anki is not running.")



main()
