import os
import shutil
import export
import csv

# Define your data
header = ['ID', 'SIZE', 'SOUND', 'START']
game = "2005"
path = f"D:\\Games\\NBA LIVE {game}\\audio\\speech\\arena\\"

if game == "2001":
    path = f"D:\\Games\\NBA LIVE {game}\\speech\\"
    hdr_idx = f"{path}xearplhr.idx"
    hdr_fcd = f"{path}xearplhr.fcd"
    dat_idx = f"{path}xearndt.idx"
    dat_fcd = f"{path}xearndt.fcd"
else:
    path = f"D:\\Games\\NBA LIVE {game}\\audio\\speech\\arena\\"
    hdr_idx = f"{path}xarplhdr.idx"
    hdr_fcd = f"{path}xarplhdr.fcd"
    dat_idx = f"{path}xarndat.idx"
    dat_fcd = f"{path}xarndat.fcd"

filename = f"{game}speech.csv"
rows = []
ids = []
# reading hdr.idx
def read_hdr_idx():
    with open(hdr_idx, 'rb') as file:
        data = file.read()
        hex_data = data.hex()
        total_data = 0
        # each player has 40 bytes of data.
        for i in range(0, len(hex_data), 80):
            if hex_data[i:i+2] == "00":
                continue
            total_data += 1
            playerID = hex_data[i:i+8]
            hdrStart = hex_data[i+64:i+72]
            hdrLength = hex_data[i+72:i+80]
            byte_playerID = bytes.fromhex(playerID)
            byte_start = bytes.fromhex(hdrStart)
            reversed_byte_start = byte_start[::-1].hex()
            byte_length = bytes.fromhex(hdrLength)
            reversed_byte_length = byte_length[::-1][3:].hex()
            decoded_string = byte_playerID.decode("utf-8")
            print(f"Player ID: {decoded_string}")
            print(f"HDR Start: {reversed_byte_start}")
            print(f"HDR Length: {reversed_byte_length} ({int(reversed_byte_length, 16)})")
            hdrdata = read_hdr_fcd("", reversed_byte_start, int(reversed_byte_length, 16))
            id = hdrdata[0]
            ids.append(id)
            rows.append(hdrdata)
            # print(hex_data[i:i+80])
    print(f"Total number of PA data: {total_data}")

def read_hdr_idx_2003():
    with open(hdr_idx, 'rb') as file:
        data = file.read()
        hex_data = data.hex()
        total_data = 0
        # each player has 40 bytes of data.
        for i in range(0, len(hex_data), 48):
            if hex_data[i:i+2] == "00":
                continue
            total_data += 1
            playerID = hex_data[i:i+24]
            hdrStart = hex_data[i+32:i+40]
            hdrLength = hex_data[i+40:i+46]
            byte_playerID = bytes.fromhex(playerID).rstrip(b'\x00')
            byte_start = bytes.fromhex(hdrStart)
            reversed_byte_start = byte_start[::-1].hex()
            byte_length = bytes.fromhex(hdrLength)
            reversed_byte_length = byte_length[::-1][2:].hex()
            decoded_string = byte_playerID.decode("utf-8")
            print(f"Player ID: {decoded_string}")
            print(f"HDR Start: {reversed_byte_start}")
            print(f"HDR Length: {reversed_byte_length} ({int(reversed_byte_length, 16)})")
            decoded_string = decoded_string[:-5]
            hdrdata = read_hdr_fcd(decoded_string, reversed_byte_start, int(reversed_byte_length, 16))
            ids.append(decoded_string)
            rows.append(hdrdata)
            # print(hex_data[i:i+80])
    print(f"Total number of PA data: {total_data}")

def read_hdr_fcd(decoded_string, start, length):
    with open(hdr_fcd, 'rb') as file:
        # decoded_string = decoded_string.ljust(7, '_')
        start_offset = int(start, 16)
        # Seek to the start address
        file.seek(start_offset)
        # Read the specified number of bytes
        data = file.read(length)
        # Convert bytes to hexadecimal string
        # hex_data = ''.join([format(byte, '02x') for byte in data])
        playerID = data[2:4][::-1]
        n_of_sounds = data[5]
        total_size = data[7:9][::-1]
        hex_data = str(int(''.join([format(byte, '02x') for byte in playerID]), 16)).zfill(4)
        total_size = int(''.join([format(byte, '02x') for byte in total_size]), 16)
        if game == "2003" or game == "2001":
            return [decoded_string, total_size, n_of_sounds]
        else:
            return [hex_data, total_size, n_of_sounds]

