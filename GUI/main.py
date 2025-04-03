#!/usr/bin/env python3
import os
import sys
import logging
import PySimpleGUI as sg
from cryptography.fernet import Fernet

from EmbedExtract import Cryptography, Compressor, EmbedExtract

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
    layout = [
        [sg.Text('EmbedExtract GUI', size=(30, 1), justification='center', font=('Helvetica', 20), relief=sg.RELIEF_RIDGE)],
        [sg.HorizontalSeparator()],
        [sg.TabGroup([[
            sg.Tab('Embed', [
                [sg.Text('File Format:'), sg.Combo(['jpeg', 'png', 'gif', 'pdf', 'qr'], default_value='jpeg', key='format')],
                [sg.Text('Carrier File:'), sg.Input(key='carrier'), sg.FileBrowse()],
                [sg.Text('Payload File:'), sg.Input(key='payload'), sg.FileBrowse()],
                [sg.Text('Optional: Encrypt'), sg.Checkbox('', key='encrypt')],
                [sg.Text('Optional: Compress'), sg.Checkbox('', key='compress')],
                [sg.Button('Embed Data')]
            ]),
            sg.Tab('Extract', [
                [sg.Text('File Format:'), sg.Combo(['jpeg', 'png', 'gif', 'pdf', 'qr'], default_value='jpeg', key='x_format')],
                [sg.Text('Carrier File:'), sg.Input(key='x_carrier'), sg.FileBrowse()],
                [sg.Text('Output Path:'), sg.Input(key='x_output'), sg.FileSaveAs()],
                [sg.Text('Encrypted?'), sg.Checkbox('', key='x_encrypt')],
                [sg.Text('Compressed?'), sg.Checkbox('', key='x_compress')],
                [sg.Button('Extract Data')]
            ])
        ]])],
        [sg.Button('Exit')]
    ]
    return sg.Window('EmbedExtract GUI', layout, element_justification='center', finalize=True)

def handle_embed(embed_extract, crypto, compressor, values):
    """Handle the embedding process."""
    file_format = values['format']
    carrier_path = values['carrier']
    payload_path = values['payload']
    enc = values['encrypt']
    comp = values['compress']

    # Check if the provided carrier and payload files are valid
    if file_format in ['jpeg', 'png', 'gif']:
        if not (carrier_path and os.path.isfile(carrier_path)):
            sg.popup_error('Invalid carrier file.')
            return
        if not (payload_path and os.path.isfile(payload_path)):
            sg.popup_error('Invalid payload file.')
            return
        try:
            # Read the payload file
            with open(payload_path, 'rb') as f:
                data = f.read()
            if comp:
                data = compressor.compress(data)
                logging.info('Data compressed for embedding.')
            if enc:
                data = crypto.encrypt(data)
                logging.info('Data encrypted for embedding.')
            # Embed the data into the carrier file
            success = embed_extract.embed_binary(carrier_path, data, file_format)
            if success:
                sg.popup('Data embedded successfully!')
                logging.info('Embed operation successful.')
            else:
                sg.popup_error('Embed operation failed!')
                logging.error('Embed operation failed.')
        except Exception as e:
            sg.popup_error(f'Error: {str(e)}')
            logging.exception('Exception in embedding data')

    # Similar handling for 'pdf' and 'qr' formats...

def handle_extract(embed_extract, crypto, compressor, values):
    """Handle the extraction process."""
    file_format = values['x_format']
    carrier_path = values['x_carrier']
    output_path = values['x_output']
    enc = values['x_encrypt']
    comp = values['x_compress']

    # Check if the provided carrier file and output path are valid
    if file_format in ['jpeg', 'png', 'gif']:
        if not (carrier_path and os.path.isfile(carrier_path)):
            sg.popup_error('Invalid file.')
            return
        if not output_path:
            sg.popup_error('No output path given.')
            return
        try:
            # Extract the data from the carrier file
            data = embed_extract.extract_binary(carrier_path, file_format)
            if data is None:
                sg.popup_error('No data found or extraction error.')
                logging.error('Extraction operation returned None.')
                return
            if enc:
                data = crypto.decrypt(data)
                logging.info('Data decrypted for extraction.')
            if comp:
                data = compressor.decompress(data)
                logging.info('Data decompressed.')
            # Save the extracted data to the output path
            with open(output_path, 'wb') as f:
                f.write(data)
            sg.popup(f'Data extracted to {output_path}')
            logging.info('Extract operation successful.')
        except Exception as e:
            sg.popup_error(f'Error: {str(e)}')
            logging.exception('Exception in data extraction')

    # Similar handling for 'pdf' and 'qr' formats...

def main():
    """Main function to setup and run the GUI application."""
    setup_logging()
    embed_extract = EmbedExtract()
    crypto = Cryptography()
    compressor = Compressor()
    window = create_main_window()

    # Event loop to process events and get the values of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Embed Data':
            handle_embed(embed_extract, crypto, compressor, values)
        elif event == 'Extract Data':
            handle_extract(embed_extract, crypto, compressor, values)

    window.close()

if __name__ == '__main__':
    main()
