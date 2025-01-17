import csv
import pytube
import pytubefix
import genanki
import shutil
import os
import utils
import random
import requests
import py_ankiconnect

def download_single_youtube_playlist(playlist_index, num_of_playlists, playlist_url, main_output_folder, playlist_name):
    # Create output folder if it doesn't exist
    output_folder_full_path = os.path.join(main_output_folder, playlist_name)
    if not os.path.exists(output_folder_full_path):
        os.makedirs(output_folder_full_path)

    # Load the playlist
    playlist = pytube.Playlist(playlist_url)
    num_of_videos = len(playlist.video_urls)

    playlist_name = playlist.title

    for index, video_url in enumerate(playlist.video_urls):
        try:
            # Load the YouTube video
            yt = pytubefix.YouTube(video_url)

            # Get the highest resolution stream available
            stream = yt.streams.get_highest_resolution()
            #stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

            video_name =yt.title
            print(f'playlist name: {playlist_name}, playlist {playlist_index+1} out of {num_of_playlists}.  Downloading video {index+1} out of {num_of_videos}. video name: {video_name}')
            stream.download(output_folder_full_path)
        except Exception as e:
            print(f'Failed to download: {video_url}')
            print(f'Error: {e}\n')
    print('\n')

def download_youtube_playlists(main_output_folder):
    playlists = {
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4G-DgkNaMFyBhFuiAT0gsEW": "צבעים",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4HLu2OVH_8lDr0XShY6mV98": "מילות שאלה",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4EOm9GD2sqgNKtgbUKC0oER": "בריאות הגוף והנפש",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4F-0KUTh1sgufPjyz4uut40": "חינוך והשכלה",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4HP4oYNwjs6ZW_kAuJ-p1v5": "לפי מוצא",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4EQrfOOh0B_4jXnv90LojhR": "דמוגרפיה",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4G6Gm647PdUchKcz3VMtwZK": "מתמטיקה ומספרים",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4FlWGKjNP0-ySjX-XQ5TIAh": "ביטויים ומילים",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4GMh3Fw2tgNBceCkOYHLoSt": "כלכלה וכסף",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4GL_sdv5nn5MhhT0pw4ZmD1": "הגנה וטרור",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4ELOEnk5-258ZBf7QWjVjkb": "אירועי תרבות ופנאי",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4G5u5ulpwGa9V9hn565CcDS": "אתרים מוסדות וארגונים",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4HdqwJ6AL7EfwchzO4_sgRl": "תזונה",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4EbSJ0eEHXfiIEsbENj3Ng_": "שפה",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4ERscSE5gdrPmuVFev0l1Pd": "נכות",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4E1AuTXB_tjTS9fvZ4xu5Ge": "ארגוני רפואה ובריאות",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4EMLFVljn-BBEcAbXE0yVqG": "שושנת הרוחות",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4H4Yqa0-RsqvqALXqmPJJ_o": "דיגיטל",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4FYU4SNON3-R0ens9USDf32": "סוג חומר",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4HV-QNKxwomxQJPZtOTux4U": "ניירת וטפסים",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4Fjr51fprQBTeUyafNqpvqv": "קוסמטיקה",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4FjchU6cLuFMiDmwivecHoe": "מדע וטכנולוגיה",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4Hs-Uhm7UqAP7fyT_E9aTSd": "משקאות",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4GPHi8B3bAEOkfy3AcYxjFy": "מזג אוויר",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4ErKJNFsp6_DLAc8iSDylF3": "כלי תחבורה",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4EP7lMRJhLGHUCjWc5AzBMj": "מבנה דת וזרמים דתיים",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4HQ3kugvRQsoIjZq7XuzRu1": "טקסים יהודים ולבוש מסורתי",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4GUvNd0LMlRV5gh2N_cvAFz": "זיהום ומחלות והגיינה",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4GJ-yYsEyyHmabBIcwlAw8k": "אישיים מהתנך",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4H-_AlM0IuLnRfq0An_Bjcz": "ספורט",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4G0CPPTqQAbkHj8bLJK_Z2v": "משפחה ויחסים",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4EXUbOd0ggLBqD6tn_PfNbW": "כלים ומכשירים למזון",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4F0Cnnc5ziMLxwYniKLn5Tc": "שיטות ודרכי תקשורת",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4FaApIwnG8M0bIM94i6NGg0": "כלי עבודה",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4HYMEvQgKfL-EQctHc8aQJZ": "חלקי מבנה בית",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4ErAyrMR_5zUm2JHLgIVPa-": "בריאות",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4EfAKay4Piodpg1gaID91yd": "רפואה",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4EOmzPNcgIhe68b9XHVvy9Z": "מדעי הטבע ומדעים מדוייקים",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4FW-nq6o9ERdVt4aYytz_Lx": "דמויות",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4GrhVrC-1O4Dg6RnVdUOOYO": "תשתיות, דרכים וכבישים",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4EXTiYkiS8GrEyEloz3SvKE": "תחבורה",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4FhHnzp824Sb_za38HyMkvD": "אביזרי אופנה",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4GOjwqN12tMC31NT51zLtEH": "טבע וצורות נוף",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4Hvcq6rzYSLDETDw1PZKT9H": "אישיים",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4FcBw1JbQLii9E7JwXn6nYl": "מידות",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4HkEHkem4q2fG-D0yOCg0I0": "מצבים",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4EASrxXN1-PyOy6OH2Ek_v6": "אוכל",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4H7TWiABi_a4NDu_7y7CO-8": "מזון",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4FmEViS17O2M5-sLyaUhOOz": "ריהוט",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4F0az918H6peQC70PUXBUbv": "בית ועיצוב",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4HinxCS2fT08H9c4KfUUeRi": "בגדים",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4EDZI51NjVKIKM9bhaTwndJ": "אופנה ויופי",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4GPlr4S6orKGtVXRVEFSjqM": "תכונות חומר",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4HS8M3kOrUA38gjjSE2BXID": "תכונות",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4G5GQBmug1cxV-M3QqQFMt6": "תקשורת",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4HDTFhWev52Oahgy_iyurSG": "פטירה ואבל",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4EFmTnHa5TmEdbE6oD2i78t": "אמצעי וכלי כתיבה",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4GfxLoXiQxTe8o-gevl2dq3": "ציוד משרדי",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4FdsB1aCtUJbwffyueIFX4k": "כלים ומכשירים",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4E7HFgxFTV8NFHG9aMq0tDK": "תכונות אופי",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4EJtKRf98PaUrDMApml_5DA": "דת מסורת היסטוריה יהודית",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4ELXj7r5YMcpvvipS46xTOR": "ישובים וערים",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4EPeBeRS3Mzgc4tcF29xmyk": "ארצות",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4Erkdz4hu94xf5dA2DJQLkz": "גיאוגרפיה",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4EZWjhET00CGxLkOg4n7MSe": "מרחב",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4GbkxMpIj488GtXXgGIHVEL": "זמנים",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4ETmxeSuT-8-ZUn9r1AORE7": "גוף האדם",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4EsH_khRdo7vnsb_NOdaSzM": "צורות",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4Fw79q85RNoGBS0Ng3CK7Dd": "מוצרי בית ומוצרי חשמל ביתיים",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4HEHJFhEGAt-swJmMa_a7mz": "אנשי מקצוע וסוגי מקצועות",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4H6oHNZp51G_Z5DfVBghYhl": "חפצים וצעצועים",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4Ei76HlD_bf4A8zA3qAQ3qh": "פעלים",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4H9WZfleFUvcMoouH8Vc6EV": "בעלי חיים ומגוריהם",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4F6fTTh5132o197iOoQ_ucC": "שונות",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4EaP63thFhceT1fjBCRl57F": "חגים ומועדים",
        "https://www.youtube.com/playlist?list=PLCuW5EMQWQ4FR3FRBxSm1wtSagFXNtvbi": "כינויי גוף"
    }

    num_of_playlists = len(playlists)

    for playlist_index, (playlist_url, playlist_name) in enumerate(playlists.items()):
        download_single_youtube_playlist(playlist_index, num_of_playlists, playlist_url, main_output_folder, playlist_name)

    print('Download playlists from youtube completed!')
