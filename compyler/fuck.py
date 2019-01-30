 # elif re.match(r'[\s]', char):
#     self.pos += 1
#     continue

# Begin Comment(leading slash)
if re.match(r'[\/]', char):
    # look one ahead to see if it is a comment or just a slash
    print('open slash')
    if re.match(r'[\*]', self.code[self.pos+1]):
        print('open star')
        # Tell the lexer we are in a comment
        # Ignore till out of comment
        comment = True
    else:
        continue
    
        

# while in a comment check for end of comment, otherwise skip over
elif comment:
    # print(char)
    if re.match(r'[\*]', char):
        print('close star')
        if re.match(r'[\/]', self.code[self.pos+1]):
            print('close slash')
            # Comment was ended!
            comment = False
            self.pos += 1
            continue
    else:
        # self.buffer = ''
        self.pos += 1
        continue

