import requests
import hashlib
import sys


# query_char : hashed version of the data
def API_data_request(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching : {res.status_code}, check the api and try again')
    return res

def get_password_leak_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwnedpasswords_api_check(password):
    # check password if it is exists API reply
    # we have to run our password through SHA one hasing algo use hashlib
    # print(hashlib.sha1(password.encode('utf-8')).hexdigest().upper())
    SHA1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    # we will now store first 5 charecter and last char
    head, tail = SHA1_password[:5], SHA1_password[5:]
    response = API_data_request(head)

    # print((head, tail))
    # print (response)
    return get_password_leak_count(response, tail)
    # return response
    

#API_data_request('CFBRS')
def main(args):
    for password in args:
        count = pwnedpasswords_api_check(password)
        if count :
            print(f'{password} was found {count} of times, you should change your password')
        else :
            print('Your password is unique')
    return 'done!'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))