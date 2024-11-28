import os
import subprocess

def export_speech_2003(id, address, size, filename, game):
    # Convert address and size to integers
    address = int(address, 16)
    size = int(size)
    
    # Open and read the binary file
    with open(filename, 'rb') as file:
        # Move to the correct position in the file
        file.seek(address)
        # Read the specified number of bytes
        data = file.read(size)

    start_bytes = bytes.fromhex("5343486C24")
    end_bytes = bytes.fromhex("5343456C08000000")

    position = 0
    block_counter = 0
    # Create the output filename
    try:
        os.mkdir(f"speeches{game}\{id}")
    except:
        pass

    while True:
        # Find the start of the next block
        start_index = data.find(start_bytes, position)
        if start_index == -1:
            break  # No more blocks found
        
        # Find the end of the block
        end_index = data.find(end_bytes, start_index + len(start_bytes))
        if end_index == -1:
            break  # No end found for the last block
        
        # Include the end bytes in the block
        end_index += len(end_bytes)
        
        # Extract the block
        block = data[start_index:end_index]
        
        output_filename = f"speeches{game}\\{id}\\{block_counter}.asf"
        
        # Write the block to a new file
        with open(output_filename, 'wb') as output_file:
            output_file.write(block)
        
        # Print confirmation
        print(f"Data block {block_counter} extracted and saved to {output_filename}")
        
        # Apply the subprocess command to the output file
        subprocess_command = f"sx -wave speeches{game}\\{id}\\{block_counter}.asf -=speeches{game}\\{id}\\{block_counter}.wav"

        try:
            subprocess.run(subprocess_command, check=True)
            print(f"Subprocess applied to {output_filename}")
        except subprocess.CalledProcessError as e:
            print(f"Subprocess failed for {output_filename} with error: {e}")
        
        # Delete the .asf file
        if output_filename.endswith(".asf"):
            os.remove(output_filename)
            print(f"File {output_filename} deleted")
        
        # Update position and block counter
        position = end_index
        block_counter += 1

def export_speech_data(id, address, size, filename, game):
    # Convert address and size to integers
    address = int(address, 16)
    size = int(size)
    
    # Open and read the binary file
    with open(filename, 'rb') as file:
        # Move to the correct position in the file
        file.seek(address)
        # Read the specified number of bytes
        data = file.read(size)

    # start_bytes = bytes.fromhex("5343486C24")
    # end_bytes = bytes.fromhex("5343456C08000000")

    if game == "07" or game == "08" or game == "09":
        start_bytes = bytes.fromhex("5343486C28")
        end_bytes = bytes.fromhex("5343456C08000000")
    elif game == "2004":
        start_bytes = bytes.fromhex("5343486C20")
        end_bytes = bytes.fromhex("5343456C08000000")
    else:
        start_bytes = bytes.fromhex("5343486C24")
        end_bytes = bytes.fromhex("5343456C08000000")

    position = 0
    block_counter = 0
    # Create the output filename
    try:
        os.mkdir(f"speeches\{id}")
    except:
        pass

    while True:
        # Find the start of the next block
        start_index = data.find(start_bytes, position)
        if start_index == -1:
            break  # No more blocks found
        
        # Find the end of the block
        end_index = data.find(end_bytes, start_index + len(start_bytes))
        if end_index == -1:
            break  # No end found for the last block
        
        # Include the end bytes in the block
        end_index += len(end_bytes)
        
        # Extract the block
        block = data[start_index:end_index]
        
        output_filename = f"speeches\\{id}\\{block_counter}.asf"
        
        # Write the block to a new file
        with open(output_filename, 'wb') as output_file:
            output_file.write(block)
        
        # Print confirmation
        print(f"Data block {block_counter} extracted and saved to {output_filename}")
        
        # Apply the subprocess command to the output file
        subprocess_command = f"sx -wave speeches\\{id}\\{block_counter}.asf -=speeches\\{id}\\{block_counter}.wav"

        try:
            subprocess.run(subprocess_command, check=True)
            print(f"Subprocess applied to {output_filename}")
        except subprocess.CalledProcessError as e:
            print(f"Subprocess failed for {output_filename} with error: {e}")
        
        # Delete the .asf file
        if output_filename.endswith(".asf"):
            os.remove(output_filename)
            print(f"File {output_filename} deleted")
        
        # Update position and block counter
        position = end_index
        block_counter += 1

