import imaplib
import json 
import email

IMAP_SERVER = "imap-mail.outlook.com"
IMAP_PORT = 993


def read_logon_data():
    with open ("seeds.json") as json_file:
        logon_dict = json.load(json_file)
    return logon_dict

def login(user, password):
    client = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    client.login(user, password)
    client.select("INBOX", readonly=True)
    return client

def download_emails(client:imaplib.IMAP4_SSL ,ids):
    for i in ids:
        print(f"Downloading mail id: {i.decode()}")
        _, data = client.fetch(i, '(RFC822)')
        with open(f'emails/{i.decode()}.eml', 'wb') as f:
            f.write(data[0][1])
    client.close()
    print(f'Downloaded {len(ids)} mails!')

def email_ids(client: imaplib.IMAP4_SSL):
    _, ids = client.search(None, 'ALL')
    ids = ids[0].split()
    return ids


def main():
    logon_dict = read_logon_data()
    result = login(logon_dict["seeds"][0]["username"], logon_dict["seeds"][0]["password"])
    ids = email_ids(result)
    download_emails(result ,ids)
    result.close()

if __name__ == "__main__":
    main()