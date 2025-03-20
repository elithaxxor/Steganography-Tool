mport os, sys, traceback, io, time
import PIL.Image
# copyleft material, all wrongs reserved.

############ IMPORTANT CODE FOR REFACTOR ###############
##  IMAGE OFFSET (HEX VAL) == FFD9
## 'ab' == append bytes
## OFFSET = byte_content.index(bytes.fromhex('FFD9')) --> to find hex offset val
## f.seek(OFFSET+2) --> to read hex after .picture offset val.
## inject_bytes = PIL.Image.open(inject_img_bytes) <-- create new file
## byte_array = io.BytesIO() <-- create new file
## inject_bytes.save(byte_array, format='PNG') <-- create new file
##     try: [<--- WRITE BINARY TO FILE]
##        with open(orig_img, 'ab') as f, open(exec_file, 'rb') as e:
##            f.write(e.read())
#########################################################

''' 
    * The code embeds hidden messages into png, and writes binary data to datastructure. The emedded file will execute upon running program, so beware.. 
    * Currently works with pictures [offset val FFD9]; however- the code can be refactored for .PDF .Doc etc.. [Refactor The Code Finding Data-Structures 
    * Offset Value in Hex. 
'''
### Global Vars ###
# names
img_name = '/photo.jpg'
img_name_2 = '/photo2.jpg'
executable_toEmbed = 'sample.exe'

# dirs
cwd = os.getcwd()
img_dir = str(cwd) + str(img_name)
img_dir_2 = str(cwd) + str(img_name_2)
exec_dir = str(cwd) + str(executable_toEmbed)



if __name__ == '__main__':
    main()

