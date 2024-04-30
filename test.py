import pickle

emails = {
    'nboxer@usc.edu': 'lth',
    'blackadarj22@icloud.com': 'lh'
}

with open('data/emails.pickle', 'wb') as file:
    pickle.dump(emails, file)

