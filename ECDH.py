class ECDH:
    def __init__(self,private_key1,private_key2,ecc):
        self.private_key1 = private_key1
        self.private_key2 = private_key2
        self.ecc = ecc
    
    def gen_public_key (self):        
        public_key1 = self.ecc.scalar_mul(self.private_key1,self.ecc.G)
        public_key2 = self.ecc.scalar_mul(self.private_key2,self.ecc.G)
        return public_key1,public_key2
