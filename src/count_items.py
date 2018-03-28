import jsonlines
import os

def main():
    users = {}
    threads = {}
    line_count = 0

    file_path = raw_input('open file: ').strip()
    if os.path.exists(file_path):
        print 'reading...'
        with jsonlines.open(file_path, mode='r') as reader:
            for comment in reader:
                line_count = line_count + 1

                if comment['user'] in users:
                    users[comment['user']] = users[comment['user']] + 1
                else:
                    users[comment['user']] = 1

                if comment['thread'] in threads:
                    threads[comment['thread']] = threads[comment['thread']] + 1
                else:
                    threads[comment['thread']] = 1

        print 'found ' + str(len(users)) + ' users and ' + str(len(threads)) + ' threads with ' + str(line_count) + ' comments'
    else:
        print file_path + ' not found'

if __name__ == "__main__":
    main()
