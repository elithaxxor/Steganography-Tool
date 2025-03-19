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
            if f.write:
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

Okay, let's try to figure out what this Python code does. I'll start by reading through the code and the comments.

First, the code imports several modules: os, sys, traceback, io, time, and PIL.Image. The comments mention something about appending bytes after a specific hex value FFD9. From what I remember, FFD9 is the End of Image (EOI) marker in JPEG files. So maybe the code is appending data after that marker.

Looking at the functions, the first one is add_text, which opens an image file in append binary mode and writes some input text as bytes. But wait, the code converts input_text to bytes by prefixing with b, but the function's parameter is input_text. However, in the code, they have _input_text = b'input_text', which is a literal bytes string of 'input_text', not the variable. That seems like a bug. They probably meant to convert the input_text variable to bytes.

Next is read_hidden, which reads the image, finds the index of FFD9, then seeks to OFFSET+2 and tries to read the data after the EOI marker. This would retrieve any data appended after the JPEG's end.

The embed_image_hexData function takes another image, converts it to PNG format using PIL, saves it into a BytesIO buffer, and appends that PNG data to the original image. So this is embedding a PNG image after the JPEG's FFD9 marker.

read_embedded_image_hexData tries to read the embedded image by again finding FFD9, seeking past it, and then using PIL to open the data there. But since the embedded data is a PNG, it might work if PIL can read it from the bytes stream.

Then there's embed_executable_file, which simply appends the contents of an executable file to the original image. And retrieve_embedded_exec does the reverse: finds FFD9, seeks past it, and writes the remaining data to a new executable file.

The main function seems to test all these functions. It prompts for input text, adds it to the image, reads hidden data, embeds another image, tries to read that embedded image, embeds an executable, and then retrieves it.

So the overall purpose is to hide data (text, another image, an executable) within a JPEG file by appending it after the EOI marker. Since JPEG readers stop at FFD9, the appended data is ignored when viewing the image normally. But someone with this code can extract the hidden data.

The comments mention that embedding an executable could execute upon running, which is a security risk. The code seems to be a form of steganography, hiding files within image files. However, the note about the embedded file executing upon running the program might refer to if the image is treated as an executable, which isn't standard. But if someone extracts the executable and runs it, that's when it would execute.

Potential issues I see: The add_text function's byte conversion is incorrect. Also, when embedding a PNG, the code appends the PNG bytes to the JPEG, which works because the JPEG reader ignores data after FFD9. Retrieving the embedded PNG by seeking past FFD9 and reading the rest should work. For the executable, same approach—appending the EXE after FFD9, then extracting it later.

In summary, this code allows hiding additional data (text, images, executables) within a JPEG image by appending the data after the JPEG's end marker. It includes functions to embed and retrieve such hidden data.

This code is designed to perform steganography by embedding hidden data (such as text, images, or executables) into JPEG images. The hidden data is appended after the JPEG's End of Image (EOI) marker (FFD9), which allows it to remain undetected when the image is viewed normally. Here's a breakdown of its functionality:
Key Features:

    Append Text/Data to JPEG:

        The add_text function appends custom text (as bytes) after the FFD9 marker in the JPEG file. However, there's a bug: it hardcodes b'input_text' instead of using the provided input_text variable.

    Read Hidden Text/Data:

        The read_hidden function locates the FFD9 marker, skips past it, and reads any appended data.

    Embed Images:

        embed_image_hexData converts another image (e.g., PNG) into bytes and appends it to the JPEG.

        read_embedded_image_hexData extracts the embedded image data and saves it as a new PNG file.

    Embed Executables:

        embed_executable_file appends an executable (e.g., .exe) to the JPEG.

        retrieve_embedded_exec extracts the executable from the JPEG and writes it to a file.

Workflow:

    The main function tests all features:

        Embeds user-provided text into photo.jpg.

        Reads the hidden text.

        Embeds photo2.jpg into photo.jpg.

        Extracts the embedded image.

        Embeds and retrieves an executable (sample.exe).

Risks:

    Malware Potential: If an embedded executable is extracted and run, it could execute malicious code. The code itself does not trigger execution but facilitates hiding such files.

    Compatibility: The hidden data is not part of the JPEG structure and relies on appending after FFD9. Some tools might strip this data.

Limitations/Bugs:

    The add_text function incorrectly hardcodes the byte string instead of using user input.

    The code assumes all JPEGs end with FFD9, which is standard but not guaranteed in modified files.

    Error handling is present but limited; some functions may fail silently.

Summary:

This script is a steganography tool for hiding files within JPEG images. It exploits the JPEG file structure to append data after the image's end marker, allowing covert storage and retrieval of text, images, or executables. Use cases range from benign data hiding to malicious payload delivery.
