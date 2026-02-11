import requests
import os
import re

# The list of songs you provided
songs_playlist = [
    "Patience - Guns N' Roses",
    "Fast Car - Tracy Chapman",
    "Ordinary World - Duran Duran",
    "Baby One More Time - Travis",
    "Sunday Bloody Sunday - U2",
    "To Be With You - Mr. Big",
    "Crazy - Seal",
    "Still the One - Shania Twain",
    "Drive - Incubus",
    "Englishman in New York - Sting",
    "Alright - Supergrass",
    "High and Dry - Radiohead",
    "Somewhere Only We Know - Keane",
    "One - U2"
]

more_songs = [
    "Nirvana - Nevermind",
    "Metallica - Metallica (The Black Album)",
    "Pearl Jam - Ten",
    "Soundgarden - Superunknown",
    "Alice in Chains - Dirt",
    "Stone Temple Pilots - Core",
    "Radiohead - OK Computer",
    "Green Day - Dookie",
    "The Smashing Pumpkins - Mellon Collie and the Infinite Sadness",
    "My Bloody Valentine - Loveless",
    "Nine Inch Nails - The Downward Spiral",
    "Rage Against the Machine - Rage Against the Machine",
    "Hole - Live Through This",
    "Red Hot Chili Peppers - Blood Sugar Sex Magik",
    "Temple of the Dog - Temple of the Dog",
    "Pantera - Vulgar Display of Power",
    "Tool - Ænima",
    "Björk - Post",
    "Massive Attack - Mezzanine",
    "The Notorious B.I.G. - Ready to Die",
    "Dr. Dre - The Chronic",
    "Wu-Tang Clan - Enter the Wu-Tang (36 Chambers)",
    "Nas - Illmatic",
    "A Tribe Called Quest - The Low End Theory",
    "Daft Punk - Homework",
    "The Prodigy - The Fat of the Land",
    "Oasis - (What's the Story) Morning Glory?",
    "Blur - Parklife",
    "Pulp - Different Class",
    "The Verve - Urban Hymns",
    "Beastie Boys - Check Your Head",
    "Beck - Odelay",
    "Lauryn Hill - The Miseducation of Lauryn Hill",
    "Alanis Morissette - Jagged Little Pill",
    "No Doubt - Tragic Kingdom",
    "Foo Fighters - The Colour and the Shape",
    "Jane's Addiction - Ritual de lo Habitual",
    "Sonic Youth - Goo",
    "Pavement - Crooked Rain, Crooked Rain",
    "Neutral Milk Hotel - In the Aeroplane Over the Sea",
    "Marilyn Manson - Antichrist Superstar",
    "Korn - Korn",
    "Deftones - Around the Fur",
    "Faith No More - Angel Dust",
    "L7 - Bricks Are Heavy",
    "Mudhoney - Every Good Boy Deserves Fudge",
    "Screaming Trees - Sweet Oblivion",
    "Silverchair - Frogstomp",
    "Bush - Sixteen Stone",
    "Live - Throwing Copper"
]

def download_album_art(song_list):
    if not os.path.exists('album_covers'):
        os.makedirs('album_covers')

    for query in song_list:
        print(f"Searching for: {query}...")
        
        # iTunes Search API URL
        url = "https://itunes.apple.com/search"
        params = {
            "term": query,
            "limit": 1,
            "media": "music",
            "entity": "song"
        }

        try:
            response = requests.get(url, params=params).json()
            
            if response['resultCount'] > 0:
                result = response['results'][0]
                # Get the 100x100 URL and swap it for 1000x1000 for high resolution
                img_url = result['artworkUrl100'].replace('100x100bb', '1000x1000bb')
                
                # Sanitize filename
                filename = re.sub(r'[\\/*?:"<>|]', "", query) + ".jpg"
                img_data = requests.get(img_url).content
                
                with open(f"album_covers/{filename}", 'wb') as handler:
                    handler.write(img_data)
                print(f"  Success: Saved to album_covers/{filename}")
            else:
                print(f"  Failed: No results found for {query}")
                
        except Exception as e:
            print(f"  Error searching for {query}: {e}")

if __name__ == "__main__":
    #download_album_art(songs_playlist) - Peer and Roey playlist
    download_album_art(more_songs)  # Additional songs playlist