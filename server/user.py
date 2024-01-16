import subprocess

class UserClass:
    def __init__(self, telecom):
        try:
            contract_id = subprocess.run(["cat", "../.soroban/arch-id"], check=True, capture_output = True)
        except:
            raise Exception("Cannot find contract ID!")
        try:
            auth_id = subprocess.run(["soroban", "config", "identity", "address", "--global", telecom], check=True, capture_output = True)
        except:
            raise Exception("Cannot find auth ID!")
        
        self.contract = contract_id.stdout.decode('ascii')[:-1]
        self.auth = auth_id.stdout.decode('ascii')[:-1]

    def get(self, telecom):
        try:
            result = subprocess.run(["soroban", "contract", "invoke", 
                        "--id", self.contract, 
                        "--source", telecom,
                        "--network", "testnet",
                        "--", 
                        "user_usage", 
                        "--auth", self.auth], check=True, capture_output = True)
            return result.stdout.decode('ascii')
        except:
            raise Exception("Error")
        
    def remove(self, telecom):
        try:
            subprocess.run(["soroban", "contract", "invoke", 
                            "--id", self.contract, 
                            "--source", telecom,
                            "--network", "testnet",
                            "--", 
                            "remove_user_usage", 
                            "--auth", self.auth], check=True)
        except:
            raise Exception("Error")