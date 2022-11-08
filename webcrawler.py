import os


#create directory
def create_dir(directory):
    if not os.path.exists(directory):
        print("creating directory... '{}'".format(directory))
        os.makedirs(directory)
        print('Directory created')
    else:
        print('directory exists!')

#create file
def create_file(directory, base_site):
    queue_file = os.path.join(directory, 'queue.txt')
    crawled_file = os.path.join(directory, 'crawled_site.txt')
    if not os.path.isfile(queue_file):
        write_file(queue_file, base_site)
    if not os.path.isfile(crawled_file):
        write_file(crawled_file, '')

#write to file
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)

#append to file
def append_to_file(path, data):
    with open(path, 'a') as f:
        f.write(data, '\n')

#delete file-content
def delete_file_content(path):
    open(path, 'w').close()

#copy content from file to a set-object. this is to increase program execution speed as it is faster to access set-object compared to a file
def file_to_set(filename):
    file_content = set()
    with open(filename, 'rt') as f:
        for line in f:
            file_content.add(line.replace('\n', ''))

    return file_content

#copy content from set-object back to file.
def set_to_file(content, filename):
    with open(filename, 'w') as f:
        for each in sorted(content):
            f.write(each+'\n')
