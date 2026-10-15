
import unittest

from es import ECC
from EC_ElGamal import EC_ElGamal


P = 1009
A = 1
B = 50
G = (0, 177)
EXPECTED_ORDER = 1000


class TestECC(unittest.TestCase):
    def setUp(self):
        self.ecc = ECC(P, A, B, G)

    def assert_on_curve(self, point):
        if point is None:
            return
        x, y = point
        self.assertTrue(0 <= x < P and 0 <= y < P)
        self.assertEqual((y * y - x**3 - A * x - B) % P, 0,
        msg=f"曲線上にない点です: {point}")

    def test_generator_order(self):
        self.assertGreater(EXPECTED_ORDER, 0)
        self.assertIsNotNone(G)
        self.assert_on_curve(G)
        point = None

        for n in range(1, EXPECTED_ORDER + 1):
            point = self.ecc.add(point, G)
            self.assert_on_curve(point)
            # 逐次加算とスカラー倍の結果も比較する。
            self.assertEqual(self.ecc.scalar_mul(n, G), point,
            msg=f"{n}G: 加算とスカラー倍が一致しません")
            if n < EXPECTED_ORDER:
                self.assertIsNotNone(
                    point, msg=f"指定回数より早い{n}回で一周しました")
            else:
                self.assertIsNone(
                    point, msg=f"{EXPECTED_ORDER}回で一周しませんでした")

    def test_encryption_decryption(self):
        if (P, A, B, G) == (1009, 1, 50, (0, 177)):
            with self.subTest(case="既知の暗号文"):
                cipher = EC_ElGamal((3, 33), (5, 455), 114, 60, self.ecc)
                self.assertEqual(self.ecc.scalar_mul(114, G), (5, 455))
                self.assertEqual(cipher.encryption(), ((80, 604), (726, 130)))
                self.assertEqual(cipher.decryption((80, 604), (726, 130)),(3, 33))

        private_keys = (1, 7, 114, EXPECTED_ORDER - 1)
        ephemeral_keys = (1, 2, 60, EXPECTED_ORDER // 2, EXPECTED_ORDER - 1)

        for private_key in private_keys:
            public_key = self.ecc.scalar_mul(private_key, G)
            self.assertIsNotNone(public_key)
            self.assert_on_curve(public_key)
            for k in ephemeral_keys:
                shared = self.ecc.scalar_mul(k, public_key)
                messages = (
                    G,
                    self.ecc.scalar_mul(7, G),
                    self.ecc.scalar_mul(EXPECTED_ORDER // 2, G),
                    self.ecc.negate(shared),
                    None,
                )
                for message in messages:
                    with self.subTest(private_key=private_key, k=k, M=message):
                        self.assert_on_curve(message)
                        cipher = EC_ElGamal(
                            message, public_key, private_key, k, self.ecc)
                        c1, c2 = cipher.encryption()
                        self.assert_on_curve(c1)
                        self.assert_on_curve(c2)
                        self.assertEqual(cipher.decryption(c1, c2), message)


if __name__ == "__main__":
    unittest.main(verbosity=2)
