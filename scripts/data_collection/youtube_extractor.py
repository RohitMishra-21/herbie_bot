#!/usr/bin/env python3
"""
YouTube Transcript Scraper for Herbie Content
Extracts Herbie dialogue from Fantastic Four episodes
"""

import re
import json
from pathlib import Path
from typing import List, Dict
import requests
from urllib.parse import urlparse, parse_qs

class YouTubeHerbieExtractor:
    def __init__(self):
        self.herbie_keywords = [
            'herbie', 'h.e.r.b.i.e', 'robot', 'humanoid experimental robot',
            'b-type integrated electronics'
        ]
        
        self.output_dir = Path("data/raw/youtube_transcripts")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL"""
        parsed = urlparse(url)
        if parsed.hostname in ['www.youtube.com', 'youtube.com']:
            return parse_qs(parsed.query).get('v', [None])[0]
        elif parsed.hostname == 'youtu.be':
            return parsed.path[1:]
        return None

    def get_transcript_via_api(self, video_url: str) -> List[Dict]:
        """
        Get transcript using YouTube Transcript API (requires youtube-transcript-api)
        Install with: pip install youtube-transcript-api
        """
        herbie_lines = []
        
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            
            video_id = self.extract_video_id(video_url)
            if not video_id:
                print(f"Could not extract video ID from {video_url}")
                return herbie_lines
            
            print(f"Fetching transcript for video: {video_id}")
            
            # Get transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Look for Herbie lines
            for entry in transcript:
                text = entry['text'].lower()
                
                # Check if this line mentions Herbie or seems like robot dialogue
                if any(keyword in text for keyword in self.herbie_keywords):
                    # Try to determine if this is Herbie speaking
                    if self.is_likely_herbie_dialogue(entry['text']):
                        herbie_lines.append({
                            'dialogue': entry['text'].strip(),
                            'timestamp': entry['start'],
                            'duration': entry['duration'],
                            'source': video_url,
                            'method': 'youtube_transcript',
                            'situation': 'from_episode',
                            'emotion': self.detect_emotion(entry['text']),
                            'context': f"From YouTube video at {entry['start']}s"
                        })
            
        except ImportError:
            print("youtube-transcript-api not installed. Install with: pip install youtube-transcript-api")
        except Exception as e:
            print(f"Error getting transcript: {e}")
        
        return herbie_lines

    def is_likely_herbie_dialogue(self, text: str) -> bool:
        """Determine if text is likely Herbie speaking"""
        text_lower = text.lower()
        
        # Strong indicators this is Herbie
        herbie_indicators = [
            'herbie', 'h.e.r.b.i.e', 'compute', 'sensors', 'alert',
            'do not fear', 'fantastic four', 'mr. fantastic',
            'affirmative', 'negative', 'danger', 'threat detected'
        ]
        
        # Robot speech patterns
        robot_patterns = [
            r'\bcompute\b', r'\bsensors?\b', r'\banalyz\w*\b',
            r'\baffirmative\b', r'\bnegative\b', r'\balert\b',
            r'\bdetect\w*\b', r'\bsystem\w*\b'
        ]
        
        # Check for indicators
        indicator_count = sum(1 for indicator in herbie_indicators if indicator in text_lower)
        pattern_count = sum(1 for pattern in robot_patterns if re.search(pattern, text_lower))
        
        return indicator_count > 0 or pattern_count > 1

    def detect_emotion(self, text: str) -> str:
        """Detect emotion from dialogue text"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['alert', 'danger', 'warning', 'threat']):
            return 'urgent'
        elif any(word in text_lower for word in ['greetings', 'hello', 'pleased']):
            return 'friendly'
        elif any(word in text_lower for word in ['help', 'assist', 'save']):
            return 'helpful'
        elif any(word in text_lower for word in ['compute', 'analyze', 'calculate']):
            return 'analytical'
        else:
            return 'neutral'

    def search_youtube_videos(self) -> List[str]:
        """
        Return a list of YouTube URLs for Fantastic Four episodes with Herbie
        These are manually curated - you can expand this list
        """
        return [
            # Add actual YouTube URLs here
            # Example format:
            # "https://www.youtube.com/watch?v=VIDEO_ID_HERE",
            
            # Note: Due to copyright, many full episodes may not be available
            # Look for:
            # - Fantastic Four 1967 animated series episodes
            # - Character compilation videos
            # - Herbie-specific clips
            # - Comic convention panels discussing Herbie
        ]

    def manual_transcript_input(self) -> List[Dict]:
        """
        Helper function for manual transcript entry
        Use this if automated methods don't work
        """
        print("\n📝 Manual transcript entry mode")
        print("Paste episode transcripts and identify Herbie lines")
        print("Type 'done' when finished")
        
        herbie_lines = []
        
        while True:
            print("\nEnter a line (or 'done' to finish):")
            line = input("> ").strip()
            
            if line.lower() == 'done':
                break
            
            if line:
                print("Is this Herbie speaking? (y/n):")
                is_herbie = input("> ").lower().startswith('y')
                
                if is_herbie:
                    print("What's the situation/context?")
                    situation = input("> ").strip() or "unknown_situation"
                    
                    print("What emotion? (urgent/friendly/helpful/analytical/neutral)")
                    emotion = input("> ").strip() or "neutral"
                    
                    herbie_lines.append({
                        'dialogue': line,
                        'source': 'manual_entry',
                        'method': 'manual_transcript',
                        'situation': situation,
                        'emotion': emotion,
                        'context': 'Manually entered from episode transcript'
                    })
                    
                    print("✅ Added!")
        
        return herbie_lines

    def process_all_sources(self) -> List[Dict]:
        """Process all available sources"""
        all_quotes = []
        
        print("🎬 Starting YouTube transcript extraction...")
        
        # Method 1: Process known YouTube URLs
        youtube_urls = self.search_youtube_videos()
        
        if youtube_urls:
            for url in youtube_urls:
                print(f"Processing: {url}")
                quotes = self.get_transcript_via_api(url)
                all_quotes.extend(quotes)
                print(f"Found {len(quotes)} Herbie lines")
        else:
            print("No YouTube URLs configured. Add URLs to search_youtube_videos() method.")
        
        # Method 2: Manual entry option
        print("\nWould you like to manually enter transcript data? (y/n)")
        if input("> ").lower().startswith('y'):
            manual_quotes = self.manual_transcript_input()
            all_quotes.extend(manual_quotes)
        
        return all_quotes

    def save_transcript_data(self, quotes: List[Dict]):
        """Save extracted transcript data"""
        if not quotes:
            print("No quotes to save.")
            return
        
        # Save as JSON
        json_file = self.output_dir / "youtube_herbie_quotes.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(quotes, f, indent=2, ensure_ascii=False)
        
        # Save in template format
        template_file = self.output_dir / "youtube_quotes_template.txt"
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write("# Herbie quotes extracted from YouTube transcripts\n\n")
            
            for quote in quotes:
                f.write("---\n")
                f.write(f"SITUATION: {quote['situation']}\n")
                f.write(f"HERBIE: \"{quote['dialogue']}\"\n")
                f.write(f"EMOTION: {quote['emotion']}\n")
                f.write(f"CONTEXT: {quote['context']}\n")
                f.write(f"SOURCE: {quote['source']}\n")
                f.write("---\n\n")
        
        print(f"💾 Saved {len(quotes)} quotes to:")
        print(f"   - {json_file}")
        print(f"   - {template_file}")

def main():
    extractor = YouTubeHerbieExtractor()
    
    # Process all sources
    quotes = extractor.process_all_sources()
    
    # Save results
    extractor.save_transcript_data(quotes)
    
    print(f"\n✅ YouTube extraction complete!")
    print(f"Found {len(quotes)} Herbie quotes from transcripts")

if __name__ == "__main__":
    main()