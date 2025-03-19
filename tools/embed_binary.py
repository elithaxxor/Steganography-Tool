#steganography_tool_basic
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


## Logic ##
def add_text(img_dir, input_text):
    ''' To Inject Custom Custom Str Byte Data to Img. '''
    time.sleep(.5)
    try:
        with open(img_dir, 'ab') as f:
            _input_text = b'input_text'
            print(type(_input_text))
            print('adding [byte-text]: ', _input_text)
            f.write(_input_text)
            if f.write:
                return 1
            else:
                return 0
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print(f'[-] Exception in add_text, {str(e)}, \n\n {traceback.format_exc()}')


#### IMAGE OFFSET (HEX VAL) == FFD9
def read_hidden(img_dir):
    ''' To read Hidden image from Function(add_text) '''
    time.sleep(.5)
    try:
        with open(img_dir, 'rb') as f:
            byte_content=f.read()
            #print(byte_content)
            OFFSET = byte_content.index(bytes.fromhex('FFD9'))
            f.seek(OFFSET+2) ## move two bytes past the offsetval (FFD9) to read injected bytedata
            # print('[OFFSET-LEN]--> should be less', len(OFFSET))
            print('byte_content\n\n\t', byte_content, '[OFFSET]\n\t', OFFSET, '[OFFSET+2]\n\t', OFFSET+2)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print(f'[-] Exception in read_hidden, {str(e)},\n\n {traceback.format_exc()}')

def embed_image_hexData(org_img, inject_img_bytes):
    ''' To Inject The Byte Data from One Image to Another Image '''
    time.sleep(.5)

    try:
        inject_bytes = PIL.Image.open(inject_img_bytes)
        byte_array = io.BytesIO()
        inject_bytes.save(byte_array, format='PNG')
        with open(org_img, 'ab') as f:  ## will write bytedata--> the picture image remains unchanged. (look into hex-data)
            f.write(byte_array.getvalue())
            if fwith the actual URLs of your images. This structure will make your README file more visually appealing and informative. If you need further customization, feel free to ask!.write:
                return 1
            else:
                return 0
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print(f'[-] Exception in embed_image_hexData, {str(e)},\n\n {traceback.format_exc()}')

def read_embedded_image_hexData(orig_img, embedded_img):
    ''' Creates a new image with embedded data '''
    time.sleep(.5)
    try:
        with open(orig_img, 'rb') as f:
            byte_content = f.read()
            OFFSET = byte_content.index(bytes.fromhex('FFD9'))
            # print('[NEW-OFFSET-LEN]--> should be more than prev. val. ', len(OFFSET))
            f.seek(OFFSET+2)
            new_img = PIL.Image.open(io.BytesIO(f.read())) ### <--- BUG NEED TO FIX
            new_img.save('embedded_img.png')
            if new_img:
                return 1
            else:
                return 0
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print(f'[-] Exception in read_embedded_image_hexData, {str(e)},\n\n {traceback.format_exc()}')

def embed_executable_file(orig_img, exec_file):
    ''' USE THIS FUNCTION TO EMBEDD EXECUTABLE FILES '''
    try:
        with open(orig_img, 'ab') as f, open(exec_file, 'rb') as e:
            f.write(e.read())
            if f.write:
                return 1
            else:
                return 0
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print(f'[-] Exception in embed_executable_file, {str(e)},\n\n {traceback.format_exc()}')

def retrieve_embedded_exec(orig_img, exec_file):
    print(f'[+].. Reading Binary for executable thats embedded in jpg... \n\t\t [EXEC-FILE] {exec_file}  \n\t\t [IMG-LOC] {orig_img}')
    try:
        with open(orig_img, 'rb') as f:
            content = f.read()
            OFFSET = content.index(bytes.fromhex('FFD9'))
            f.seek(OFFSET+2)
        with open(exec_file, 'wb') as e:
            e.write(f.read())
            if e.write:
                return 1
            else: return 0
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print(f'[-] Exception in retrieve_embedded_exec, {str(e)},\n\n {traceback.format_exc()}')



## init ##
def main():
    print('x'*50)
    input_text = input('add the text to embed:')
    print('[+] To Add Code to Images [+]')
    print('[!] Copyleft material, all wrongs reserved!')
    print('[+] Processing \n', img_dir)
    text_results = add_text(str(img_dir), str(input_text))
    print('adding text result: ', text_results,'\n',' X' * 50)
    read_hidden(img_dir)
    embed_img_result = embed_image_hexData(img_dir, img_dir_2)
    print('[?] Did we embedded hex? : ', embed_img_result)
    read_embedded_results = read_embedded_image_hexData(img_dir, img_dir_2)
    print('[?] Could we read the embedded text? ', read_embedded_results)
    exec_results = embed_executable_file(img_dir, exec_dir)
    print('[?] Did we embed the executable? ', exec_results)
    retreive_exec_results = retrieve_embedded_exec(img_dir, exec_dir)
    print('[?] Were we able to retrieve the executable... ?  ', retreive_exec_results)

if __name__ == '__main__':
    main()
