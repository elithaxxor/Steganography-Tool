import os
import platform
import psutil
from tools.embed_binary import SteganographyTool
from tools.hidden_msg.recv.recv import MessageReceiver
from tools.hidden_msg.hide.hide_msg import MessageHider
from colorama import Fore, Style, init

init(autoreset=True)

def display_system_info():
    print(f"{Fore.CYAN}System Information:")
    print(f"{Fore.GREEN}OS: {platform.system()} {platform.release()}")
    print(f"{Fore.GREEN}Processor: {platform.processor()}")
    print(f"{Fore.GREEN}Architecture: {platform.architecture()[0]}")
    print(f"{Fore.GREEN}Machine: {platform.machine()}")
    print(f"{Fore.GREEN}Python Version: {platform.python_version()}")
    
    print(f"\n{Fore.CYAN}Disk Information:")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"{Fore.GREEN}Device: {partition.device}")
        print(f"{Fore.GREEN}Mountpoint: {partition.mountpoint}")
        print(f"{Fore.GREEN}File system type: {partition.fstype}")
        usage = psutil.disk_usage(partition.mountpoint)
        print(f"{Fore.GREEN}Total Size: {usage.total / (1024 ** 3):.2f} GB")
        print(f"{Fore.GREEN}Used: {usage.used / (1024 ** 3):.2f} GB")
        print(f"{Fore.GREEN}Free: {usage.free / (1024 ** 3):.2f} GB")
        print(f"{Fore.GREEN}Percentage: {usage.percent}%")
        print("")

def main_menu():
    while True:
        print(f"{Fore.CYAN}Main Menu:")
        print(f"{Fore.YELLOW}1. Hide a message in an image")
        print(f"{Fore.YELLOW}2. Retrieve a hidden message from an image")
        print(f"{Fore.YELLOW}3. Embed binary data in an image")
        print(f"{Fore.YELLOW}4. Retrieve embedded binary data from an image")
        print(f"{Fore.RED}5. Exit")
        
        choice = input(f"{Fore.CYAN}Enter your choice: ")
        
        if choice == '1':
            image_path = input(f"{Fore.CYAN}Enter the path to the image: ")
            message = input(f"{Fore.CYAN}Enter the message to hide: ")
            output_path = input(f"{Fore.CYAN}Enter the output path for the image: ")
            message_hider = MessageHider(image_path, message, output_path)
            message_hider.hide_message()
        elif choice == '2':
            image_path = input(f"{Fore.CYAN}Enter the path to the image: ")
            message_receiver = MessageReceiver(image_path)
            message_receiver.retrieve_message()
        elif choice == '3':
            img_name = input(f"{Fore.CYAN}Enter the path to the image: ")
            img_name_2 = input(f"{Fore.CYAN}Enter the path to the second image: ")
            executable_toEmbed = input(f"{Fore.CYAN}Enter the path to the executable: ")
            steganography_tool = SteganographyTool(img_name, img_name_2, executable_toEmbed)
            input_text = input(f"{Fore.CYAN}Enter the text to embed: ")
            steganography_tool.add_text(input_text)
            steganography_tool.read_hidden()
            steganography_tool.embed_image_hexData()
            steganography_tool.read_embedded_image_hexData()
            steganography_tool.embed_executable_file()
            steganography_tool.retrieve_embedded_exec()
        elif choice == '4':
            img_name = input(f"{Fore.CYAN}Enter the path to the image: ")
            executable_toEmbed = input(f"{Fore.CYAN}Enter the path to the executable: ")
            steganography_tool = SteganographyTool(img_name, img_name, executable_toEmbed)
            steganography_tool.retrieve_embedded_exec()
        elif choice == '5':
            print(f"{Fore.RED}Exiting...")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.")

if __name__ == '__main__':
    display_system_info()
    main_menu()
