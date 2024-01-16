import subprocess

class TransactionClass:
    def __init__(self, telecom):
        try:
            contract_id = 'CAY6DBQGPW3ISVL2QRPEROAO5JUSW44OQJLEKI43LOCOTA6AAJMUXM7C'
            # contract_id = subprocess.run(["cat", "../.soroban/arch-id"], check=True, capture_output = True)
        except:
            raise Exception("Cannot find contract ID!")
        try:
            auth_id_process = subprocess.run(["soroban", "config", "identity", "address", "--global", telecom], check=True, capture_output=True)
            auth_id = auth_id_process.stdout.decode('ascii').strip()
        except:
            raise Exception("Cannot find auth ID!")
        
        self.contract = contract_id
        self.auth = auth_id

    def test(self):
        return self.auth

    def add(self, user, telecom_pay, telecom_receive, usage):
        print(self.contract, self.auth, user, telecom_pay, telecom_receive, usage)
        try:
            subprocess.run(["soroban", "contract", "invoke", 
                        "--id", self.contract, 
                        "--source", telecom_pay,
                        "--network", "testnet",
                        "--", 
                        "add_transaction", 
                        "--auth", 'GDKSU7W2OXVTK2D7K4OU67TFF22VMARBQRX2NC7VCXA2ZOIGKH6JHCUP',
                        "--user", user,
                        "--telecom_pay", telecom_pay,
                        "--telecom_receive", telecom_receive,
                        "--usage", str(usage)], check=True)
        except:
            raise Exception("Error")
        
    def get_all(self, telecom):
        try:
            result = subprocess.run(["soroban", "contract", "invoke", 
                        "--id", self.contract, 
                        "--source", telecom,
                        "--network", "testnet",
                        "--", 
                        "get_all_transactions", 
                        "--auth", self.auth], check=True, capture_output = True)
            return result.stdout.decode('ascii')
        except:
            raise Exception("Error")
        
        
    def remove_all(self, telecom):
        try:
            subprocess.run(["soroban", "contract", "invoke", 
                            "--id", self.contract, 
                            "--source", telecom,
                            "--network", "testnet",
                            "--", 
                            "remove_transactions", 
                            "--auth", self.auth], check=True)
        except:
            raise Exception("Error")