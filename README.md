# DiscordScraper
 does what it says on the box

 Discord Message Archival
    
    --imagestoretype',
        default = "file", 
        help    = "set if images are saved in the DB as text or externally as files, 
        OPTIONS: 'file' OR 'base64'.
    
    --messagelimit',
        default = "10000", 
        help    = "Number of messages to download" )
    
    --databasename',
        default = "discordmessagehistory", 
        help    = "Name of the file to save the database as" )
    
    --databasetype',
        default = "sqlite3", 
        help    = "text storage format, can be 'sqlite3' OR 'csv', This applies to base64 image data as well"
    
    --imagesaveformat'
        default = ".png", 
        help    = File extension for images