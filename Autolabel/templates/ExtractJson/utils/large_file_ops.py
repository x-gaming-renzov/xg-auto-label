import os

def create_chunks(file_path, cache_path):
    with open(file_path, "r") as f:
        #read one line at a time till end of file
        chunk_id = 0
        while True:
            line = f.readline()
            if not line:
                break
            #create a new file for each line
            with open(f"{cache_path}/chunks/chunk_{chunk_id}.txt", "w") as chunk_file:
                chunk_file.write(line)
            chunk_id += 1
    return chunk_id

    