# Summary

#  [in your] main.py
from steganography_tool import add_text, read_hidden, embed_image_hexData, read_embedded_image_hexData, embed_executable_file, retrieve_embedded_exec

# Example usage
add_text('image.jpg', 'hidden message')
hidden_data = read_hidden('image.jpg')
print(hidden_data)

## Why Use __init__.py:
```
    Package Initialization: The __init__.py file is used to mark a directory as a Python package, allowing you to import modules from that directory.
    Organized Imports: It helps in organizing and managing imports by consolidating them in one place.
    Namespace Management: It provides a way to manage the namespace of the package, making it easier to handle imports and dependencies.
```
## Why Switch to Classes:
```
    Encapsulation: Using classes allows encapsulation of related functionalities, which enhances code organization and readability.
    Reusability: Classes promote code reusability by allowing you to create instances with specific states and behaviors.
    Maintainability: Classes make the code more maintainable by grouping related functions and variables together, making it easier to understand and modify.
    Scalability: Classes provide a scalable structure for adding new features and functionalities without disrupting the existing codebase.
```
***By organizing your code into classes and using an __init__.py file, you create a more modular, maintainable, and scalable codebase.
