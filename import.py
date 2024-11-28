import os
import subprocess
import struct
import shutil

def import_wav(directory):
    """Adjust volume of all .wav files in a directory and its subdirectories."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.wav'):
                file_path = os.path.join(root, file)
                subprocess_command = f"sx -sndstream -mt_blk {file_path} -={file_path[:-4]}.asf"

                try:
                    subprocess.run(subprocess_command, check=True)
                    print(f"Subprocess applied to {file_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Subprocess failed for {file_path} with error: {e}")

                with open(f"{file_path[:-4]}.asf", 'rb') as file:
                    data = file.read()

                total_size = len(data)
                print(f"Original size: {total_size} bytes")

                if total_size % 256 != 0:
                    padding_needed = 256 - (total_size % 256)
                    print(f"Padding needed: {padding_needed} bytes")
                    
                    data += b'\x00' * padding_needed

                    with open(f"{file_path[:-4]}.asf", 'wb') as file:
                        file.write(data)
                    
                    print(f"New size: {len(data)} bytes")
                else:
                    print("File size is already divisible by 256 bytes")

                # Once done make sure total byte sizes can be divided by 256. Add enough bytes to make sure this happens

# Convert ID to UINT16
def int_to_uint16(value):
    """Convert an integer to UINT16 and return as a hexadecimal string."""
    value = int(value)
    if not (0 <= value <= 65535):
        raise ValueError("Value out of range for UINT16")
    uint16_bytes = struct.pack('H', value)
    return uint16_bytes.hex()


def int_to_uint8(value):
    """Convert an integer to UINT8 and return as a hexadecimal string."""
    if not (0 <= value <= 255):
        raise ValueError("Value out of range for UINT8")
    uint8_bytes = struct.pack('B', value)
    return uint8_bytes.hex()

def reverse_hex_offset(hex_offset):
    """Reverse the order of bytes in a hexadecimal offset."""
    # Convert hex string to an integer
    int_value = int(hex_offset, 16)
    
    # Convert integer to bytes (ensure it is 2 bytes long)
    byte_value = int_value.to_bytes(2, byteorder='big')
    
    # Reverse the bytes
    reversed_byte_value = byte_value[::-1]
    
    # Convert the reversed bytes back to an integer
    reversed_int_value = int.from_bytes(reversed_byte_value, byteorder='big')
    
    # Convert the integer back to a zero-padded hex string
    reversed_hex_offset = f'{reversed_int_value:04X}'
    
    return reversed_hex_offset

def get_hex_string_from_length(array_length):
    """Return a hex string based on the length of an array."""
    if array_length == 3:
        return '07'
    elif array_length == 2:
        return '03'
    elif array_length == 1:
        return '01'
    else:
        raise ValueError("Unsupported array length. Only lengths 1, 2, and 3 are supported.")

def int_to_byte_string(value):
    if not isinstance(value, int):
        raise TypeError("Input value must be an integer.")
    
    # Convert the integer to hexadecimal and remove the '0x' prefix
    hex_str = hex(value)[2:]
    
    # Ensure the result is uppercase
    hex_str = hex_str.upper()
    
    # Pad with a leading zero if the length of hex_str is odd
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str
    
    return hex_str

def count_trailing_zero_bytes(file_path):
    """Count how many times the byte 00 appears at the end of the file."""
    with open(file_path, 'rb') as file:
        data = file.read()
    
    # Reverse the data to count trailing zeros
    reversed_data = data[::-1]
    zero_byte = b'\x00'
    
    count = 0
    for byte in reversed_data:
        if byte == zero_byte[0]:
            count += 1
        else:
            break
    # At end of an .asf file, there are 3 bytes as 00.
    count -= 3
    
    return count

def modify_file_with_bytes(file_path, byte_set_str):
    """Modify the file by appending the byte set, preserving existing trailing bytes."""
    # Convert the byte set string to bytes
    byte_set = bytes.fromhex(byte_set_str)
    byte_set_length = len(byte_set)
    # Read the file data
    with open(file_path, 'rb') as file:
        data = file.read()
    
    # Count trailing zero bytes
    reversed_data = data[::-1]
    zero_byte = b'\x00'
    
    trailing_zero_count = -3
    for byte in reversed_data:
        if byte == zero_byte[0]:
            trailing_zero_count += 1
        else:
            break

    # Determine if we need to add 256 empty bytes
    if trailing_zero_count < byte_set_length:
        # Add 256 empty bytes
        data += zero_byte * 256
        trailing_zero_count += 256
    
    # Ensure we have enough trailing zero bytes for replacement
    # Replace only the last byte_set_length trailing zero bytes with the byte set
    new_data = data[:-byte_set_length] + byte_set
    
    # Write the modified data back to the file
    with open(file_path, 'wb') as file:
        file.write(new_data)

def import_hdr(directory):
    ids = next(os.walk(directory))[1]
    for id in ids:
        list = os.listdir(f"{directory}\{id}")
        sounds = [f for f in list if f.endswith(".asf")]
        # 0 is loudest 2 is lowest
        """Concatenate multiple files and print the starting offsets of each."""
        concatenated_data = b''
        current_offset = 0
        offsets = {}
        n_of_sounds = len(sounds)
        for file_path in sounds:
            with open(f"{directory}\{id}\{file_path}", 'rb') as file:
                file_data = file.read()
                offsets[file_path] = current_offset
                concatenated_data += file_data
                current_offset += len(file_data)

        with open(f"{directory}\{id}\{id}.fcd", 'wb') as out_file:
            out_file.write(concatenated_data)
        file_length = len(concatenated_data)

        # print("File starting offsets (in hex):")

        # for file_path, offset in offsets.items():
        #     print(f"{file_path}: {offset:04X}")

        # print(file_length)
        hdr_string = ""
        # Create HDR bytes, append sound type, id and 01
        hdr_string += int_to_uint16(17354) + int_to_uint16(id) + '01'
        hdr_string += str(n_of_sounds).zfill(2)
        hdr_string += "00" + f"{file_length:06X}" + "00000000"
        offsets_later = offsets
        del offsets_later[next(iter(offsets_later))]
        length = len(offsets)
        for file_path, offset in (offsets.items()):
            hdr_string += int_to_uint8(length)
            hdr_string += reverse_hex_offset(f"{(offset):04X}")
            length -= 1
        hdr_string += "00"
        hdr_string += n_of_sounds * "70"
        hdr_string += get_hex_string_from_length(n_of_sounds)
        hdr_string += "000000"
        len_hdr = len(hdr_string) // 2
        # which will be 4872496E then created HDR then 4872537A000000 then 1C (from 1C, 14, 18 remember)
        hdrfordat_string = "4872496E" + hdr_string + "4872537A000000" + int_to_byte_string(len_hdr)
        # print(count_trailing_zero_bytes(f"{directory}\{id}\{id}.fcd"))
        # print(hdrfordat_string)
        # print(len(hdrfordat_string))

        modify_file_with_bytes(f"{directory}\{id}\{id}.fcd", hdrfordat_string)
        # If zero bytes at end are larger than len_hdr, fine, paste hdr there.
        # If not, add 256 more empty bytes.

        hdr_binary_data = bytes.fromhex(hdr_string)

        with open(f"{directory}\{id}\{id}_hdr.fcd", 'wb') as file:
            file.write(hdr_binary_data)

        print(f"Created HDR file for {id}")

    # First, concatenate .asf files and get total size and starting offsets of other sounds.
    # First, add uint of 17354 which is CA43 then player ID (directory name) int_to_uint16 then 01
    # then depending on how many asf files are there, add total n. of asf files 01,02,03
    # add 00, then add total size in UINT16
    # add 0000000000
    # if there are other sounds, start from latest one, 3rd one first and 2nd one later
    # add 02, starting offset of 02
    # add 01, starting offset of 01
    # add 00
    # add 70 for each sound, eg 3 sounds 707070
    # add 07, 03, 01. if 3 sounds, 07 2 sounds, 03 1 sound, 01
    # add 000000
            
def str_to_hex(s):
    return s.encode().hex().upper()

def int_to_reverse_hex(n, length=4):
    hex_str = f'{n:0{length*2}X}'
    byte_array = bytes.fromhex(hex_str)
    return byte_array[::-1].hex().upper()

def read_file_as_hex(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    hex_content = content.hex().upper()
    return hex_content

def write_hex_to_file(hex_content, output_file_path):
    with open(output_file_path, 'ab') as output_file:
        output_file.write(bytes.fromhex(hex_content))

def get_current_offset(output_file_path):
    try:
        return os.path.getsize(output_file_path)
    except FileNotFoundError:
        return 0

def insert_before_block(file_path, target_block, insert_content):
    with open(file_path, 'rb+') as file:
        content = file.read().hex().upper()
        target_index = content.find(target_block)
        
        if target_index == -1:
            print(f"Target block not found in {file_path}.")
            return

        # Calculate byte position from hex position
        byte_index = target_index // 2

        # Insert content
        file.seek(byte_index)
        rest_of_file = file.read()
        file.seek(byte_index)
        file.write(bytes.fromhex(insert_content))
        file.write(rest_of_file)

def append_data(directory, game):
    path = f"D:\\Games\\NBA LIVE {game}\\audio\\speech\\arena\\"
    hdr_idx = f"{path}xarplhdr.idx"
    hdr_fcd = f"{path}xarplhdr.fcd"
    dat_idx = f"{path}xarndat.idx"
    dat_fcd = f"{path}xarndat.fcd"

    ids = next(os.walk(directory))[1]
    hdrs = []
    sounds = []
    for id in ids:
        list = os.listdir(f"{directory}\{id}")
        hdrs.append(f"{directory}\{id}\{id}_hdr.fcd")
        sounds.append(f"{directory}\{id}\{id}.fcd")

    dat_current_offset = get_current_offset(dat_fcd)
    hdr_current_offset = get_current_offset(hdr_fcd)

    for sound in sounds:
        # append sound to dat_fcd
        # Read the file content as hex
        hex_content = read_file_as_hex(sound)
        id = ids[sounds.index(sound)]
        # Calculate the length in bytes
        length = len(hex_content) // 2

        # Print the current offset and length
        # print(f"File: {sound}, Starting Offset: {dat_current_offset}, Length: {length}")

        # Write the hex content to the output file
        write_hex_to_file(hex_content, dat_fcd)

        # append index to dat_idxd
        # Convert ID to hex
        id_hex = str_to_hex(id)
        
        # Find the block and insert the content before it
        if game == "2005":
            predefined_bytes = "2E64617400006174002E64617400617400CCCCCCCCCCCCCCCCCCCCCC"
            target_block = "0035332E6461740000006174002E646174006174"
        elif game == "06":
            predefined_bytes = "2E646174006E74726F2E6461740000740064617400CCCCCCCCCCCCCC"
            target_block = "0035332E64617400006E74726F2E64617400007400646174"
            
        # Predefined bytes
        length_hex = int_to_reverse_hex(length, 4)

        # Create the insertion content
        insert_content = id_hex + predefined_bytes + int_to_reverse_hex(dat_current_offset, 4) + length_hex

        insert_before_block(dat_idx, target_block, insert_content)

        # Update the current offset
        dat_current_offset += length

        print(f"Imported {id} to dat.fcd")
        
    for hdr in hdrs:
        # append sound to dat_fcd
        # Read the file content as hex
        hex_content = read_file_as_hex(hdr)
        id = ids[hdrs.index(hdr)]
        # Calculate the length in bytes
        length = len(hex_content) // 2

        # Print the current offset and length
        # print(f"File: {sound}, Starting Offset: {dat_current_offset}, Length: {length}")

        # Write the hex content to the output file
        write_hex_to_file(hex_content, hdr_fcd)

        # append index to dat_idxd
        # Convert ID to hex
        id_hex = str_to_hex(id)
        
        # Predefined bytes
        predefined_bytes = "2E68647200CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"

        length_hex = int_to_reverse_hex(length, 4)

        # Create the insertion content
        insert_content = id_hex + predefined_bytes + int_to_reverse_hex(hdr_current_offset, 4) + length_hex

        # Find the block and insert the content before it
        target_block = "003839382E68647200CCCCCCCCCCCCCCCCCCCCCC"
        insert_before_block(hdr_idx, target_block, insert_content)
        
        # Update the current offset
        hdr_current_offset += length

        print(f"Imported {id} to hdr.fcd")
    
    print(f"Number of imported HDR files: {len(hdrs)}")
    print(f"Number of imported sound files: {len(sounds)}")

    # Get length of id.fcd
    # Append id.fcd to arndat.fcd then get starting offset
    # Append a new line to arndat.idx with info

    # Get length of id_hdr.fcd
    # Append id.fcd to arplhdr.fcd then get starting offset
    # Append a new line to arplhdr.idx with info

# Example usage
game = input("Enter the game that you want to import PA speech data (type 2005 or 06): ")
directory = f"speeches{game}"

operation = input("What operation do you want to do? For converting sounds to .asf files ands creating HDR data, type I. If you want to import sound data to game, type A.")
if operation == "A" or operation == "a":
    append_data(directory, game)
elif operation == "I" or operation == "i":
    import_wav(directory)
    import_hdr(directory)

else:
    input("You didn't select an operation. Please re-run the script, and press Enter to exit the script.")
