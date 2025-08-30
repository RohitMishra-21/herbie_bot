#!/usr/bin/env python3
"""
API-Based Herbie Data Collection
Uses various APIs to gather Herbie character data
"""

import requests
import json
import time
from pathlib import Path
from typing import List, Dict, Optional
import os
from urllib.parse import quote

class APIDataCollector:
    def __init__(self):
        self.output_dir = Path("data/raw/api_collected")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Rate limiting
        self.request_delay = 1  # seconds between requests
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'HerbieBot/1.0 (Educational Project)'
        })

    def search_marvel_api(self, api_key: Optional[str] = None) -> List[Dict]:
        """
        Search Marvel's official API for Herbie data
        Get API key from: https://developer.marvel.com/
        """
        quotes = []
        
        if not api_key:
            print("⚠️  Marvel API key not provided. Skipping Marvel API search.")
            print("   Get a free API key from: https://developer.marvel.com/")
            return quotes
        
        try:
            # Search for Herbie character
            url = "https://gateway.marvel.com/v1/public/characters"
            params = {
                'apikey': api_key,
                'name': 'H.E.R.B.I.E.',
                'limit': 10
            }
            
            print("🔍 Searching Marvel API for Herbie...")
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            for character in data.get('data', {}).get('results', []):
                name = character.get('name', '')
                description = character.get('description', '')
                
                if 'herbie' in name.lower() or 'h.e.r.b.i.e' in name.lower():
                    # Extract any quoted material from description
                    if description:
                        quotes.append({
                            'dialogue': description,
                            'source': 'Marvel Official API',
                            'method': 'marvel_api',
                            'situation': 'character_description',
                            'emotion': 'informational',
                            'context': f'Official Marvel character description for {name}'
                        })
            
            time.sleep(self.request_delay)
            
        except Exception as e:
            print(f"Error with Marvel API: {e}")
        
        return quotes

    def search_comic_vine_api(self, api_key: Optional[str] = None) -> List[Dict]:
        """
        Search Comic Vine API for Herbie data
        Get API key from: https://comicvine.gamespot.com/api/
        """
        quotes = []
        
        if not api_key:
            print("⚠️  Comic Vine API key not provided. Skipping Comic Vine search.")
            print("   Get a free API key from: https://comicvine.gamespot.com/api/")
            return quotes
        
        try:
            # Search for Herbie character
            url = "https://comicvine.gamespot.com/api/search/"
            params = {
                'api_key': api_key,
                'query': 'H.E.R.B.I.E. Herbie',
                'resources': 'character',
                'format': 'json',
                'limit': 10
            }
            
            print("🔍 Searching Comic Vine API...")
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            for result in data.get('results', []):
                name = result.get('name', '')
                description = result.get('description', '')
                deck = result.get('deck', '')  # Short description
                
                if any(keyword in name.lower() for keyword in ['herbie', 'h.e.r.b.i.e']):
                    # Process description and deck for quotes
                    for text_field, field_name in [(description, 'description'), (deck, 'deck')]:
                        if text_field:
                            # Look for quoted dialogue
                            import re
                            quoted_parts = re.findall(r'"([^"]+)"', text_field)
                            for quote in quoted_parts:
                                if len(quote) > 10:
                                    quotes.append({
                                        'dialogue': quote.strip(),
                                        'source': f"Comic Vine - {result.get('site_detail_url', 'Unknown')}",
                                        'method': 'comic_vine_api',
                                        'situation': f'from_{field_name}',
                                        'emotion': 'unknown',
                                        'context': f'From Comic Vine {field_name} for {name}'
                                    })
                            
                            # Also add the full description as context if it mentions dialogue
                            if any(word in text_field.lower() for word in ['said', 'says', 'speaks', 'tells']):
                                quotes.append({
                                    'dialogue': text_field.strip(),
                                    'source': f"Comic Vine - {result.get('site_detail_url', 'Unknown')}",
                                    'method': 'comic_vine_api',
                                    'situation': 'character_info',
                                    'emotion': 'informational',
                                    'context': f'Character information from Comic Vine'
                                })
            
            time.sleep(self.request_delay)
            
        except Exception as e:
            print(f"Error with Comic Vine API: {e}")
        
        return quotes

    def search_open_library(self) -> List[Dict]:
        """
        Search Open Library for Fantastic Four books/comics
        No API key required
        """
        quotes = []
        
        try:
            print("🔍 Searching Open Library...")
            
            # Search for Fantastic Four related books
            url = "https://openlibrary.org/search.json"
            params = {
                'q': 'fantastic four herbie',
                'limit': 20
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            for book in data.get('docs', []):
                title = book.get('title', '')
                subtitle = book.get('subtitle', '')
                first_sentence = book.get('first_sentence', [])
                
                # Look for Herbie mentions
                combined_text = f"{title} {subtitle} {' '.join(first_sentence)}"
                
                if 'herbie' in combined_text.lower():
                    # Extract any useful information
                    for sentence in first_sentence:
                        if 'herbie' in sentence.lower() and len(sentence) > 15:
                            quotes.append({
                                'dialogue': sentence.strip(),
                                'source': f"Open Library - {title}",
                                'method': 'open_library',
                                'situation': 'from_book_description',
                                'emotion': 'unknown',
                                'context': f'From book description: {title}'
                            })
            
            time.sleep(self.request_delay)
            
        except Exception as e:
            print(f"Error with Open Library: {e}")
        
        return quotes

    def search_wikiquote(self) -> List[Dict]:
        """
        Search Wikiquote for character quotes
        Uses Wikipedia/Wikiquote API
        """
        quotes = []
        
        try:
            print("🔍 Searching Wikiquote...")
            
            # Search Wikiquote for Fantastic Four
            url = "https://en.wikiquote.org/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': 'Fantastic Four Herbie',
                'srlimit': 10
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            for result in data.get('query', {}).get('search', []):
                title = result.get('title', '')
                snippet = result.get('snippet', '')
                
                if 'herbie' in snippet.lower():
                    # Get page content
                    content_params = {
                        'action': 'query',
                        'format': 'json',
                        'titles': title,
                        'prop': 'extracts',
                        'exintro': True,
                        'explaintext': True
                    }
                    
                    content_response = self.session.get(url, params=content_params)
                    content_data = content_response.json()
                    
                    pages = content_data.get('query', {}).get('pages', {})
                    for page_id, page_data in pages.items():
                        extract = page_data.get('extract', '')
                        
                        # Look for Herbie quotes
                        import re
                        lines = extract.split('\n')
                        for line in lines:
                            if 'herbie' in line.lower() and '"' in line:
                                quoted_parts = re.findall(r'"([^"]+)"', line)
                                for quote in quoted_parts:
                                    if len(quote) > 10:
                                        quotes.append({
                                            'dialogue': quote.strip(),
                                            'source': f"Wikiquote - {title}",
                                            'method': 'wikiquote',
                                            'situation': 'from_quote_collection',
                                            'emotion': 'unknown',
                                            'context': f'From Wikiquote page: {title}'
                                        })
                    
                    time.sleep(self.request_delay)
            
        except Exception as e:
            print(f"Error with Wikiquote: {e}")
        
        return quotes


    def collect_from_all_apis(self, api_keys: Dict[str, str] = None) -> List[Dict]:
        """
        Collect data from all available APIs
        
        api_keys format:
        {
            'marvel': 'b89e800fa339a012ff4df7cd7b8cf9ad4d6c1f84',
            'comic_vine': 'a6391378ef50a67d4da35c9d428f751971015803'
        }
        """
        if api_keys is None:
            api_keys = {}
        
        all_quotes = []
        
        print("🚀 Starting API-based data collection...")
        
        # Marvel API
        marvel_quotes = self.search_marvel_api(api_keys.get('marvel'))
        all_quotes.extend(marvel_quotes)
        print(f"Marvel API: {len(marvel_quotes)} quotes")
        
        # Comic Vine API
        comic_vine_quotes = self.search_comic_vine_api(api_keys.get('comic_vine'))
        all_quotes.extend(comic_vine_quotes)
        print(f"Comic Vine API: {len(comic_vine_quotes)} quotes")
        
        # Open Library (no key needed)
        open_lib_quotes = self.search_open_library()
        all_quotes.extend(open_lib_quotes)
        print(f"Open Library: {len(open_lib_quotes)} quotes")
        
        # Wikiquote (no key needed)
        wikiquote_quotes = self.search_wikiquote()
        all_quotes.extend(wikiquote_quotes)
        print(f"Wikiquote: {len(wikiquote_quotes)} quotes")
        
        
        return all_quotes

    def save_api_data(self, quotes: List[Dict]):
        """Save API-collected data"""
        if not quotes:
            print("No quotes collected from APIs.")
            return
        
        # Save as JSON
        json_file = self.output_dir / "api_herbie_quotes.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(quotes, f, indent=2, ensure_ascii=False)
        
        # Save in template format
        template_file = self.output_dir / "api_quotes_template.txt"
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write("# Herbie quotes collected from various APIs\n\n")
            
            for quote in quotes:
                f.write("---\n")
                f.write(f"SITUATION: {quote['situation']}\n")
                f.write(f"HERBIE: \"{quote['dialogue']}\"\n")
                f.write(f"EMOTION: {quote['emotion']}\n")
                f.write(f"CONTEXT: {quote['context']}\n")
                f.write(f"SOURCE: {quote['source']}\n")
                f.write("---\n\n")
        
        print(f"💾 Saved {len(quotes)} API quotes to:")
        print(f"   - {json_file}")
        print(f"   - {template_file}")

def main():
    """Main function with API key configuration"""
    collector = APIDataCollector()
    
    # Configure your API keys here
    api_keys = {
        # Get these from the respective services
        'marvel': 'b89e800fa339a012ff4df7cd7b8cf9ad4d6c1f84',
        'comic_vine': 'a6391378ef50a67d4da35c9d428f751971015803'
    }
    
    # You can also load API keys from environment variables
    api_keys.update({
        'marvel': os.getenv('MARVEL_API_KEY'),
        'comic_vine': os.getenv('COMIC_VINE_API_KEY')
    })
    
    # Remove None values
    api_keys = {k: v for k, v in api_keys.items() if v}
    
    if not api_keys:
        print("⚠️  No API keys configured.")
        print("   Add your API keys to the script or set environment variables:")
        print("   - MARVEL_API_KEY")
        print("   - COMIC_VINE_API_KEY")
        print("\n   Some sources (Open Library, Wikiquote) don't require keys.")
    
    # Collect from all APIs
    quotes = collector.collect_from_all_apis(api_keys)
    
    # Save results
    collector.save_api_data(quotes)
    
    print(f"\n✅ API collection complete!")
    print(f"📊 Total quotes from APIs: {len(quotes)}")

if __name__ == "__main__":
    main()