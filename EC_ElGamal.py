class EC_ElGamal:
    def __init__ (self,M,public_key,private_key,k,ecc):
        self.M = M
        self.public_key = public_key
        self.private_key = private_key
        self.k = k
        self.ecc = ecc
    
    def encryption(self):
        C1 = self.ecc.scalar_mul(self.k,self.ecc.G)
        C2 = self.ecc.add(self.M,self.ecc.scalar_mul(self.k,self.public_key))
        return C1,C2

    def decryption(self,C1,C2):
        shared = self.ecc.scalar_mul(self.private_key,C1)
        dec_M = self.ecc.add(C2,self.ecc.negate(shared))
        return dec_M