def remove_whitespaces(folder_path):
    # Iterate over all items in the given folder path
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # Check if the item is a directory
        if os.path.isdir(item_path):
            # Replace whitespaces with underscores in the directory name
            new_item_name = item.replace(' ', '_')
            new_item_path = os.path.join(folder_path, new_item_name)

            # Rename the directory if the name has changed
            if new_item_name != item:
                os.rename(item_path, new_item_path)

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


def create_decks_in_anki(folder_path, decks_folder_full_path):
    utils.create_empty_folder(decks_folder_full_path)

    print("Creating decks in anki. Please wait...\n")
    for subfolder_name in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder_name)
        package_name = subfolder_name + ".apkg"

        deck_name = package_name
        deck_id = random.randint(1, 2**63 - 1)  # Generate a unique identifier within the valid range

        # Create a new Anki deck
        deck = genanki.Deck(deck_id, deck_name)

        for video_file in os.listdir(subfolder_path):
            if video_file.endswith(('.mp4', '.mov', '.avi')):
                video_name = os.path.splitext(video_file)[0]
                video_path = f"[sound:{video_file}]"

                # Create a card with the video name on the front and video on the back
                note = genanki.Note(
                    model=genanki.Model(
                        1607392319,
                        'Simple Model',
                        fields=[
                            {'name': 'Front'},
                            {'name': 'Back'},
                        ],
                        templates=[
                            {
                                'name': 'Card 1',
                                'qfmt': '{{Front}}',
                                'afmt': '{{FrontSide}}<br>{{Back}}',
                            },
                        ]),
                    fields=[video_name, video_path]
                )

                deck.add_note(note)

        # Generate the Anki package
        package = genanki.Package(deck)
        package.media_files = [os.path.join(subfolder_path, f) for f in os.listdir(subfolder_path)]
        pack_file_full_path = os.path.join(decks_folder_full_path, package_name)
        package.write_to_file(pack_file_full_path)

    print("Anki decks created successfully\n")


