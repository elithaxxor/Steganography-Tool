import os
import sys
import glob
import logging
import PySimpleGUI as sg
from cryptography.fernet import Fernet

from EmbedExtract import Cryptography, Compressor, EmbedExtract
from batch_processor import BatchProcessor
from stego_detector import StegoDetector

# Configure logging
logging.basicConfig(
    filename='embed_extract.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        filename='embed_extract.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def create_main_window():
    """Create the main GUI window."""
    sg.theme('DarkBlue3')
    
    # Define the tabs
    embed_tab_layout = [
        [sg.Text('File Format:'), sg.Combo(['jpeg', 'png', 'gif', 'pdf', 'qr', 'wav', 'mp4'], default_value='jpeg', key='format')],
        [sg.Text('Mode:'), sg.Radio('Single File', 'MODE', default=True, key='single_mode'), 
         sg.Radio('Batch Processing', 'MODE', default=False, key='batch_mode')],
        [sg.Text('Carrier File(s):'), sg.Input(key='carrier'), 
         sg.FileBrowse(key='file_browse', visible=True),
         sg.FolderBrowse(key='folder_browse', visible=False)],
        [sg.Text('Payload File:'), sg.Input(key='payload'), sg.FileBrowse()],
        [sg.Text('Optional: Encrypt'), sg.Checkbox('', key='encrypt')],
        [sg.Text('Optional: Compress'), sg.Checkbox('', key='compress')],
        [sg.Button('Embed Data')],
        [sg.Text('Progress:'), sg.ProgressBar(100, orientation='h', size=(20, 20), key='progress_embed')],
        [sg.Text('', size=(40, 2), key='status_embed')]
    ]
    
    extract_tab_layout = [
        [sg.Text('File Format:'), sg.Combo(['jpeg', 'png', 'gif', 'pdf', 'qr', 'wav', 'mp4'], default_value='jpeg', key='x_format')],
        [sg.Text('Mode:'), sg.Radio('Single File', 'X_MODE', default=True, key='x_single_mode'), 
         sg.Radio('Batch Processing', 'X_MODE', default=False, key='x_batch_mode')],
        [sg.Text('Carrier File(s):'), sg.Input(key='x_carrier'), 
         sg.FileBrowse(key='x_file_browse', visible=True),
         sg.FolderBrowse(key='x_folder_browse', visible=False)],
        [sg.Text('Output Path:'), sg.Input(key='x_output'), 
         sg.FileSaveAs(key='x_file_save', visible=True),
         sg.FolderBrowse(key='x_folder_save', visible=False)],
        [sg.Text('Encrypted?'), sg.Checkbox('', key='x_encrypt')],
        [sg.Text('Compressed?'), sg.Checkbox('', key='x_compress')],
        [sg.Button('Extract Data')],
        [sg.Text('Progress:'), sg.ProgressBar(100, orientation='h', size=(20, 20), key='progress_extract')],
        [sg.Text('', size=(40, 2), key='status_extract')]
    ]
    
    # Add new Detect tab
    detect_tab_layout = [
        [sg.Text('Select a file to analyze for steganography:')],
        [sg.Input(key='detect_file'), sg.FileBrowse()],
        [sg.Button('Detect Steganography')],
        [sg.Text('Progress:'), sg.ProgressBar(100, orientation='h', size=(20, 20), key='progress_detect')],
        [sg.Text('', size=(50, 1), key='result_detect')],
        [sg.Multiline('', size=(60, 10), key='details_detect', disabled=True)]
    ]
    
    layout = [
        [sg.Text('EmbedExtract GUI', size=(30, 1), justification='center', font=('Helvetica', 20), relief=sg.RELIEF_RIDGE)],
        [sg.HorizontalSeparator()],
        [sg.TabGroup([[
            sg.Tab('Embed', embed_tab_layout),
            sg.Tab('Extract', extract_tab_layout),
            sg.Tab('Detect', detect_tab_layout)
        ]])],
        [sg.Button('Exit')]
    ]
    
    window = sg.Window('EmbedExtract GUI', layout, element_justification='center', finalize=True)
    
    # Setup event handlers for mode changes
    window['single_mode'].update(True)
    window['batch_mode'].update(False)
    window['file_browse'].update(visible=True)
    window['folder_browse'].update(visible=False)
    
    window['x_single_mode'].update(True)
    window['x_batch_mode'].update(False)
    window['x_file_browse'].update(visible=True)
    window['x_folder_browse'].update(visible=False)
    window['x_file_save'].update(visible=True)
    window['x_folder_save'].update(visible=False)
    
    return window

def handle_embed_single(window, embed_extract, crypto, compressor, values):
    """Handle single file embedding process."""
    file_format = values['format']
    carrier_path = values['carrier']
    payload_path = values['payload']
    enc = values['encrypt']
    comp = values['compress']

    # Check if the provided payload file is valid
    if not (payload_path and os.path.isfile(payload_path)):
        sg.popup_error('Invalid payload file.')
        return

    try:
        window['progress_embed'].update(0)
        window['status_embed'].update('Reading payload file...')
        
        # Read the payload file
        with open(payload_path, 'rb') as f:
            data = f.read()
        
        window['progress_embed'].update(10)
        
        if comp:
            window['status_embed'].update('Compressing data...')
            data = compressor.compress(data)
            logging.info('Data compressed for embedding.')
            window['progress_embed'].update(20)
        
        if enc:
            window['status_embed'].update('Encrypting data...')
            data = crypto.encrypt(data)
            logging.info('Data encrypted for embedding.')
            window['progress_embed'].update(30)
        
        window['status_embed'].update('Embedding data...')
        
        if file_format in ['jpeg', 'png', 'gif']:
            if not (carrier_path and os.path.isfile(carrier_path)):
                sg.popup_error('Invalid carrier file.')
                return
            # Embed the data into the carrier file
            success = embed_extract.embed_binary(carrier_path, data, file_format)
            window['progress_embed'].update(90)
        
        elif file_format == 'pdf':
            if not (carrier_path and os.path.isfile(carrier_path)):
                sg.popup_error('Invalid carrier file.')
                return
            # Embed the data into the PDF file
            success = embed_extract.embed_pdf(carrier_path, data)
            window['progress_embed'].update(90)
        
        elif file_format == 'qr':
            # Generate a QR code with the embedded data
            output_path = sg.popup_get_file('Save QR Code as:', save_as=True, file_types=(('PNG Files', '*.png'),))
            if not output_path:
                return
            success = embed_extract.embed_qr(data, output_path)
            window['progress_embed'].update(90)
        
        elif file_format == 'wav':
            if not (carrier_path and os.path.isfile(carrier_path)):
                sg.popup_error('Invalid carrier file.')
                return
            # Embed the data into the WAV file
            success = embed_extract.embed_audio(carrier_path, data)
            window['progress_embed'].update(90)
        
        elif file_format == 'mp4':
            if not (carrier_path and os.path.isfile(carrier_path)):
                sg.popup_error('Invalid carrier file.')
                return
            # Embed the data into the video file
            success = embed_extract.embed_video(carrier_path, data)
            window['progress_embed'].update(90)
        
        else:
            sg.popup_error(f'Unsupported file format: {file_format}')
            return
        
        window['progress_embed'].update(100)
        
        if success:
            window['status_embed'].update('Data embedded successfully!')
            sg.popup('Data embedded successfully!')
            logging.info('Embed operation successful.')
        else:
            window['status_embed'].update('Embed operation failed!')
            sg.popup_error('Embed operation failed!')
            logging.error('Embed operation failed.')
    
    except Exception as e:
        window['status_embed'].update(f'Error: {str(e)}')
        sg.popup_error(f'Error: {str(e)}')
        logging.exception('Exception in embedding data')

def handle_embed_batch(window, batch_processor, values):
    """Handle batch embedding process."""
    file_format = values['format']
    carrier_dir = values['carrier']
    payload_path = values['payload']
    enc = values['encrypt']
    comp = values['compress']

    # Check if the provided payload file is valid
    if not (payload_path and os.path.isfile(payload_path)):
        sg.popup_error('Invalid payload file.')
        return

    # Check if the provided carrier directory is valid
    if not (carrier_dir and os.path.isdir(carrier_dir)):
        sg.popup_error('Invalid carrier directory.')
        return

    try:
        window['progress_embed'].update(0)
        window['status_embed'].update('Reading payload file...')
        
        # Read the payload file
        with open(payload_path, 'rb') as f:
            data = f.read()
        
        window['progress_embed'].update(10)
        window['status_embed'].update('Finding carrier files...')
        
        # Get all files of the specified format in the directory
        if file_format in ['jpeg', 'png', 'gif']:
            extensions = {
                'jpeg': ['*.jpg', '*.jpeg'],
                'png': ['*.png'],
                'gif': ['*.gif']
            }
            patterns = extensions.get(file_format, [f'*.{file_format}'])
            carrier_files = []
            for pattern in patterns:
                carrier_files.extend(glob.glob(os.path.join(carrier_dir, pattern)))
        elif file_format == 'pdf':
            carrier_files = glob.glob(os.path.join(carrier_dir, '*.pdf'))
        elif file_format == 'wav':
            carrier_files = glob.glob(os.path.join(carrier_dir, '*.wav'))
        elif file_format == 'mp4':
            carrier_files = glob.glob(os.path.join(carrier_dir, '*.mp4'))
        else:
            sg.popup_error(f'Unsupported file format for batch processing: {file_format}')
            return
        
        if not carrier_files:
            sg.popup_error(f'No {file_format} files found in the specified directory.')
            return
        
        window['progress_embed'].update(20)
        window['status_embed'].update(f'Found {len(carrier_files)} carrier files. Processing...')
        
        # Setup progress callback
        def update_progress(completed, total):
            # Scale from 20 to 90 percent
            progress = 20 + int(70 * completed / total)
            window['progress_embed'].update(progress)
            window['status_embed'].update(f'Processing file {completed} of {total}...')
            window.refresh()
        
        batch_processor.set_progress_callback(update_progress)
        
        # Process batch
        results = batch_processor.process_batch_embed(
            file_format,
            carrier_files,
            data,
            encrypt=enc,
            compress=comp
        )
        
        window['progress_embed'].update(100)
        
        # Count successes and failures
        successes = sum(1 for success in results.values() if success)
        failures = len(results) - successes
        
        window['status_embed'].update(f'Completed: {successes} successful, {failures} failed.')
        sg.popup(f'Batch processing completed!\n\nSuccessful: {successes}\nFailed: {failures}')
        logging.info(f'Batch embed operation completed. Successful: {successes}, Failed: {failures}')
    
    except Exception as e:
        window['status_embed'].update(f'Error: {str(e)}')
        sg.popup_error(f'Error: {str(e)}')
        logging.exception('Exception in batch embedding data')

def handle_extract_single(window, embed_extract, crypto, compressor, values):
    """Handle single file extraction process."""
    file_format = values['x_format']
    carrier_path = values['x_carrier']
    output_path = values['x_output']
    enc = values['x_encrypt']
    comp = values['x_compress']

    # Check if the provided carrier file is valid
    if not (carrier_path and os.path.isfile(carrier_path)):
        sg.popup_error('Invalid carrier file.')
        return

    if not output_path:
        sg.popup_error('No output path given.')
        return

    try:
        window['progress_extract'].update(0)
        window['status_extract'].update('Extracting data...')
        
        # Extract the data from the carrier file
        if file_format in ['jpeg', 'png', 'gif']:
            data = embed_extract.extract_binary(carrier_path, file_format)
        
        elif file_format == 'pdf':
            data = embed_extract.extract_pdf(carrier_path)
        
        elif file_format == 'qr':
            data = embed_extract.extract_qr(carrier_path)
        
        elif file_format == 'wav':
            data = embed_extract.extract_audio(carrier_path)
        
        elif file_format == 'mp4':
            data = embed_extract.extract_video(carrier_path)
        
        else:
            sg.popup_error(f'Unsupported file format: {file_format}')
            return
        
        window['progress_extract'].update(50)
        
        if data is None:
            window['status_extract'].update('No data found or extraction error.')
            sg.popup_error('No data found or extraction error.')
            logging.error('Extraction operation returned None.')
            return
        
        if enc:
            window['status_extract'].update('Decrypting data...')
            try:
                data = crypto.decrypt(data)
                logging.info('Data decrypted for extraction.')
                window['progress_extract'].update(70)
            except Exception as e:
                window['status_extract'].update(f'Decryption error: {str(e)}')
                sg.popup_error(f'Decryption error: {str(e)}. Was the data encrypted?')
                return
        
        if comp:
            window['status_extract'].update('Decompressing data...')
            try:
                data = compressor.decompress(data)
                logging.info('Data decompressed.')
                window['progress_extract'].update(90)
            except Exception as e:
                window['status_extract'].update(f'Decompression error: {str(e)}')
                sg.popup_error(f'Decompression error: {str(e)}. Was the data compressed?')
                return
        
        # Save the extracted data to the output path
        window['status_extract'].update('Saving extracted data...')
        with open(output_path, 'wb') as f:
            f.write(data)
        
        window['progress_extract'].update(100)
        window['status_extract'].update(f'Data extracted to {output_path}')
        sg.popup(f'Data extracted to {output_path}')
        logging.info('Extract operation successful.')
    
    except Exception as e:
        window['status_extract'].update(f'Error: {str(e)}')
        sg.popup_error(f'Error: {str(e)}')
        logging.exception('Exception in data extraction')

def handle_extract_batch(window, batch_processor, values):
    """Handle batch extraction process."""
    file_format = values['x_format']
    carrier_dir = values['x_carrier']
    output_dir = values['x_output']
    enc = values['x_encrypt']
    comp = values['x_compress']

    # Check if the provided carrier directory is valid
    if not (carrier_dir and os.path.isdir(carrier_dir)):
        sg.popup_error('Invalid carrier directory.')
        return

    # Check if the provided output directory is valid
    if not output_dir:
        sg.popup_error('No output directory given.')
        return
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    try:
        window['progress_extract'].update(0)
        window['status_extract'].update('Finding carrier files...')
        
        # Get all files of the specified format in the directory
        if file_format in ['jpeg', 'png', 'gif']:
            extensions = {
                'jpeg': ['*.jpg', '*.jpeg'],
                'png': ['*.png'],
                'gif': ['*.gif']
            }
            patterns = extensions.get(file_format, [f'*.{file_format}'])
            carrier_files = []
            for pattern in patterns:
                carrier_files.extend(glob.glob(os.path.join(carrier_dir, pattern)))
        elif file_format == 'pdf':
            carrier_files = glob.glob(os.path.join(carrier_dir, '*.pdf'))
        elif file_format == 'qr':
            carrier_files = glob.glob(os.path.join(carrier_dir, '*.png'))  # QR codes are typically stored as PNG
        elif file_format == 'wav':
            carrier_files = glob.glob(os.path.join(carrier_dir, '*.wav'))
        elif file_format == 'mp4':
            carrier_files = glob.glob(os.path.join(carrier_dir, '*.mp4'))
        else:
            sg.popup_error(f'Unsupported file format for batch processing: {file_format}')
            return
        
        if not carrier_files:
            sg.popup_error(f'No {file_format} files found in the specified directory.')
            return
        
        window['progress_extract'].update(10)
        window['status_extract'].update(f'Found {len(carrier_files)} carrier files. Processing...')
        
        # Setup progress callback
        def update_progress(completed, total):
            # Scale from 10 to 90 percent
            progress = 10 + int(80 * completed / total)
            window['progress_extract'].update(progress)
            window['status_extract'].update(f'Processing file {completed} of {total}...')
            window.refresh()
        
        batch_processor.set_progress_callback(update_progress)
        
        # Process batch
        results = batch_processor.process_batch_extract(
            file_format,
            carrier_files,
            output_dir,
            encrypt=enc,
            compress=comp
        )
        
        window['progress_extract'].update(100)
        
        # Count successes and failures
        successes = sum(1 for success in results.values() if success)
        failures = len(results) - successes
        
        window['status_extract'].update(f'Completed: {successes} successful, {failures} failed.')
        sg.popup(f'Batch processing completed!\n\nSuccessful: {successes}\nFailed: {failures}\n\nFiles saved to: {output_dir}')
        logging.info(f'Batch extract operation completed. Successful: {successes}, Failed: {failures}')
    
    except Exception as e:
        window['status_extract'].update(f'Error: {str(e)}')
        sg.popup_error(f'Error: {str(e)}')
        logging.exception('Exception in batch data extraction')

def handle_detect(window, stego_detector, values):
    """Handle steganography detection process."""
    file_path = values['detect_file']
    
    # Check if the provided file is valid
    if not (file_path and os.path.isfile(file_path)):
        sg.popup_error('Invalid file.')
        return
    
    try:
        window['progress_detect'].update(10)
        window['result_detect'].update('Analyzing file...')
        window['details_detect'].update('')
        
        # Perform detection
        probability, details, file_type, interpretation = stego_detector.detect_file(file_path)
        
        window['progress_detect'].update(100)
        
        # Format result message
        result_message = f"Detection Result: {probability:.2%} - {interpretation}"
        window['result_detect'].update(result_message)
        
        # Format details
        details_text = f"File Type: {file_type}\n\n"
        details_text += f"Analysis Details:\n"
        
        for key, value in details.items():
            if isinstance(value, float):
                details_text += f"- {key}: {value:.4f}\n"
            else:
                details_text += f"- {key}: {value}\n"
        
        window['details_detect'].update(details_text)
        
        logging.info(f'Steganography detection completed for {file_path}. Probability: {probability:.2%}')
    
    except Exception as e:
        window['result_detect'].update(f'Error: {str(e)}')
        window['details_detect'].update(f'An error occurred during detection:\n{str(e)}')
        sg.popup_error(f'Error: {str(e)}')
        logging.exception('Exception in steganography detection')

def main():
    """Main function to setup and run the GUI application."""
    setup_logging()
    embed_extract = EmbedExtract()
    crypto = Cryptography()
    compressor = Compressor()
    batch_processor = BatchProcessor(embed_extract, crypto, compressor)
    stego_detector = StegoDetector()
    window = create_main_window()

    # Event loop to process events and get the values of the inputs
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        
        # Handle mode changes for embed tab
        elif event == 'single_mode':
            window['file_browse'].update(visible=True)
            window['folder_browse'].update(visible=False)
            window['carrier'].update('')
        
        elif event == 'batch_mode':
            window['file_browse'].update(visible=False)
            window['folder_browse'].update(visible=True)
            window['carrier'].update('')
        
        # Handle mode changes for extract tab
        elif event == 'x_single_mode':
            window['x_file_browse'].update(visible=True)
            window['x_folder_browse'].update(visible=False)
            window['x_file_save'].update(visible=True)
            window['x_folder_save'].update(visible=False)
            window['x_carrier'].update('')
            window['x_output'].update('')
        
        elif event == 'x_batch_mode':
            window['x_file_browse'].update(visible=False)
            window['x_folder_browse'].update(visible=True)
            window['x_file_save'].update(visible=False)
            window['x_folder_save'].update(visible=True)
            window['x_carrier'].update('')
            window['x_output'].update('')
        
        # Handle embed operation
        elif event == 'Embed Data':
            if values['single_mode']:
                handle_embed_single(window, embed_extract, crypto, compressor, values)
            else:  # batch_mode
                handle_embed_batch(window, batch_processor, values)
        
        # Handle extract operation
        elif event == 'Extract Data':
            if values['x_single_mode']:
                handle_extract_single(window, embed_extract, crypto, compressor, values)
            else:  # batch_mode
                handle_extract_batch(window, batch_processor, values)
        
        # Handle detect operation
        elif event == 'Detect Steganography':
            handle_detect(window, stego_detector, values)

    window.close()

if __name__ == '__main__':
    main()
