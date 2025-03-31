#!/usr/bin/env python3
import os
import sys
import logging
import PySimpleGUI as sg
from cryptography.fernet import Fernet

from EmbedExtract import Cryptography, Compressor, EmbedExtract
# Example: from core.EmbedExtract import Cryptography, Compressor, EmbedExtract

logging.basicConfig(
    filename='embed_extract.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    sg.theme('DarkBlue3')  # Elegant theme

    embed_extract = EmbedExtract()
    crypto = Cryptography()
    compressor = Compressor()

    # Layout
    layout = [
        [sg.Text('EmbedExtract GUI', size=(30,1), justification='center', font=('Helvetica', 20), relief=sg.RELIEF_RIDGE)],
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

    window = sg.Window('EmbedExtract GUI', layout, element_justification='center', finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event == 'Embed Data':
            file_format = values['format']
            carrier_path = values['carrier']
            payload_path = values['payload']
            enc = values['encrypt']
            comp = values['compress']

            if file_format in ['jpeg','png','gif']:  # image-based
                if not (carrier_path and os.path.isfile(carrier_path)):
                    sg.popup_error('Invalid carrier file.')
                    continue
                if not (payload_path and os.path.isfile(payload_path)):
                    sg.popup_error('Invalid payload file.')
                    continue
                try:
                    with open(payload_path, 'rb') as f:
                        data = f.read()

                    if comp:
                        data = compressor.compress(data)
                        logging.info('Data compressed for embedding.')
                    if enc:
                        data = crypto.encrypt(data)
                        logging.info('Data encrypted for embedding.')

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

            elif file_format == 'pdf':
                if not (carrier_path and os.path.isfile(carrier_path)):
                    sg.popup_error('Invalid PDF file.')
                    continue
                if not (payload_path and os.path.isfile(payload_path)):
                    sg.popup_error('Invalid payload file.')
                    continue
                try:
                    with open(payload_path, 'rb') as f:
                        data = f.read()

                    if comp:
                        data = compressor.compress(data)
                        logging.info('PDF data compressed.')
                    if enc:
                        data = crypto.encrypt(data)
                        logging.info('PDF data encrypted.')

                    success = embed_extract.embed_pdf(carrier_path, data)
                    if success:
                        sg.popup('Data embedded in PDF metadata successfully!')
                        logging.info('PDF embed operation successful.')
                    else:
                        sg.popup_error('PDF embed operation failed!')
                        logging.error('PDF embed operation failed.')
                except Exception as e:
                    sg.popup_error(f'Error: {str(e)}')
                    logging.exception('Exception in PDF embedding')

            elif file_format == 'qr':
                data = sg.popup_get_text('Enter the data for the QR code:')
                if data is None:
                    continue
                out_file = sg.popup_get_file('Save QR code as:', save_as=True, default_extension='.png')
                if not out_file:
                    continue
                try:
                    if comp:
                        data = compressor.compress(data.encode())  # compress requires bytes
                        logging.info('QR data compressed.')
                    else:
                        data = data.encode()

                    if enc:
                        data = crypto.encrypt(data)
                        logging.info('QR data encrypted.')

                    # Create QR code from final data
                    embed_extract.create_qr(data, out_file)
                    sg.popup(f'QR Code created: {out_file}')
                    logging.info('QR code created successfully.')
                except Exception as e:
                    sg.popup_error(f'Error: {str(e)}')
                    logging.exception('Exception in QR code creation')

        elif event == 'Extract Data':
            file_format = values['x_format']
            carrier_path = values['x_carrier']
            output_path = values['x_output']
            enc = values['x_encrypt']
            comp = values['x_compress']

            if file_format in ['jpeg','png','gif']:
                if not (carrier_path and os.path.isfile(carrier_path)):
                    sg.popup_error('Invalid file.')
                    continue
                if not output_path:
                    sg.popup_error('No output path given.')
                    continue

                try:
                    data = embed_extract.extract_binary(carrier_path, file_format)
                    if data is None:
                        sg.popup_error('No data found or extraction error.')
                        logging.error('Extraction operation returned None.')
                        continue
                    if enc:
                        data = crypto.decrypt(data)
                        logging.info('Data decrypted for extraction.')
                    if comp:
                        data = compressor.decompress(data)
                        logging.info('Data decompressed.')

                    with open(output_path, 'wb') as f:
                        f.write(data)
                    sg.popup(f'Data extracted to {output_path}')
                    logging.info('Extract operation successful.')

                except Exception as e:
                    sg.popup_error(f'Error: {str(e)}')
                    logging.exception('Exception in data extraction')

            elif file_format == 'pdf':
                if not (carrier_path and os.path.isfile(carrier_path)):
                    sg.popup_error('Invalid PDF file.')
                    continue
                if not output_path:
                    sg.popup_error('No output path specified.')
                    continue
                try:
                    data = embed_extract.extract_pdf(carrier_path)
                    if not data:
                        sg.popup_error('No data found or extraction error.')
                        logging.error('No data returned from PDF extract.')
                        continue
                    if enc:
                        data = crypto.decrypt(data)
                        logging.info('PDF data decrypted.')
                    if comp:
                        data = compressor.decompress(data)
                        logging.info('PDF data decompressed.')

                    with open(output_path, 'wb') as f:
                        f.write(data)
                    sg.popup(f'Data extracted to {output_path}')
                    logging.info('PDF data extract operation successful.')
                except Exception as e:
                    sg.popup_error(f'Error: {str(e)}')
                    logging.exception('Exception in PDF extract')

            elif file_format == 'qr':
                if not (carrier_path and os.path.isfile(carrier_path)):
                    sg.popup_error('Invalid QR image file.')
                    continue
                try:
                    raw_data = embed_extract.decode_qr(carrier_path)
                    if not raw_data:
                        sg.popup_error('No data found in QR code.')
                        logging.warning('No data found in QR code.')
                        continue

                    # Attempt decrypt or decompress only if user indicates
                    if enc:
                        raw_data = crypto.decrypt(raw_data)
                        logging.info('QR data decrypted.')
                    if comp:
                        raw_data = compressor.decompress(raw_data)
                        logging.info('QR data decompressed.')

                    # Save or display data
                    with open(output_path, 'wb') as f:
                        f.write(raw_data)
                    sg.popup(f'Data extracted from QR code to {output_path}')
                    logging.info('QR extract operation successful.')
                except Exception as e:
                    sg.popup_error(f'Error: {str(e)}')
                    logging.exception('Exception in QR extract')

    window.close()

if __name__ == '__main__':
    main()
