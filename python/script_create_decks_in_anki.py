import genanki
import os
import csv

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

def main():
    current_folder = os.getcwd()
    csv_file_name = 'cards.csv'
    csv_full_path = os.path.join(current_folder, csv_file_name)
    create_anki_deck_from_csv(csv_full_path, deck_name="Vocabulary Deck", output_file="vocab.apkg")


main()
