class GenKey:
    def __init__(self,private_key,ecc):
        self.private_key = private_key
        self.ecc = ecc
    
    def gen_public_key (self):        
        public_key = self.ecc.scalar_mul(self.private_key,self.ecc.G)
        return public_key
