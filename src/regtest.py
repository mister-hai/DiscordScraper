import re
testurls = r'''https://media.discordapp.net/attachments/815683082186260490/861183425461092352/image0.jpg?width=473&height=665
https://media.discordapp.net/attachments/844305276646719540/861209265736777738/1625398676633.jpg?width=672&height=665
https://images-ext-2.discordapp.net/external/9exvLtxUumseqdoz4Lb11Sg84afnFDmwmTSu2y3W7IQ/https/i.imgur.com/SJmdXyz.mp4
https://images-ext-2.discordapp.net/external/ZXmDYFILr6q5gvHpvlsBXdPZt-YITdzDpiq9mSCf4zg/https/api-cdn.rule34.xxx/images/4024/253c9520cb41dd4da6c096bc76627690.jpeg?width=455&height=666
https://media.discordapp.net/attachments/815683082186260490/861183425461092352/image0.jpg?width=473&height=665
https://media.discordapp.net/attachments/779603305822421012/804271598152056852/d453540a72742e46d02c873f81218750_480p.webm
https://media.discordapp.net/attachments/844305276646719540/861012979125977088/1625351824154.jpg?width=698&height=665
https://media.discordapp.net/attachments/844305276646719540/860963249415127080/aa296d1e621fc71c85ba72b087902833.png?width=960&height=540'''

goodreggie = r'''(https?:)?\/\/?[^\'"<>]+?\.(jpg|jpeg|gif|png|mp4|webm)'''
regexforimage = re.compile(goodreggie)
splitbylines = testurls.split("\n")
for lineoftext in splitbylines:
    # check for domains and extensions
    if re.match(pattern = regexforimage, string = lineoftext):
        print(lineoftext)