def split_videos_in_subfolders(folder_path, max_num_of_files_in_folders):
    # Iterate through all subfolders in the given folder path
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)

        if os.path.isdir(subfolder_path):
            # Get all mp4 files in the subfolder
            videos_files = sorted([f for f in os.listdir(subfolder_path) if f.endswith('.mp4')])
            num_of_total_files = len(videos_files)

            if num_of_total_files <= max_num_of_files_in_folders:
                continue

            if num_of_total_files > 0:
                # Calculate the number of new folders needed
                num_folders = (num_of_total_files + max_num_of_files_in_folders - 1) // max_num_of_files_in_folders

                # Create new subfolders and move files
                for i in range(num_folders):
                    #new_subfolder_name = f"{subfolder}_עד_{max_num_of_files_in_folders}_מילים_{i + 1:04d}"
                    new_subfolder_name = f"{subfolder}_{i + 1:04d}"
                    new_subfolder_path = os.path.join(folder_path, new_subfolder_name)
                    os.makedirs(new_subfolder_path, exist_ok=True)

                    # Determine the range of files for this new subfolder
                    start_index = i * max_num_of_files_in_folders
                    end_index = min(start_index + max_num_of_files_in_folders, num_of_total_files)

                    for j in range(start_index, end_index):
                        file_to_move = videos_files[j]
                        os.rename(os.path.join(subfolder_path, file_to_move),
                                  os.path.join(new_subfolder_path, file_to_move))
            os.rmdir(subfolder_path)

def shorten_video_names(folder_path, video_extension):
    # Define the suffix to look for
    suffix = " בשפת הסימנים הישראלית - מילון שפת הסימנים הישראלית"

    # Walk through all subfolders and files in the given folder
    for dirpath, _, filenames in os.walk(folder_path):
        filenames.sort()  # Sort filenames alphabetically
        for filename in filenames:
            if filename.endswith(video_extension):
                filename_no_extension = filename

                # Remove the suffix if present
                if filename.endswith(suffix + video_extension):
                    filename_no_extension = filename[:-len(suffix) - 4]
                else:
                    filename_no_extension = filename[:-4]

                # Remove the leading underscore if present
                if filename_no_extension.startswith('_'):
                    filename_no_extension = filename_no_extension[1:]

                filename_no_extension = filename_no_extension.strip()

                new_filename = filename_no_extension + video_extension

                # Only rename if the new filename is different
                if new_filename != filename:
                    # Construct the full file paths
                    old_file_path = os.path.join(dirpath, filename)
                    new_file_path = os.path.join(dirpath, new_filename)

                    # Rename the file
                    os.rename(old_file_path, new_file_path)
                    #print(f'Renamed: "{filename}" to "{new_filename}"')


def remove_duplicate_names(folder_path):
    seen_files = set()
    for root, _, files in os.walk(folder_path):
        files.sort()  # Sort files alphabetically
        for file in files:
            file_path = os.path.join(root, file)
            if file in seen_files:
                os.remove(file_path)
                print(f"Deleted duplicate file: {file_path}")
            else:
                seen_files.add(file)

def delete_empty_folders(folder_full_path):
    """Delete all empty sub-folders in the given folder."""
    for subfolder_name in os.listdir(folder_full_path):
        subfolder_full_path = os.path.join(folder_full_path, subfolder_name)
        if os.path.isdir(subfolder_full_path) and not os.listdir(subfolder_full_path):
            os.rmdir(subfolder_full_path)

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
