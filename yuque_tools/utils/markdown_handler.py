import logging
import os
import tempfile
import shutil
import pypandoc


class MarkdownHandler:
    """A class to handle markdown file operations and conversions.
    
    This class provides functionality to handle markdown files, including loading 
    content from files or strings and converting markdown to other formats like 
    docx.
    """

    def __init__(self, path=None, content=None):
        """Initialize MarkdownHandler with either markdown file path or content.
        
        Args:
            path (str, optional): Path to markdown file to load
            content (str, optional): Raw markdown content string to use
            
        Raises:
            ValueError: If neither path nor content is provided, or if both are 
                provided simultaneously
        """
        content_len = len(content) if content else 0
        logging.debug(
            f"Initializing MarkdownHandler: path={path}, content_len={content_len}"
        )
        self._validate_inputs(path, content)
        self._temp_file = None  # Temporary file path for content string
        self._temp_dir = None   # Temporary directory for content string
        
        if content:
            logging.debug("Creating temporary directory and file for content")
            # Create temporary directory and file if content is provided
            self._temp_dir = tempfile.mkdtemp()
            self._temp_file = os.path.join(self._temp_dir, 'content.md')
            with open(self._temp_file, 'w', encoding='utf-8') as f:
                f.write(content)
            self.path = self._temp_file
            logging.debug(f"Created temp file: {self._temp_file}")
        else:
            self.path = path
            
        self.content = self._load_content()
        logging.debug(f"Loaded content, length: {len(self.content)}")

    def _validate_inputs(self, path, content):
        """Validate the initialization input parameters.
        
        Ensures that exactly one of path or content is provided.
        
        Args:
            path (str): Path to markdown file
            content (str): Markdown content string
            
        Raises:
            ValueError: If both inputs are provided or if neither is provided
        """
        logging.debug("Validating input parameters")
        if path and content:
            logging.error("Both path and content provided")
            raise ValueError("Cannot provide both path and content")
        if not path and not content:
            logging.error("Neither path nor content provided")
            raise ValueError("Must provide either path or content")

    def _load_content(self):
        """Load markdown content from file.
        
        Returns:
            str: The raw markdown content read from file
            
        Raises:
            IOError: If file cannot be read
        """
        logging.debug(f"Loading content from: {self.path}")
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except IOError as e:
            logging.error(f"Failed to read {self.path}: {str(e)}")
            raise

    def to_docx(self, output_path):
        """Convert markdown to docx format.
        
        Converts the markdown content to a Word document using pandoc.
        Changes working directory during conversion to handle relative paths.
        
        Args:
            output_path (str): Path where the docx file should be saved
        
        Returns:
            None
                
        Raises:
            ValueError: If output path is not provided
            RuntimeError: If pandoc conversion fails
        """
        if not output_path:
            raise ValueError("Output path must be provided")

        # Save current working directory
        original_cwd = os.getcwd()
        
        try:
            # Change to markdown file's directory before conversion
            # This ensures relative paths (e.g. for images) work correctly
            os.chdir(os.path.dirname(self.path))
            
            # Convert markdown to docx using pandoc
            logging.info(
                f"Converting markdown file to Word document {output_path}"
            )
            pypandoc.convert_file(
                self.path,
                "docx", 
                outputfile=output_path
            )
            logging.info("Successfully converted markdown to Word document")
            
        finally:
            # Restore original working directory
            os.chdir(original_cwd)

    def __del__(self):
        """Cleanup temporary files and directories on object destruction.
        
        Removes any temporary files and directories created for content string 
        handling. Silently ignores any errors during cleanup.
        """
        if self._temp_file and os.path.exists(self._temp_file):
            try:
                logging.debug(f"Removing temp file: {self._temp_file}")
                os.unlink(self._temp_file)
            except (OSError, AttributeError) as e:
                logging.warning(f"Failed to remove temp file: {str(e)}")
                
        if self._temp_dir and os.path.exists(self._temp_dir):
            try:
                logging.debug(f"Removing temp dir: {self._temp_dir}")
                shutil.rmtree(self._temp_dir)
            except (OSError, AttributeError) as e:
                logging.warning(f"Failed to remove temp directory: {str(e)}")
