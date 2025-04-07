import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

class BatchProcessor:
    """Class for handling batch processing of multiple files."""
    
    def __init__(self, embed_extract, crypto=None, compressor=None):
        """Initialize with necessary components."""
        self.embed_extract = embed_extract
        self.crypto = crypto
        self.compressor = compressor
        self.progress_callback = None
        
    def set_progress_callback(self, callback):
        """Set a callback function to report progress."""
        self.progress_callback = callback
    
    def process_batch_embed(self, file_format, carrier_files, payload_data, encrypt=False, compress=False, max_workers=4):
        """
        Process multiple carrier files for embedding.
        
        Args:
            file_format (str): The format of the carrier files
            carrier_files (list): List of paths to carrier files
            payload_data (bytes): The data to embed in each carrier file
            encrypt (bool): Whether to encrypt the data
            compress (bool): Whether to compress the data
            max_workers (int): Maximum number of concurrent workers
            
        Returns:
            dict: A dictionary mapping carrier files to success/failure status
        """
        # Prepare the data
        data = payload_data
        
        if compress and self.compressor:
            data = self.compressor.compress(data)
            logging.info('Data compressed for batch embedding.')
        
        if encrypt and self.crypto:
            data = self.crypto.encrypt(data)
            logging.info('Data encrypted for batch embedding.')
        
        results = {}
        completed = 0
        total = len(carrier_files)
        
        # Process files in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_file = {}
            
            for carrier_path in carrier_files:
                if file_format in ['jpeg', 'png', 'gif']:
                    future = executor.submit(self.embed_extract.embed_binary, carrier_path, data, file_format)
                elif file_format == 'pdf':
                    future = executor.submit(self.embed_extract.embed_pdf, carrier_path, data)
                elif file_format == 'wav':
                    future = executor.submit(self.embed_extract.embed_audio, carrier_path, data)
                elif file_format == 'mp4':
                    future = executor.submit(self.embed_extract.embed_video, carrier_path, data)
                else:
                    results[carrier_path] = False
                    continue
                
                future_to_file[future] = carrier_path
            
            # Process results as they complete
            for future in as_completed(future_to_file):
                carrier_path = future_to_file[future]
                try:
                    success = future.result()
                    results[carrier_path] = success
                except Exception as e:
                    logging.exception(f'Error processing {carrier_path}: {str(e)}')
                    results[carrier_path] = False
                
                completed += 1
                if self.progress_callback:
                    self.progress_callback(completed, total)
        
        return results
    
    def process_batch_extract(self, file_format, carrier_files, output_dir, encrypt=False, compress=False, max_workers=4):
        """
        Process multiple carrier files for extraction.
        
        Args:
            file_format (str): The format of the carrier files
            carrier_files (list): List of paths to carrier files
            output_dir (str): Directory to save extracted files
            encrypt (bool): Whether the data is encrypted
            compress (bool): Whether the data is compressed
            max_workers (int): Maximum number of concurrent workers
            
        Returns:
            dict: A dictionary mapping carrier files to success/failure status
        """
        results = {}
        completed = 0
        total = len(carrier_files)
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Process files in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_file = {}
            
            for carrier_path in carrier_files:
                if file_format in ['jpeg', 'png', 'gif']:
                    future = executor.submit(self._extract_and_save, 
                                           self.embed_extract.extract_binary, 
                                           carrier_path, 
                                           output_dir, 
                                           encrypt, 
                                           compress,
                                           file_format=file_format)
                elif file_format == 'pdf':
                    future = executor.submit(self._extract_and_save, 
                                           self.embed_extract.extract_pdf, 
                                           carrier_path, 
                                           output_dir, 
                                           encrypt, 
                                           compress)
                elif file_format == 'wav':
                    future = executor.submit(self._extract_and_save, 
                                           self.embed_extract.extract_audio, 
                                           carrier_path, 
                                           output_dir, 
                                           encrypt, 
                                           compress)
                elif file_format == 'mp4':
                    future = executor.submit(self._extract_and_save, 
                                           self.embed_extract.extract_video, 
                                           carrier_path, 
                                           output_dir, 
                                           encrypt, 
                                           compress)
                else:
                    results[carrier_path] = False
                    continue
                
                future_to_file[future] = carrier_path
            
            # Process results as they complete
            for future in as_completed(future_to_file):
                carrier_path = future_to_file[future]
                try:
                    success = future.result()
                    results[carrier_path] = success
                except Exception as e:
                    logging.exception(f'Error processing {carrier_path}: {str(e)}')
                    results[carrier_path] = False
                
                completed += 1
                if self.progress_callback:
                    self.progress_callback(completed, total)
        
        return results
    
    def _extract_and_save(self, extract_func, carrier_path, output_dir, encrypt, compress, **kwargs):
        """
        Extract data from a carrier file and save it.
        
        Args:
            extract_func (callable): The extraction function to use
            carrier_path (str): Path to the carrier file
            output_dir (str): Directory to save the extracted file
            encrypt (bool): Whether the data is encrypted
            compress (bool): Whether the data is compressed
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Extract the data
            if 'file_format' in kwargs:
                data = extract_func(carrier_path, kwargs['file_format'])
            else:
                data = extract_func(carrier_path)
            
            if data is None:
                return False
            
            # Decrypt if needed
            if encrypt and self.crypto:
                try:
                    data = self.crypto.decrypt(data)
                except Exception as e:
                    logging.error(f'Decryption error: {str(e)}')
                    return False
            
            # Decompress if needed
            if compress and self.compressor:
                try:
                    data = self.compressor.decompress(data)
                except Exception as e:
                    logging.error(f'Decompression error: {str(e)}')
                    return False
            
            # Generate output filename based on carrier filename
            carrier_basename = os.path.basename(carrier_path)
            carrier_name, _ = os.path.splitext(carrier_basename)
            output_path = os.path.join(output_dir, f"{carrier_name}_extracted.bin")
            
            # Save the extracted data
            with open(output_path, 'wb') as f:
                f.write(data)
            
            return True
        
        except Exception as e:
            logging.exception(f'Error extracting and saving: {str(e)}')
            return False
