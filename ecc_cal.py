
O = None
class ECC:
    def __init__ (self,P,A,B,G):
        self.P = P
        self.A = A
        self.B = B
        self.G = G
        
    def add(self,p,q):
        if p == O :
            return q
        elif q == O :
            return p
        x1,y1 = p
        x2,y2 = q
        if x1 == x2 and (y1 + y2)%self.P == 0 :
            return O
        
        if x1 != x2 :
            num ,den= (y2-y1) , (x2-x1)
        elif p == q :
            num ,den= (3*x1**2+self.A),(2*y1)
        m = (num*pow(den,-1,self.P))%self.P
        x3 = (m**2-x1-x2)%self.P
        y3 = (m*(x1-x3)-y1)%self.P
        P_new = (x3,y3)
        return P_new

    def negate(self, point):
        if point is None:
            return None

        x, y = point
        return (x, (-y) % self.P)

    def scalar_mul(self, k, point):
        if k < 0:
            return self.scalar_mul(-k, self.negate(point))
        result = None
        addend = point
        while k > 0:
            if k & 1:
                result = self.add(result, addend)
            addend = self.add(addend, addend)
            k >>= 1
        return result

