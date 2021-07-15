# DiscordScraper
WORK IN PROGRESS

goto the following website and create a bot application. 
    You need to copy the token and user id

    1. visit : https://discord.com/developers/applications

    2. Click "create New Application", name it

    3. on the left side, click "bot" and then click "build a bot"

    4. Click "click to reveal your token "

    5. copy that token to the config.cfg file

    6. Permissions : 74752 is a reasonable default 
        but you can choose "8" for full control
        if you want to hack this bot to make more stuff
        Set that in the config.cfg file

# How to install this program:

    1. Open a terminal in home directory

    2. run the command `curl --location --remote-header-name --remote-name https://github.com/Church-of-the-SubHackers/DiscordScraper`

    3. run the command `sudo chmod +x ./DiscordScraper/setup.py`

# Ways to run this program:

    1. open `~/DiscordScraper/config.cfg` in a text editor and 
        set options according to your preferences

    AND
       run the command `~/DiscordScraper/app.py` 
    OR

    2. run the command `~/DiscordScraper/app.py --token <insert_your_token_here> --AllTheOtherOptionsYouFeellLikeSetting`

    3. ???

    4. PROFIT!

READ THE SOURCE TO LEARN SOMETHING

    Discord Message Archival
    
    --imagestoretype'
        default = "file"
        help    = "set if images are saved in the DB as text or externally as files
        OPTIONS: 'file' OR 'base64'
    
    --messagelimit
        default = "10000"
        help    = "Number of messages to download"
    
    --databasename
        default = "discordmessagehistory"
        help    = "Name of the file to save the database as"
    
    --imagesaveformat'
        default = ".png"
        help    = File extension for images

    --token
        default = discord_bot_token
        help    = "string, no quotes, of your discord bot token.
            No, this script is not going to steal it, Read the source"
    
    --gzipped
        default = True
        help    = "will gzip as much as possible to save space"
    
    --docs
        default = True
        help    = "Prints the Documentation to the terminal
            use './app.py --docs >> docs.txt' to save to a file

File Structure of the Module is the following:
    
    
    /module/
    │   ├──setup.py
    │   ├──app.py
    │   ├──config.cfg
    │   │   --- IF SAVING AS SQLITE3DB ---
    │   ├──DATABASE.DB 
    │   ├── /src
    │   │   │ --- these are the program files ---
    │   │   │ --- dont mess with these --- 
    │   │   ├── __init__.py
    │   │   ├── src1.py
    │   │   ├── src2.py
    │   │   └── src....py
    │   └── /database
            └── /images
                ├── /channel1
                │   └── /date-time
                │       ├── img1-date-time.jpg.b64
                │       ├── img2-date-time.jpg.b64
                │       └── img3-date-time.jpg.b64
                ├── /channel2
                │  └──/date-time
                │       ├── img1-date-time.jpg.b64
                │       ├── img2-date-time.jpg.b64
                │       └── img3-date-time.jpg.b64
                └── /channel3
                    ├── /date-time
                        ├── img1-date-time.jpg.b64
                        ├── img2-date-time.jpg.b64
                        ├── img3-date-time.jpg.b64
    --- IF SAVING AS CSV ---
    CSV CURRENTLY REMOVED FOR VERSION 1 RELEASE
                /messages
                    /channel1
                        msgset1-date-time.csv
                        msgset2-date-time.csv
                        msgset3-date-time.csv
                    /channel2
                        msgset1-date-time.csv
                        msgset2-date-time.csv
                        msgset3-date-time.csv
                    /channel3
                        msgset1-date-time.csv
                        msgset2-date-time.csv
                            msgset3-date-time.csv
        --- MESSAGES ARE STORED BY CHANNEL--
        --- AND SAVED AS ONE FILE PER RUN, PER CHANNEL---