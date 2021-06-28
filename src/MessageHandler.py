
class MessageHandler():
    def __init__(self):
        pass
    
    def thing(self,message):
        # Getting the embed and converting it to a dict
        embed = message.embeds[0]
        embed_dict = embed.to_dict()

        for field in embed_dict['fields']:
            if field['name'] :#== user_input['field name']:
                pass
    
    def filterbychannel():
        channel = client.get_channel(730839966472601622)
        messages = await ctx.channel.history(limit=200).flatten()
        for msg in messages:
            if word in msg.content:
                print(msg.jump_url)        

    def checkimagesdir(self):
        directory_listing = scanfilesbyextension(imagedirectory,arguments.imagesaveformat)
        return directory_listing

    def savemessageinloop(self,message):
            #if they want a CSV file of the message contents
            if SAVETOCSV == True:
                messagedirectory = os.getcwd() +"/messages/"
                #name the directory/file according to the spec
                messagedirectoryNOW = messagedirectory + message.channel + timeofrun
                #file_location = arguments.dbname + str(today) # Set the string to where you want the file to be saved to
                data.to_csv(messagedirectoryNOW)
            #
            # SAVING THE MESSAGES FOR THAT RUN IN A SQLITE3DB
            # - SINGLE FILE
            # - NO TIME DATE STAMP
            # - NO CHANNEL SUBDIRECTORY
            elif SAVETOCSV == False:
                messagesent = DiscordMessage(channel = data['channel'],
                                            time     = data['time'],
                                            sender   = data['sender'],
                                            content  = data['content'],
                                            file     = data['file'])
                #push to DB
                addmsgtodb(messagesent)
                #dbpacker.channelscrapetodb(data)

    def savefile(self,imagedata,filename):
        '''Saves a meggage according to global configuration'''
        try:
            databasefolder      = "/database"
            baseimagefolder     = databasefolder + "/images/"
            imagefoldernow      = baseimagefolder + timeofrun
            # add the time and sender/messageID to name
            # just in case of data loss
            fullfilepath = imagefoldernow + "/" + filename + str(datetime.now()) + "_" + msg.author
            #craft the path with folder information
            if os.path.isdir(imagefoldernow) == False:
                os.makedirs(imagefoldernow, exist_ok=True)
            with open(filename,'wb') as out_file:
                shutil.copyfileobj(imagedata, out_file)
            return fullfilepath
        except Exception:
            errormessage("[-] ERROR Saving Image Data to disk!")


    def checkurlagainstdomain(self,urltoscan,listofdomains):
        '''logic for allowing the control flow to continue'''
        parsedurl = urlparse(urltoscan)
        domainrequested = parsedurl.netloc.split('/')[2].split(':')[0]
        if domainrequested in listofdomains:
            return True
        else:
            return False


    def filtermessage(self,message):
        '''logic for allowing the control flow to continue'''
        if message.author != bot.user:
            return True
        else:
            return False

    def filterattachment(self,attachment,urlfilter = domainlist, extensionfilter = fileextensionfilter):
        '''logic for allowing the control flow to continue'''
        if (attachment.url != None):
            if (attachment.filename.endswith(extensionfilter)):
                if (checkurlagainstdomain(attachment.url, urlfilter)):
                    return True

    def grabimage(self,token,imageurl,savefilename):
        try:
            imageblob = SaveDiscordImage( imageurl = imageurl,
                            token        = token,
                            base64orfile = arguments.saveformat,
                            filename     = savefilename,
                            imagesaveformat = arguments.imagesaveformat
                            )
            return imageblob
        except Exception:
            errormessage("[-] Failed To Grab Image: {}".format(imageurl))
    
    def writetodbfolder(self):
        pass        
