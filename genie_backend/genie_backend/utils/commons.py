from solders.keypair import Keypair


def create_account():
    try:
        kp = Keypair()
        public_key = str(kp.pubkey())
        secret_key = kp.secret()

        return public_key, secret_key
    except Exception:
        raise
