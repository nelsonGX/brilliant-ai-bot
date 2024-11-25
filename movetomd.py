import sys
import os
import re

def extract_sections(content):
    # Split content into lines
    lines = content.split('\n')
    
    # Initialize variables
    current_h1 = {'title': '', 'content': [], 'subsections': {}}
    current_h2 = None
    sections = {}
    
    for line in lines:
        # Check for h1 (# title)
        if line.startswith('# '):
            if current_h1['title']:
                sections[current_h1['title']] = dict(current_h1)
            current_h1 = {'title': line[2:].strip(), 'content': [], 'subsections': {}}
            current_h2 = None
            
        # Check for h2 (## subtitle)
        elif line.startswith('## '):
            if current_h2:
                current_h1['subsections'][current_h2['title']] = current_h2['content']
            current_h2 = {'title': line[3:].strip(), 'content': []}
            
        # Add content to appropriate section
        else:
            if current_h2:
                current_h2['content'].append(line)
            else:
                current_h1['content'].append(line)
    
    # Add last sections
    if current_h2:
        current_h1['subsections'][current_h2['title']] = current_h2['content']
    if current_h1['title']:
        sections[current_h1['title']] = dict(current_h1)
    
    return sections

def create_markdown_files(sections):
    for h1_title, h1_data in sections.items():
        # Create directory for each h1 section
        dir_name = h1_title.replace(' ', '_')
        os.makedirs(dir_name, exist_ok=True)
        
        # Create main h1 file
        with open(f"{dir_name}.md", 'w', encoding='utf-8') as f:
            f.write(f"# {h1_title}\n")
            f.write('\n'.join(h1_data['content']))
        
        # Create files for subsections
        for h2_title, h2_content in h1_data['subsections'].items():
            filepath = os.path.join(dir_name, f"{h2_title.replace(' ', '_')}.md")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {h1_title}\n")
                f.write(f"## {h2_title}\n")
                f.write('\n'.join(h2_content))

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 movetomd.py <filename>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        sections = extract_sections(content)
        create_markdown_files(sections)
        print("Markdown files created successfully!")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()