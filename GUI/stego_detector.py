import os
import numpy as np
import logging
from PIL import Image
import wave
import cv2

class StegoDetector:
    """Class for detecting hidden data in various file formats."""
    
    def __init__(self):
        """Initialize the steganography detector."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def detect_image(self, image_path):
        """
        Detect steganography in image files (JPEG, PNG, GIF).
        
        This uses LSB analysis to detect unnatural bit patterns.
        Returns a probability between 0 and 1 that the image contains hidden data.
        """
        try:
            # Open the image file
            img = Image.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Get pixel data as numpy array
            pixels = np.array(img)
            
            # Analysis 1: Check LSB distribution
            # In natural images, the LSB should be roughly 50/50 ones and zeros
            # Steganography can disturb this balance
            lsb_0_count = np.sum(pixels & 1 == 0)
            lsb_1_count = np.sum(pixels & 1 == 1)
            total_lsbs = lsb_0_count + lsb_1_count
            
            # Calculate skew from expected 50/50 distribution
            expected = total_lsbs / 2
            skew = abs(lsb_0_count - expected) / expected
            
            # Analysis 2: Check for unusual patterns in LSB
            # In natural images, adjacent LSBs often have some correlation
            # Steganography tends to reduce this correlation
            red_lsb = pixels[:,:,0] & 1
            green_lsb = pixels[:,:,1] & 1
            blue_lsb = pixels[:,:,2] & 1
            
            # Calculate correlation between color channels
            # Lower correlation might indicate steganography
            rg_corr = np.corrcoef(red_lsb.flatten(), green_lsb.flatten())[0,1]
            rb_corr = np.corrcoef(red_lsb.flatten(), blue_lsb.flatten())[0,1]
            gb_corr = np.corrcoef(green_lsb.flatten(), blue_lsb.flatten())[0,1]
            
            # Average correlation
            avg_corr = (abs(rg_corr) + abs(rb_corr) + abs(gb_corr)) / 3
            
            # In natural images, we expect some correlation between channels
            # Lower correlation suggests possible steganography
            corr_indicator = 1 - avg_corr
            
            # Analysis 3: Sample Pair Analysis
            # This is a simplified version of sample pair analysis which looks for
            # unusual patterns in adjacent pixel values
            pairs_distortion = 0
            for c in range(3):  # For each color channel
                # Get differences between adjacent pixels
                h_diff = np.abs(pixels[:-1,:,c] - pixels[1:,:,c])
                v_diff = np.abs(pixels[:,:-1,c] - pixels[:,1:,c])
                
                # Count how many differences are odd vs even
                odd_diffs = np.sum(h_diff % 2 == 1) + np.sum(v_diff % 2 == 1)
                even_diffs = np.sum(h_diff % 2 == 0) + np.sum(v_diff % 2 == 0)
                total_diffs = odd_diffs + even_diffs
                
                # In natural images, we expect a specific ratio
                # Steganography can disturb this ratio
                if total_diffs > 0:
                    expected_odd = total_diffs * 0.5
                    diff_skew = abs(odd_diffs - expected_odd) / expected_odd
                    pairs_distortion += diff_skew
            
            pairs_distortion /= 3  # Average across channels
            
            # Combine all indicators into a final probability
            # Weights determined empirically and may need tuning
            stego_probability = (0.3 * skew + 0.4 * corr_indicator + 0.3 * pairs_distortion)
            
            # Normalize to [0, 1] range
            stego_probability = min(max(stego_probability, 0), 1)
            
            # Return additional details for reporting
            details = {
                'lsb_skew': skew,
                'channel_correlation': avg_corr,
                'pairs_distortion': pairs_distortion
            }
            
            return stego_probability, details
        
        except Exception as e:
            logging.exception(f'Error detecting steganography in image: {str(e)}')
            return 0, {'error': str(e)}
    
    def detect_audio(self, audio_path):
        """
        Detect steganography in WAV audio files.
        
        Returns a probability between 0 and 1 that the audio contains hidden data.
        """
        try:
            # Open the audio file
            with wave.open(audio_path, 'rb') as wav:
                # Get the audio parameters
                n_frames = wav.getnframes()
                n_channels = wav.getnchannels()
                sample_width = wav.getsampwidth()
                
                # Read the audio frames
                frames = wav.readframes(n_frames)
                
                # Convert to numpy array
                if sample_width == 1:  # 8-bit samples
                    audio_data = np.frombuffer(frames, dtype=np.uint8)
                elif sample_width == 2:  # 16-bit samples
                    audio_data = np.frombuffer(frames, dtype=np.int16)
                elif sample_width == 4:  # 32-bit samples
                    audio_data = np.frombuffer(frames, dtype=np.int32)
                else:
                    raise ValueError(f"Unsupported sample width: {sample_width}")
                
                # Reshape if multiple channels
                if n_channels > 1:
                    audio_data = audio_data.reshape(-1, n_channels)
                
                # Analysis 1: Check LSB distribution
                lsb_0_count = np.sum(audio_data & 1 == 0)
                lsb_1_count = np.sum(audio_data & 1 == 1)
                total_lsbs = lsb_0_count + lsb_1_count
                
                # Calculate skew from expected 50/50 distribution
                expected = total_lsbs / 2
                skew = abs(lsb_0_count - expected) / expected
                
                # Analysis 2: Spectral analysis
                # In natural audio, there should be frequency continuity
                # Steganography can disturb this continuity
                
                # Simplistic spectral analysis - just looking at the distribution
                # of first and second differences in samples
                first_diff = np.abs(np.diff(audio_data.flatten()))
                second_diff = np.abs(np.diff(first_diff))
                
                # Count odd vs even differences
                odd_first = np.sum(first_diff % 2 == 1)
                even_first = np.sum(first_diff % 2 == 0)
                odd_second = np.sum(second_diff % 2 == 1)
                even_second = np.sum(second_diff % 2 == 0)
                
                # Calculate skew from expected distributions
                if odd_first + even_first > 0:
                    expected_odd_first = (odd_first + even_first) * 0.5
                    first_skew = abs(odd_first - expected_odd_first) / expected_odd_first
                else:
                    first_skew = 0
                    
                if odd_second + even_second > 0:
                    expected_odd_second = (odd_second + even_second) * 0.5
                    second_skew = abs(odd_second - expected_odd_second) / expected_odd_second
                else:
                    second_skew = 0
                
                # Analysis 3: Adjacent sample correlation
                # In natural audio, adjacent samples are often correlated
                # Steganography can reduce this correlation
                if len(audio_data) > 1:
                    adjacent_corr = np.corrcoef(audio_data[:-1].flatten(), audio_data[1:].flatten())[0,1]
                    corr_indicator = 1 - abs(adjacent_corr)
                else:
                    corr_indicator = 0.5  # Neutral if too short to analyze
                
                # Combine all indicators into a final probability
                stego_probability = (0.3 * skew + 0.3 * (first_skew + second_skew) / 2 + 0.4 * corr_indicator)
                
                # Normalize to [0, 1] range
                stego_probability = min(max(stego_probability, 0), 1)
                
                # Return additional details for reporting
                details = {
                    'lsb_skew': skew,
                    'first_diff_skew': first_skew,
                    'second_diff_skew': second_skew,
                    'adjacent_correlation': adjacent_corr if 'adjacent_corr' in locals() else 0
                }
                
                return stego_probability, details
        
        except Exception as e:
            logging.exception(f'Error detecting steganography in audio: {str(e)}')
            return 0, {'error': str(e)}
    
    def detect_video(self, video_path):
        """
        Detect steganography in video files.
        
        Returns a probability between 0 and 1 that the video contains hidden data.
        """
        try:
            # Open the video file
            video = cv2.VideoCapture(video_path)
            
            if not video.isOpened():
                return 0, {'error': 'Could not open video file'}
            
            # Get video properties
            total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # We'll analyze a sample of frames (max 30 frames evenly distributed)
            frames_to_analyze = min(30, total_frames)
            frame_indices = np.linspace(0, total_frames - 1, frames_to_analyze, dtype=int)
            
            # Collect results for each analyzed frame
            frame_probabilities = []
            lsb_skews = []
            corr_indicators = []
            pairs_distortions = []
            
            # Analyze each selected frame
            for frame_idx in frame_indices:
                # Set frame position
                video.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                
                # Read the frame
                ret, frame = video.read()
                if not ret:
                    continue
                
                # Convert to RGB format
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Analysis 1: Check LSB distribution
                lsb_0_count = np.sum(frame_rgb & 1 == 0)
                lsb_1_count = np.sum(frame_rgb & 1 == 1)
                total_lsbs = lsb_0_count + lsb_1_count
                
                # Calculate skew from expected 50/50 distribution
                expected = total_lsbs / 2
                skew = abs(lsb_0_count - expected) / expected
                lsb_skews.append(skew)
                
                # Analysis 2: Check for unusual patterns in LSB
                red_lsb = frame_rgb[:,:,0] & 1
                green_lsb = frame_rgb[:,:,1] & 1
                blue_lsb = frame_rgb[:,:,2] & 1
                
                # Calculate correlation between color channels
                rg_corr = np.corrcoef(red_lsb.flatten(), green_lsb.flatten())[0,1]
                rb_corr = np.corrcoef(red_lsb.flatten(), blue_lsb.flatten())[0,1]
                gb_corr = np.corrcoef(green_lsb.flatten(), blue_lsb.flatten())[0,1]
                
                # Average correlation
                avg_corr = (abs(rg_corr) + abs(rb_corr) + abs(gb_corr)) / 3
                corr_indicator = 1 - avg_corr
                corr_indicators.append(corr_indicator)
                
                # Analysis 3: Sample Pair Analysis
                pairs_distortion = 0
                for c in range(3):  # For each color channel
                    h_diff = np.abs(frame_rgb[:-1,:,c] - frame_rgb[1:,:,c])
                    v_diff = np.abs(frame_rgb[:,:-1,c] - frame_rgb[:,1:,c])
                    
                    odd_diffs = np.sum(h_diff % 2 == 1) + np.sum(v_diff % 2 == 1)
                    even_diffs = np.sum(h_diff % 2 == 0) + np.sum(v_diff % 2 == 0)
                    total_diffs = odd_diffs + even_diffs
                    
                    if total_diffs > 0:
                        expected_odd = total_diffs * 0.5
                        diff_skew = abs(odd_diffs - expected_odd) / expected_odd
                        pairs_distortion += diff_skew
                
                pairs_distortion /= 3  # Average across channels
                pairs_distortions.append(pairs_distortion)
                
                # Calculate probability for this frame
                frame_prob = (0.3 * skew + 0.4 * corr_indicator + 0.3 * pairs_distortion)
                frame_prob = min(max(frame_prob, 0), 1)
                frame_probabilities.append(frame_prob)
            
            # Release the video
            video.release()
            
            # If no frames were analyzed, return 0
            if not frame_probabilities:
                return 0, {'error': 'No frames could be analyzed'}
            
            # Analysis 4: Check for frame-to-frame consistency
            # Steganography might be applied to only some frames
            frame_prob_std = np.std(frame_probabilities)
            
            # Calculate the final probability
            # Higher weight to maximum probability to detect partial steganography
            avg_prob = np.mean(frame_probabilities)
            max_prob = np.max(frame_probabilities)
            
            stego_probability = 0.6 * max_prob + 0.3 * avg_prob + 0.1 * frame_prob_std
            stego_probability = min(max(stego_probability, 0), 1)
            
            # Return additional details for reporting
            details = {
                'avg_lsb_skew': np.mean(lsb_skews),
                'avg_channel_correlation': 1 - np.mean(corr_indicators),
                'avg_pairs_distortion': np.mean(pairs_distortions),
                'frame_probability_std': frame_prob_std,
                'frames_analyzed': len(frame_probabilities)
            }
            
            return stego_probability, details
        
        except Exception as e:
            logging.exception(f'Error detecting steganography in video: {str(e)}')
            return 0, {'error': str(e)}
    
    def detect_pdf(self, pdf_path):
        """
        Detect steganography in PDF files.
        
        Returns a probability between 0 and 1 that the PDF contains hidden data.
        """
        try:
            import PyPDF2
            
            # Open the PDF file
            with open(pdf_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                
                # Check for metadata that might contain steganographic data
                metadata = pdf_reader.metadata
                has_suspicious_metadata = False
                
                # Check for custom metadata fields that are commonly used for steganography
                suspicious_keys = ['/StegData', '/EmbeddedData', '/HiddenContent', '/UserData']
                for key in suspicious_keys:
                    if metadata and key in metadata:
                        has_suspicious_metadata = True
                
                # Check for JavaScript or embedded files which can be used to hide data
                has_js = False
                has_embedded_files = False
                
                # Check for embedded files
                if '/EmbeddedFiles' in pdf_reader.trailer.get('/Root', {}):
                    has_embedded_files = True
                
                # Check for JavaScript
                for i in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[i]
                    if '/JavaScript' in page or '/JS' in page:
                        has_js = True
                
                # Analyze text extraction to detect anomalies
                text_anomalies = 0
                for i in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[i]
                    # Try to extract text - anomalies might occur with steganographic content
                    try:
                        text = page.extract_text()
                        # Check for unusual characters that might indicate hidden data
                        unusual_chars = sum(1 for c in text if ord(c) > 127)
                        if unusual_chars > len(text) * 0.1:  # More than 10% unusual characters
                            text_anomalies += 1
                    except:
                        text_anomalies += 1
                
                # Calculate probability based on found indicators
                stego_probability = 0
                
                if has_suspicious_metadata:
                    stego_probability += 0.5  # Strong indicator
                
                if has_embedded_files:
                    stego_probability += 0.3  # Moderate indicator
                
                if has_js:
                    stego_probability += 0.2  # Weak indicator
                
                if text_anomalies > 0:
                    text_anomaly_ratio = min(text_anomalies / len(pdf_reader.pages), 1.0)
                    stego_probability += 0.3 * text_anomaly_ratio
                
                # Normalize to [0, 1] range
                stego_probability = min(max(stego_probability, 0), 1)
                
                # Return additional details for reporting
                details = {
                    'suspicious_metadata': has_suspicious_metadata,
                    'embedded_files': has_embedded_files,
                    'javascript': has_js,
                    'text_anomalies': text_anomalies,
                    'total_pages': len(pdf_reader.pages)
                }
                
                return stego_probability, details
        
        except Exception as e:
            logging.exception(f'Error detecting steganography in PDF: {str(e)}')
            return 0, {'error': str(e)}
    
    def detect_file(self, file_path):
        """
        Detect steganography in a file based on its format.
        
        Returns a probability between 0 and 1 that the file contains hidden data,
        along with detailed analysis information.
        """
        # Determine file type based on extension
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
            # Image file
            probability, details = self.detect_image(file_path)
            file_type = 'Image'
        
        elif file_ext == '.wav':
            # Audio file
            probability, details = self.detect_audio(file_path)
            file_type = 'Audio'
        
        elif file_ext in ['.mp4', '.avi', '.mov']:
            # Video file
            probability, details = self.detect_video(file_path)
            file_type = 'Video'
        
        elif file_ext == '.pdf':
            # PDF file
            probability, details = self.detect_pdf(file_path)
            file_type = 'PDF'
        
        else:
            # Unsupported file type
            return 0, {'error': f'Unsupported file type: {file_ext}'}, 'Unknown'
        
        # Interpretation of the probability
        if probability < 0.3:
            interpretation = 'Low probability of hidden data'
        elif probability < 0.7:
            interpretation = 'Medium probability of hidden data'
        else:
            interpretation = 'High probability of hidden data'
        
        return probability, details, file_type, interpretation