def read_hdr_fcd07(start, length):
    with open(hdr_fcd, 'rb') as file:
        start_offset = int(start, 16)
        # Seek to the start address
        file.seek(start_offset)
        # Read the specified number of bytes
        data = file.read(length)
        # Convert bytes to hexadecimal string
        # hex_data = ''.join([format(byte, '02x') for byte in data])
        playerID = data[4:6][::-1]
        n_of_sounds = data[3]
        total_size = data[9:12][::-1]
        hex_data = str(int(''.join([format(byte, '02x') for byte in playerID]), 16)).zfill(4)
        total_size = int(''.join([format(byte, '02x') for byte in total_size]), 16)
        return [hex_data, total_size, n_of_sounds]

def read_dat_idx():
    with open(dat_idx, 'rb') as file:
        data = file.read()
        hex_data = data.hex()
        total_data = 0
        # each player has 40 bytes of data.
        for i in range(0, len(hex_data), 80):
            if hex_data[i:i+2] == "00":
                continue
            total_data += 1
            if hex_data[i+8:i+10] == "6a":
                continue
            playerID = hex_data[i:i+8]
            hdrStart = hex_data[i+64:i+72]
            hdrLength = hex_data[i+72:i+78]
            byte_playerID = bytes.fromhex(playerID)
            byte_start = bytes.fromhex(hdrStart)
            reversed_byte_start = byte_start[::-1].hex()
            byte_length = bytes.fromhex(hdrLength)
            reversed_byte_length = byte_length[::-1][3:].hex()
            decoded_string = byte_playerID.decode("utf-8")
            if decoded_string in ids:
                for sublist in rows:
                    if sublist[0] == decoded_string:
                        sublist.append(reversed_byte_start)
            # print(f"Player ID: {decoded_string}")
            # print(f"DAT Start: {reversed_byte_start}")
            # print(f"DAT Length: {reversed_byte_length} ({int(reversed_byte_length, 16)})")
    print(f"Total number of PA data: {total_data}")

def read_dat_idx_2003():
    with open(dat_idx, 'rb') as file:
        data = file.read()
        hex_data = data.hex()
        total_data = 0
        # each player has 40 bytes of data.
        for i in range(0, len(hex_data), 48):
            if hex_data[i:i+2] == "00":
                continue
            total_data += 1
            playerID = hex_data[i:i+24]
            hdrStart = hex_data[i+32:i+40]
            hdrLength = hex_data[i+40:i+46]
            byte_playerID = bytes.fromhex(playerID).rstrip(b'\x00')
            byte_start = bytes.fromhex(hdrStart)
            reversed_byte_start = byte_start[::-1].hex()
            byte_length = bytes.fromhex(hdrLength)
            reversed_byte_length = byte_length[::-1][3:].hex()
            decoded_string = byte_playerID.decode("utf-8")
            decoded_string = decoded_string[:-5]
            if decoded_string in ids:
                for sublist in rows:
                    if sublist[0] == decoded_string:
                        sublist.append(reversed_byte_start)
            # print(f"Player ID: {decoded_string}")
            # print(f"DAT Start: {reversed_byte_start}")
            # print(f"DAT Length: {reversed_byte_length} ({int(reversed_byte_length, 16)})")
    print(f"Total number of PA data: {total_data}")

# def create_hdr_player():
#     hdr += "CA43"
# After blocks are set, add 256 new bytes. At the end of the bytes, there should be a new block.
# which will be 4872496E then created HDR then 4872537A000000 then 1C (from 1C, 14, 18 remember)

def read_speech():
    if game == "2003" or game == "2001":
        read_hdr_idx_2003()
        read_dat_idx_2003()
    else:
        read_hdr_idx()
        read_dat_idx()

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file, escapechar='\\')
        # Write the header
        writer.writerow(header)
        # Write the data rows
        writer.writerows(rows)

def export_speech(file):
    try:
        os.mkdir("speeches")
    except:
        pass
    # Read the CSV file
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        # Iterate over each row
        for row in reader:
            if len(row) < 3:
                print(f"Skipping row with insufficient data: {row}")
                continue

            id, address, size = row[0], row[3], row[1]
            # Execute the export_speech_data function
            export.export_speech_data(id, address, size, dat_fcd, game)

def export_speech_2003(file):
    try:
        os.mkdir(f"speeches{game}")
    except:
        pass
    # Read the CSV file
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        # Iterate over each row
        for row in reader:
            if len(row) < 3:
                print(f"Skipping row with insufficient data: {row}")
                continue

            id, address, size = row[0], row[3], row[1]
            # Execute the export_speech_data function
            export.export_speech_2003(id, address, size, dat_fcd, game)

export_speech("2005wanted.csv")
# export_speech_2003("2001wanted.csv")

# read_speech()

# export.export_speech_data("0001", "0095e000", "37888", dat_fcd)

# export.export_speech_2004(dat_fcd, game)