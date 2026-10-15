from ecc_cal import ECC
from ECDH import ECDH
from EC_ElGamal import EC_ElGamal


def main():
    P = 1009
    A = 1
    B = 50
    G = (0, 177)
    private_key1 = 114
    private_key2 = 514
    M = (3, 33)
    k = 60  # 1~999

    ecc = ECC(P, A, B, G)
    ecdh = ECDH(private_key1, private_key2, ecc)
    public_key1, public_key2 = ecdh.gen_public_key()
    ec_elgamal = EC_ElGamal(M, public_key1, private_key1, k, ecc)

    C1, C2 = ec_elgamal.encryption()
    restored = ec_elgamal.decryption(C1, C2)
    print("平文: ", M)
    print("暗号化: ", (C1, C2))
    print("復号: ", restored)
    print("一致: ", restored == M)
    if restored != M:
        raise AssertionError("復号結果が元の平文と一致しません")


if __name__ == "__main__":
    main()
