import re
import logging

class MarkdownFormatter:
    """
    Formats a Markdown file by ensuring appropriate blank lines around titles, paragraphs,
    code blocks, and separators.
    """
    
    def __init__(self, md_path):
        """
        Initializes the MarkdownFormatter with the path to the Markdown file.
        
        Args:
            md_path (str): The path to the Markdown file to be formatted.
        """
        self.md_path = md_path
        self.in_code_block = False

    def _add_blank_lines(self, lines, index, reason):
        """
        Adds blank lines before and after the specified line if needed and logs the action.
        
        Args:
            lines (list): The list of lines from the Markdown file.
            index (int): The index of the current line in the list.
            reason (str): The reason for adding a blank line.
        """
        logging.debug(f"Checking if a blank line is needed before and after line {index + 1}: {reason}")

        # Add a blank line before the current line if needed
        if index > 0 and not re.match(r'^\s*$', lines[index - 1].strip()):
            lines.insert(index, '\n')
            logging.debug(f"Added blank line before line {index + 1}: {reason}")

        # Add a blank line after the current line if needed
        if index == len(lines) - 1:
            # Special case for the last line
            lines.append('\n')
            logging.debug(f"Added blank line after the last line {index + 1}: {reason}")
        elif index < len(lines) - 1 and not re.match(r'^\s*$', lines[index + 1].strip()):
            lines.insert(index + 1, '\n')
            logging.debug(f"Added blank line after line {index + 1}: {reason}")

    def _process_line(self, lines, line, index):
        """
        Processes each line and determines if blank lines need to be added.
        
        Args:
            lines (list): The list of lines from the Markdown file.
            line (str): The current line being processed.
            index (int): The index of the current line in the list.
        """
        stripped_line = line.strip()
        logging.debug(f"Current line: {stripped_line}")

        if re.match(r'^\s*```', stripped_line):
            logging.debug(f"Code block detected at line {index + 1}")
            self._handle_code_block(lines, line, index)
        elif re.match(r'^\s*[-*]\s', stripped_line) or re.match(r'^\s*\d+\.\s', stripped_line):
            logging.debug(f"List item detected at line {index + 1}")
            lines.append(line)
        elif re.match(r'^#+\s', stripped_line) or re.match(r'^\s*[-=]+$', stripped_line):
            logging.debug(f"Title or separator detected at line {index + 1}")
            self._add_blank_lines(lines, len(lines), "Title or separator")
            lines.append(line)
            self._add_blank_lines(lines, len(lines) - 1, "Title or separator")
        elif re.match(r'^\s*---+', stripped_line):
            logging.debug(f"Separator detected at line {index + 1}")
            self._add_blank_lines(lines, len(lines), "Separator")
            lines.append(line)
            self._add_blank_lines(lines, len(lines) - 1, "Separator")
        elif re.match(r'^\s*$', stripped_line):
            logging.debug(f"Blank line detected at line {index + 1}")
            lines.append(line)
        else:
            if not self.in_code_block:
                logging.debug(f"Paragraph detected at line {index + 1}")
                self._add_blank_lines(lines, len(lines), "Paragraph")
            lines.append(line)

    def _handle_code_block(self, lines, line, index):
        """
        Handles the formatting of code blocks, ensuring blank lines before and after.
        
        Args:
            lines (list): The list of lines from the Markdown file.
            line (str): The current line being processed.
            index (int): The index of the current line in the list.
        """
        if not self.in_code_block:
            logging.debug(f"Starting code block at line {index + 1}")
            if len(lines) > 0 and not re.match(r'^\s*$', lines[-1].strip()):
                lines.append('\n')
                logging.debug(f"Added blank line before code block start at line {index + 1}")
        lines.append(line)
        if self.in_code_block:
            logging.debug(f"Ending code block at line {index + 1}")
            if index + 1 < len(lines) and not re.match(r'^\s*$', lines[index + 1].strip()):
                lines.append('\n')
                logging.debug(f"Added blank line after code block end at line {index + 1}")
        self.in_code_block = not self.in_code_block

    def format(self):
        """
        Formats the Markdown file by reading its content, processing it, and writing back the formatted content.
        """
        with open(self.md_path, "r") as file:
            lines = file.readlines()

        formatted_lines = []
        for i, line in enumerate(lines):
            self._process_line(formatted_lines, line, i)

        # Remove redundant blank lines
        formatted_lines = re.sub(r'\n{3,}', '\n\n', ''.join(formatted_lines)).splitlines(keepends=True)
        
        with open(self.md_path, "w") as file:
            file.writelines(formatted_lines)

# Example usage:
# formatter = MarkdownFormatter('path_to_markdown_file.md')
# formatter.format()