import hashlib
import sqlite3
from flask import Flask, request
from flask_cors import CORS
import random
import string
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

from transaction import TransactionClass
from user import UserClass
from clear import ClearClass

def hash_phone_number(phone_number):
    # Convert the phone number to a byte string
    byte_phone = phone_number.encode()

    # Create a new sha256 hash object
    hasher = hashlib.sha256()

    # Update the hash object with the byte string
    hasher.update(byte_phone)

    # Return the hexadecimal representation of the digest
    return hasher.hexdigest()
def create_did():
    # Define the prefix
    prefix = "did:example:"

    # Define the length of the random part
    random_part_length = 18  # Adjust this number as needed

    # Generate a random string using letters and digits
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=random_part_length))

    # Combine the prefix and the random part
    did = prefix + random_part

    return did
def generate_key_pair(key_size=2048):
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )

    # Generate public key
    public_key = private_key.public_key()

    # Serialize private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serialize public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem
def clear_database():
    # Connect to a database (or create one if it doesn't exist)
    conn = sqlite3.connect('my_database.db')

    # Create a cursor object using the cursor() method
    cursor = conn.cursor()

    # Execute a query
    cursor.execute('DROP TABLE IF EXISTS users')

    # Save (commit) the changes
    conn.commit()

    # Close the connection
    conn.close()
