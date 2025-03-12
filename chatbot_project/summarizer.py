import PyPDF2
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from youtube_transcript_api import YouTubeTranscriptApi
import re
from transformers import pipeline
<<<<<<< HEAD
=======
from pytube import YouTube  
>>>>>>> 1f5b2fea555c7d390e3e0bd1e31c90e33d1f0ba4

class Summarizer:
    def __init__(self):
        # Initialize the transformer-based summarization pipeline
        try:
            self.transformer_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            self.use_transformers = True
        except Exception as e:
            print(f"Warning: Could not initialize transformer model: {str(e)}")
            print("Falling back to LSA summarizer")
            self.use_transformers = False

    def summarize_text(self, text, sentences_count=5, max_length=200):
        # Try transformer-based summarization first if available
        if self.use_transformers and len(text.split()) > 40:
            try:
                # Clean text for better summarization
                cleaned_text = text.replace('\n', ' ').strip()
                cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
                
                # Truncate if needed (BART has a limit of ~1024 tokens)
                if len(cleaned_text) > 1000:
                    cleaned_text = cleaned_text[:1000]
                
                # Generate summary using transformer model
                summary = self.transformer_summarizer(cleaned_text, 
                                                     max_length=max_length,
                                                     min_length=30, 
                                                     do_sample=False)[0]['summary_text']
                return summary
            except Exception as e:
                print(f"Transformer summarization failed: {str(e)}")
                print("Falling back to LSA summarizer")
        
        # Fall back to LSA summarization
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentences_count)
        return " ".join([str(sentence) for sentence in summary])

    def summarize_file(self, file_path):
        try:
            if file_path.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read()
                # Get standard summary for text files
                summary = self.summarize_text(text)
            elif file_path.endswith(".pdf"):
                text = self._extract_pdf_text(file_path)
                if not text:
                    return "Could not extract text from PDF file."
                
                # Calculate appropriate summary length based on PDF content size
                word_count = len(text.split())
                print(f"PDF word count: {word_count}")
                
                # Adjust summary parameters based on content length
                if word_count > 1000:
                    max_length = 400  # Longer summary for lengthy PDFs
                    sentences_count = 15
                elif word_count > 500:
                    max_length = 300  # Medium length summary
                    sentences_count = 12
                else:
                    max_length = 250  # Standard summary for shorter PDFs
                    sentences_count = 8
                    
                # Get custom summary for PDFs
                summary = self.summarize_text(text, sentences_count=sentences_count, max_length=max_length)
            else:
                return "Unsupported file type. Use .txt or .pdf."
                
            # Add the emoji and formatting for all successful summaries
            return f"📝 Summary:\n\n{summary}"
        except Exception as e:
            return f"Error: {str(e)}"

    def _extract_pdf_text(self, file_path):
        """Extract and clean text from PDF file with improved handling."""
        try:
            with open(file_path, "rb") as file:
                pdf = PyPDF2.PdfReader(file)
                num_pages = len(pdf.pages)
                
                # Handle empty PDF
                if num_pages == 0:
                    return ""
                    
                all_text = []
                
                # Extract text from each page with error handling
                for i in range(num_pages):
                    try:
                        page = pdf.pages[i]
                        text = page.extract_text()
                        
                        # Skip empty pages
                        if text and text.strip():
                            # Clean the text
                            text = text.replace('\n\n', ' ').replace('\n', ' ')
                            text = re.sub(r'\s+', ' ', text)
                            all_text.append(text)
                    except Exception as e:
                        print(f"Error extracting text from page {i+1}: {str(e)}")
                        continue
                
                combined_text = " ".join(all_text)
                
                # Additional cleaning
                combined_text = re.sub(r'[^\w\s.,;:!?()\[\]{}\-"\'`]', '', combined_text)  # Remove special characters
                combined_text = re.sub(r'\s+', ' ', combined_text)  # Normalize whitespace
                
                # Remove page numbers and common headers/footers
                combined_text = re.sub(r'\b\d+\b\s+of\s+\b\d+\b', '', combined_text)  # "X of Y" page indicators
                combined_text = re.sub(r'Page\s+\d+', '', combined_text)  # "Page X" indicators
                
                return combined_text.strip()
                
        except Exception as e:
            print(f"PDF extraction failed: {str(e)}")
            return ""

    def summarize_video(self, video_url):
        """Summarize a YouTube video with more detailed output."""
        try:
            video_id = self._extract_video_id(video_url)
            if not video_id:
                return "Invalid YouTube URL"
                        
            # Fetch transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            print(f"Transcript segments: {len(transcript_list)}")
            if not transcript_list:
                return "No transcript available for this video."
                
            # Combine transcript text and clean it
            transcript_text = ' '.join([item['text'] for item in transcript_list])
            
            # Process transcript for better results
            transcript_text = transcript_text.replace('\n', ' ').strip()
            transcript_text = re.sub(r'\s+', ' ', transcript_text)
            
            if len(transcript_text.split()) < 20:
                return "Video transcript is too short to summarize."
            
            # Determine appropriate max length based on transcript size - INCREASED FOR LONGER SUMMARIES
            transcript_word_count = len(transcript_text.split())
            print(f"Transcript word count: {transcript_word_count}")
            
            if transcript_word_count > 1000:
                max_length = 400  # Much longer summary for longer videos
                sentences_count = 15
            elif transcript_word_count > 500:
                max_length = 300  # Longer summary for medium videos
                sentences_count = 12
            else:
                max_length = 250  # Standard summary for shorter videos
                sentences_count = 8
            
            # Use the enhanced summarize_text method with increased parameters
            if self.use_transformers and transcript_word_count > 40:
                try:
                    cleaned_text = transcript_text.replace('\n', ' ').strip()
                    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
                    
                    # Handle longer transcripts better by splitting if needed
                    if len(cleaned_text) > 1000:
                        first_chunk = cleaned_text[:1000]
                        # Get transformer summary with higher min_length
                        summary = self.transformer_summarizer(
                            first_chunk,
                            max_length=max_length,
                            min_length=100,  # Increased from 30
                            do_sample=False,
                            num_beams=4     # Better quality generation
                        )[0]['summary_text']
                    else:
                        summary = self.transformer_summarizer(
                            cleaned_text,
                            max_length=max_length,
                            min_length=100,  # Increased from 30
                            do_sample=False,
                            num_beams=4     # Better quality generation
                        )[0]['summary_text']
                    
                    # If summary is too short, fall back to LSA
                    if len(summary.split()) < 30:
                        raise Exception("Transformer summary too short")
                        
                    return f"📝 Summary:\n\n{summary}"
                except Exception as e:
                    print(f"Transformer summarization failed: {str(e)}")
                    print("Falling back to LSA summarizer")
            
            # LSA summarization with increased sentences
            parser = PlaintextParser.from_string(transcript_text, Tokenizer("english"))
            summarizer = LsaSummarizer()
            summary = summarizer(parser.document, sentences_count)
            summary_text = " ".join([str(sentence) for sentence in summary])
            
            if not summary_text or len(summary_text) < 50:
                return "Could not generate a meaningful summary for this video."
                
            return f"📝 Summary:\n\n{summary_text}"
            
        except Exception as e:
            if "TranscriptsDisabled" in str(e):
                return "This video doesn't have available transcripts."
            return f"Error summarizing video: {str(e)}"

    def _extract_video_id(self, url):
        """Extract YouTube video ID from URL."""
        patterns = [
            r'(?:v=|/v/|youtu\.be/|/embed/)([^&?/]+)',
            r'youtube.com/watch\?v=([^&?/]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
