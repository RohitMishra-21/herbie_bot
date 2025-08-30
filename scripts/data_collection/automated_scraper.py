#!/usr/bin/env python3
"""
Automated Herbie Data Collection Suite
Multiple approaches to gather Herbie dialogue data
"""

import requests
import json
import time
import re
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
from typing import List, Dict
import os
from urllib.parse import urljoin, urlparse

class HerbieDataCollector:
    def __init__(self):
        self.base_dir = Path("data/raw/automated")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Common headers to avoid being blocked
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def scrape_marvel_wiki(self) -> List[Dict]:
        """Scrape Herbie data from Marvel Wiki/Fandom"""
        quotes = []
        
        urls = [
            "https://marvel.fandom.com/wiki/H.E.R.B.I.E.",
            "https://marvel.fandom.com/wiki/Humanoid_Experimental_Robot,_B-type,_Integrated_Electronics_(Earth-616)",
            "https://marvel.fandom.com/wiki/H.E.R.B.I.E._(Earth-8107)"
        ]
        
        for url in urls:
            try:
                print(f"Scraping: {url}")
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for quotes in various sections
                quote_patterns = [
                    r'"([^"]*Herbie[^"]*)"',
                    r'"([^"]*H\.E\.R\.B\.I\.E[^"]*)"',
                    r'says?\s*"([^"]+)"',  # Pattern for "Herbie says..."
                ]
                
                text_content = soup.get_text()
                
                for pattern in quote_patterns:
                    matches = re.findall(pattern, text_content, re.IGNORECASE)
                    for match in matches:
                        if len(match) > 10 and 'herbie' in match.lower():
                            quotes.append({
                                'dialogue': match.strip(),
                                'source': url,
                                'method': 'wiki_scrape',
                                'situation': 'extracted_from_wiki',
                                'emotion': 'unknown',
                                'context': 'From Marvel Wiki page'
                            })
                
                time.sleep(2)  # Be respectful to the server
                
            except Exception as e:
                print(f"Error scraping {url}: {e}")
        
        return quotes

    def scrape_comic_databases(self) -> List[Dict]:
        """Scrape comic databases for Herbie appearances"""
        quotes = []
        
        # Comic database URLs (these are examples - replace with actual accessible ones)
        comic_db_urls = [
            "https://comicvine.gamespot.com/herbie/4005-12804/",
            # Add more comic database URLs here
        ]
        
        for url in comic_db_urls:
            try:
                print(f"Scraping comic database: {url}")
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for dialogue or quotes sections
                dialogue_sections = soup.find_all(['p', 'div', 'span'], 
                                                string=re.compile(r'herbie|H\.E\.R\.B\.I\.E', re.I))
                
                for section in dialogue_sections:
                    text = section.get_text().strip()
                    if '"' in text and len(text) > 20:
                        # Extract quoted text
                        quoted_parts = re.findall(r'"([^"]+)"', text)
                        for quote in quoted_parts:
                            if 'herbie' in quote.lower() or len(quote) > 15:
                                quotes.append({
                                    'dialogue': quote.strip(),
                                    'source': url,
                                    'method': 'comic_db_scrape',
                                    'situation': 'from_comic_database',
                                    'emotion': 'unknown',
                                    'context': 'Extracted from comic database'
                                })
                
                time.sleep(3)  # Be respectful
                
            except Exception as e:
                print(f"Error scraping {url}: {e}")
        
        return quotes

    def generate_synthetic_quotes(self) -> List[Dict]:
        """Generate synthetic Herbie quotes based on patterns"""
        
        # Herbie speech patterns and templates
        herbie_templates = [
            "Herbie computes that {situation}!",
            "Alert! Alert! Herbie's sensors detect {danger}!",
            "Do not fear, {character}! Herbie will {action}!",
            "Herbie is {emotion} to {action}!",
            "Greetings! Herbie is {description}!",
            "Herbie's analysis indicates {analysis}!",
            "Affirmative! Herbie will {action} immediately!",
            "Herbie does not compute {confusion}, but Herbie will help!",
            "Danger! {threat} approaching! Herbie recommends {action}!",
            "Herbie's mission is to {mission}!"
        ]
        
        # Fill-in options
        fill_options = {
            'situation': ['danger approaches', 'assistance is required', 'the Fantastic Four need help'],
            'danger': ['hostile entities', 'unknown threats', 'suspicious activity'],
            'character': ['Mr. Fantastic', 'Invisible Woman', 'Human Torch', 'The Thing', 'citizens'],
            'action': ['assist you', 'save the day', 'protect the innocent', 'analyze the threat'],
            'emotion': ['pleased', 'programmed', 'determined', 'ready'],
            'description': ['H.E.R.B.I.E., your faithful assistant', 'ready to serve', 'online and operational'],
            'analysis': ['success probability is high', 'all systems are functioning', 'the threat level is moderate'],
            'confusion': ['human emotions', 'illogical behavior', 'this strange phenomenon'],
            'threat': ['Doom-bots', 'alien invaders', 'unknown entities'],
            'mission': ['protect the Fantastic Four', 'serve humanity', 'maintain peace']
        }
        
        synthetic_quotes = []
        
        for template in herbie_templates:
            # Find placeholders in template
            placeholders = re.findall(r'{(\w+)}', template)
            
            # Generate multiple variations
            for i in range(3):  # 3 variations per template
                filled_template = template
                situation = "generated_dialogue"
                context = "Synthetic quote based on Herbie speech patterns"
                
                for placeholder in placeholders:
                    if placeholder in fill_options:
                        import random
                        replacement = random.choice(fill_options[placeholder])
                        filled_template = filled_template.replace(f'{{{placeholder}}}', replacement)
                        
                        # Determine situation and emotion based on content
                        if 'alert' in filled_template.lower() or 'danger' in filled_template.lower():
                            situation = 'warning_of_danger'
                            emotion = 'urgent'
                        elif 'greetings' in filled_template.lower():
                            situation = 'greeting'
                            emotion = 'friendly'
                        elif 'assist' in filled_template.lower() or 'help' in filled_template.lower():
                            situation = 'offering_help'
                            emotion = 'helpful'
                        else:
                            emotion = 'determined'
                
                synthetic_quotes.append({
                    'dialogue': filled_template,
                    'source': 'synthetic_generation',
                    'method': 'template_based',
                    'situation': situation,
                    'emotion': emotion,
                    'context': context
                })
        
        return synthetic_quotes

    def search_internet_archive(self) -> List[Dict]:
        """Search Internet Archive for Fantastic Four content"""
        quotes = []
        
        # Internet Archive API search
        search_url = "https://archive.org/advancedsearch.php"
        
        search_params = {
            'q': 'Fantastic Four Herbie',
            'fl': 'identifier,title,description',
            'output': 'json',
            'rows': 50
        }
        
        try:
            print("Searching Internet Archive...")
            response = self.session.get(search_url, params=search_params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            for item in data.get('response', {}).get('docs', []):
                title = item.get('title', '')
                description = item.get('description', '')
                identifier = item.get('identifier', '')
                
                # Look for Herbie mentions in descriptions
                combined_text = f"{title} {description}"
                if 'herbie' in combined_text.lower():
                    # Try to extract any quoted material
                    quoted_parts = re.findall(r'"([^"]+)"', combined_text)
                    for quote in quoted_parts:
                        if len(quote) > 10:
                            quotes.append({
                                'dialogue': quote.strip(),
                                'source': f"https://archive.org/details/{identifier}",
                                'method': 'internet_archive',
                                'situation': 'from_archive_description',
                                'emotion': 'unknown',
                                'context': f'From Internet Archive item: {title}'
                            })
            
            time.sleep(2)
            
        except Exception as e:
            print(f"Error searching Internet Archive: {e}")
        
        return quotes

    def collect_all_data(self) -> List[Dict]:
        """Run all collection methods"""
        all_quotes = []
        
        print("🤖 Starting automated Herbie data collection...")
        
        # Method 1: Marvel Wiki scraping
        print("\n1. Scraping Marvel Wiki...")
        wiki_quotes = self.scrape_marvel_wiki()
        all_quotes.extend(wiki_quotes)
        print(f"   Collected {len(wiki_quotes)} quotes from wikis")
        
        # Method 2: Comic databases
        print("\n2. Scraping comic databases...")
        comic_quotes = self.scrape_comic_databases()
        all_quotes.extend(comic_quotes)
        print(f"   Collected {len(comic_quotes)} quotes from comic databases")
        
        # Method 3: Internet Archive
        print("\n3. Searching Internet Archive...")
        archive_quotes = self.search_internet_archive()
        all_quotes.extend(archive_quotes)
        print(f"   Collected {len(archive_quotes)} quotes from Internet Archive")
        
        # Method 4: Generate synthetic quotes
        print("\n4. Generating synthetic quotes...")
        synthetic_quotes = self.generate_synthetic_quotes()
        all_quotes.extend(synthetic_quotes)
        print(f"   Generated {len(synthetic_quotes)} synthetic quotes")
        
        return all_quotes

    def clean_and_deduplicate(self, quotes: List[Dict]) -> List[Dict]:
        """Clean and remove duplicate quotes"""
        print("\n🧹 Cleaning and deduplicating data...")
        
        cleaned_quotes = []
        seen_dialogues = set()
        
        for quote in quotes:
            dialogue = quote['dialogue'].strip()
            
            # Basic cleaning
            dialogue = re.sub(r'\s+', ' ', dialogue)  # Remove extra whitespace
            dialogue = dialogue.strip('"\'')  # Remove surrounding quotes
            
            # Skip if too short or already seen
            if len(dialogue) < 10 or dialogue.lower() in seen_dialogues:
                continue
            
            # Skip if doesn't seem like Herbie dialogue
            if not any(keyword in dialogue.lower() for keyword in ['herbie', 'h.e.r.b.i.e', 'robot', 'compute', 'sensors', 'alert']):
                continue
            
            seen_dialogues.add(dialogue.lower())
            quote['dialogue'] = dialogue
            cleaned_quotes.append(quote)
        
        print(f"   Cleaned dataset: {len(cleaned_quotes)} unique quotes")
        return cleaned_quotes

    def save_collected_data(self, quotes: List[Dict]):
        """Save collected data in multiple formats"""
        print("\n💾 Saving collected data...")
        
        # Save as JSON
        json_file = self.base_dir / "automated_herbie_quotes.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(quotes, f, indent=2, ensure_ascii=False)
        
        # Save as CSV
        csv_file = self.base_dir / "automated_herbie_quotes.csv"
        df = pd.DataFrame(quotes)
        df.to_csv(csv_file, index=False, encoding='utf-8')
        
        # Save in training format
        training_file = self.base_dir / "herbie_training_data.jsonl"
        with open(training_file, 'w', encoding='utf-8') as f:
            for quote in quotes:
                training_entry = {
                    "instruction": f"You are Herbie from Fantastic Four. Respond in character to this situation: {quote['situation']}",
                    "input": quote['context'],
                    "output": quote['dialogue']
                }
                f.write(json.dumps(training_entry, ensure_ascii=False) + '\n')
        
        # Save in original template format for manual review
        template_file = self.base_dir / "herbie_quotes_template_format.txt"
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write("# Automatically collected Herbie quotes\n")
            f.write("# Review and edit as needed\n\n")
            
            for quote in quotes:
                f.write("---\n")
                f.write(f"SITUATION: {quote['situation']}\n")
                f.write(f"HERBIE: \"{quote['dialogue']}\"\n")
                f.write(f"EMOTION: {quote['emotion']}\n")
                f.write(f"CONTEXT: {quote['context']}\n")
                f.write(f"SOURCE: {quote['source']}\n")
                f.write("---\n\n")
        
        print(f"   Saved {len(quotes)} quotes to:")
        print(f"   - JSON: {json_file}")
        print(f"   - CSV: {csv_file}")
        print(f"   - Training format: {training_file}")
        print(f"   - Template format: {template_file}")

def main():
    """Main function to run automated collection"""
    collector = HerbieDataCollector()
    
    # Collect all data
    all_quotes = collector.collect_all_data()
    
    # Clean and deduplicate
    clean_quotes = collector.clean_and_deduplicate(all_quotes)
    
    # Save results
    collector.save_collected_data(clean_quotes)
    
    print(f"\n✅ Automation complete!")
    print(f"📊 Total quotes collected: {len(clean_quotes)}")
    print(f"📁 Data saved to: data/raw/automated/")
    print(f"\n🔍 Next steps:")
    print(f"1. Review the collected quotes in data/raw/automated/")
    print(f"2. Edit/improve quotes in herbie_quotes_template_format.txt")
    print(f"3. Run your training data creation script")

if __name__ == "__main__":
    main()