def init_database():
    # Connect to a database (or create one if it doesn't exist)
    conn = sqlite3.connect('my_database.db')

    # Create a cursor object using the cursor() method
    cursor = conn.cursor()
    # Clear the database
    # cursor.execute('DROP TABLE IF EXISTS users')
    # conn.commit()

    # Check if the table exists
    table_name = 'users'
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cursor.fetchone()
    if result:
        print(f"Table '{table_name}' exists.")
        return
    # Create a table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_did TEXT NOT NULL,
        hashed_phone_number TEXT NOT NULL,
        plan TEXT NOT NULL,
        provider TEXT NOT NULL,
        PRIMARY KEY (user_did)
        )
    ''')
    conn.commit()
    # Insert some data
    data = [
        ("1234567890", "Basic", "A_Telecom"),
        ("0987654321", "Premium", "B_Telecom")
    ]
    for row in data:
        user_did=create_did()
        hashed_phone = hash_phone_number(row[0])
        plan = row[1]
        provider = row[2]
        
        try:
            cursor.execute('''
                INSERT INTO users (user_did, hashed_phone_number, plan, provider) 
                VALUES (?, ?, ?, ?)
            ''', (user_did, hashed_phone, plan, provider))
        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")
    conn.commit()

    conn.close()
def print_database():
    # Connect to a database (or create one if it doesn't exist)
    conn = sqlite3.connect('my_database.db')

    # Create a cursor object using the cursor() method
    cursor = conn.cursor()

    # Execute a query
    cursor.execute('SELECT * FROM users')

    # Fetch all rows from the last executed statement
    results = cursor.fetchall()

    # Print the results
    for row in results:
        print(row)

    # Close the connection
    conn.close()
def add_user(user_did, phone_number, plan, provider):
    # Connect to a database (or create one if it doesn't exist)
    conn = sqlite3.connect('my_database.db')

    # Create a cursor object using the cursor() method
    cursor = conn.cursor()
    hashed_phone_number=hash_phone_number(phone_number)
    # Insert some data
    try:
        cursor.execute('''
            INSERT INTO users (user_did, hashed_phone_number, plan, provider) 
            VALUES (?, ?, ?, ?)
        ''', (user_did, hashed_phone_number, plan, provider))
    except sqlite3.IntegrityError as e:
        print(f"Error occurred: {e}")
    conn.commit()

    conn.close()
def delete_user(user_did):
    # Connect to a database (or create one if it doesn't exist)
    conn = sqlite3.connect('my_database.db')

    # Create a cursor object using the cursor() method
    cursor = conn.cursor()
    # Insert some data
    try:
        cursor.execute('''
            DELETE FROM users WHERE user_did=?
        ''', (user_did,))
    except sqlite3.IntegrityError as e:
        print(f"Error occurred: {e}")
    conn.commit()

    conn.close()
def get_user(user_did):
    # Connect to a database (or create one if it doesn't exist)
    conn = sqlite3.connect('my_database.db')

    # Create a cursor object using the cursor() method
    cursor = conn.cursor()
    # Find some data
    try:
        cursor.execute('''SELECT * FROM users WHERE user_did=?''', (user_did,))
    except sqlite3.IntegrityError as e:
        print(f"Error occurred: {e}")
    conn.commit()
    results = cursor.fetchall()
    conn.close()
    return results
def sign_data(private_key_pem, data):
    # Deserialize the private key from bytes
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None,  # Use a password if your key is encrypted
        backend=default_backend()
    )
    return private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
def verify_signature(public_key_pem, signature, data):
    # Deserialize the public key from bytes
    public_key = serialization.load_pem_public_key(
        public_key_pem,
        backend=default_backend()
    )
    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False

app = Flask(__name__)
CORS(app)

@app.route('/verify_VC', methods=['POST'])
def verify_VC():
    req_data = request.get_json()
    json_data = {
        "user_did": req_data['user_did'],
        "hashed_phone_number": req_data['phone_number'],
        "plan": req_data['plan'],
        "provider": req_data['provider']
    }
    print(req_data)
    # Convert JSON to a string
    serialized_json = json.dumps(json_data, sort_keys=True).encode()
    # To verify the signature
    is_valid = verify_signature(public_key, bytes.fromhex(req_data['signature']), serialized_json)

    print("Signature valid:", is_valid)
    if is_valid:
        return "OK", 200
    else:
        return "Error", 400

@app.route('/add_user', methods=['POST'])
def add_user_route():
    user_did = request.get_json().get('user_did')
    phone_number = request.get_json().get('phone_number')
    plan = request.get_json().get('plan')
    provider = request.get_json().get('provider')
    print(user_did, phone_number, plan, provider)
    try:
        add_user(user_did, phone_number, plan, provider)
        json_data = {
        "user_did": user_did,
        "hashed_phone_number": hash_phone_number(phone_number),
        "plan": plan,
        "provider": provider
        }
        # Convert JSON to a string
        serialized_json = json.dumps(json_data, sort_keys=True).encode()
        # Assuming you already have private_key and public_key from the previous steps
        # Sign the serialized JSON
        signature = sign_data(private_key, serialized_json)
        # Attach the signature to your data (or store it however you prefer)
        json_data['signature'] = signature.hex()
    except:
        return "Error", 400
    return json_data, 200


@app.route('/delete_user/<user_did>', methods=['DELETE'])
def delete_user_route(user_did):
    try:
        delete_user(user_did)
    except:
        return "Error", 400
    return "OK", 200

@app.route('/print_database', methods=['GET'])
def print_database_route():
    print_database()
    return "OK", 200

@app.route('/get_did', methods=['GET'])
def get_did_route():
    did = create_did()
    return did, 200

#################### Transaction ####################
# data: {user, telecom_pay, usage}
# TODO: check if user exists
@app.route('/<telecom>/transaction/add', methods=['POST'])
def add_transaction(telecom):
    if request.method == 'POST':
        data = request.get_json()
        transaction = TransactionClass(telecom)
        json_data = {
            "user_did": data['user_did'],
            "hashed_phone_number": data['phone_number'],
            "plan": data['plan'],
            "provider": data['provider']
        }
        print(json_data)
        # Convert JSON to a string
        serialized_json = json.dumps(json_data, sort_keys=True).encode()
        # To verify the signature
        is_valid = verify_signature(public_key, bytes.fromhex(data['signature']), serialized_json)

        print("Signature valid:", is_valid)
        if is_valid:
            print(data)
        else:
            return "Error", 400
        try:
            transaction.add(data["user_did"], data["provider"], telecom , data["usage"])
            return 'Success', 200
        except:
            return 'Fail', 403

@app.route('/<telecom>/transaction/get', methods=['GET'])
def get_transactions(telecom):
    if request.method == 'GET':
        transaction = TransactionClass(telecom)
        try:
            result = transaction.get_all(telecom)
            return result, 200
        except:
            return 'Fail', 403

@app.route('/<telecom>/transaction/remove', methods=['POST'])
def remove_transactions(telecom):
    if request.method == 'POST':
        transaction = TransactionClass(telecom)
        try:
            transaction.remove_all(telecom)
            return 'Success', 200
        except:
            return 'Fail', 403

####################### User ########################
@app.route('/<telecom>/user_usage/get', methods=['GET'])
def get_user_usage(telecom):
    if request.method == 'GET':
        user = UserClass(telecom)
        try:
            result = user.get(telecom)
            return result, 200
        except:
            return 'Fail', 403
        
@app.route('/<telecom>/user/remove', methods=['POST'])
def remove_user_usage(telecom):
    if request.method == 'POST':
        user = UserClass(telecom)
        try:
            user.remove(telecom)
            return 'Success', 200
        except:
            return 'Fail', 403
        
####################### Clear #######################
@app.route('/<telecom>/clear/get', methods=['GET'])
def get_clear(telecom):
    if request.method == 'GET':
        clear = ClearClass(telecom)
        try:
            result = clear.get(telecom)
            return result, 200
        except:
            return 'Fail', 403
        
@app.route('/<telecom>/clear/remove', methods=['POST'])
def remove_clear(telecom):
    if request.method == 'POST':
        clear = ClearClass(telecom)
        try:
            clear.remove(telecom)
            return 'Success', 200
        except:
            return 'Fail', 403

if __name__ == '__main__':
    init_database()
    app.run(debug=True, port=5000)
