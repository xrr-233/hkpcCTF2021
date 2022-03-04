import random
from Crypto.Util.number import getPrime as get_prime

# https://link.springer.com/content/pdf/10.1007/s42452-019-1928-8.pdf
class NagatyCryptosystem:
    def __init__(self, p=None):
        # Section 3.1
        # 先为系统定义一个一直用下去的大质数
        self.p = get_prime(1024) if p is None else p
        
        # 生成1024个小于2^1024的数字
        u = [random.getrandbits(1024) for _ in range(1024)]

        self.private_key = sum(u) # 私钥为这1024个数之和
        self.public_key  = self.private_key % self.p # 公钥为私钥%大质数

        self.shared_key = None

    def start_exchange(self): # 返回公钥和大质数
        return (self.public_key, self.p)

    def exchange(self, y_B):
        S_A = self.private_key
        y_A = self.public_key

        y_AB = y_A * y_B
        S_AB = (y_AB * y_B) * S_A % self.p
        print("S_AB: " + str(S_AB))
        S_AB1 = (y_AB * y_B) * y_A * (self.p + 1) % self.p
        print("S_AC: " + str(S_AB))

        self.shared_key = S_AB # 共享密钥 = 两者的公钥相乘 * 别人的公钥 * 自己的私钥 % 大质数

    def encrypt(self, m):
        sk = self.shared_key
        if sk is None: raise Exception('Key exchange is not completed')

        return m * sk
    
    def decrypt(self, c):
        sk = self.shared_key
        if sk is None: raise Exception('Key exchange is not completed')

        return c // sk


# Sanity test
if(__name__=="__main__"):
    cipher_alice = NagatyCryptosystem()
    alice_public_key, p = cipher_alice.start_exchange() # 拿到公钥

    cipher_bob = NagatyCryptosystem(p)
    bob_public_key, _ = cipher_bob.start_exchange() # 两个人的公钥不一样

    cipher_alice.exchange(bob_public_key)
    cipher_bob.exchange(alice_public_key)
    print("A公钥：" + str(alice_public_key))
    print("A私钥：" + str(cipher_alice.private_key))
    print("B公钥：" + str(bob_public_key))
    print("B私钥：" + str(cipher_bob.private_key))
    print("A共享密钥：" + str(cipher_alice.shared_key))
    print("B共享密钥：" + str(cipher_bob.shared_key))

    # Test: Alice sends a message to Bob and Bob is able to decrypt it
    m = 1337
    c = cipher_alice.encrypt(m)

    assert cipher_bob.decrypt(c) == m

    # Test: Bob sends a message to Alice and Alice is able to decrypt it
    m = 1337
    c = cipher_bob.encrypt(m)
    assert cipher_alice.decrypt(c) == m

def main():
    # Reads the flag and converts the string into a number
    with open('flag.txt', 'rb') as f: flag = f.read()
    flag = int.from_bytes(flag, 'big')

    cipher_alice = NagatyCryptosystem()
    alice_public_key, p = cipher_alice.start_exchange()

    cipher_bob = NagatyCryptosystem(p)
    bob_public_key, _ = cipher_bob.start_exchange()

    cipher_alice.exchange(bob_public_key)
    cipher_bob.exchange(alice_public_key)

    c = cipher_alice.encrypt(flag)
    
    print('p =', hex(p))
    print('y_A =', hex(alice_public_key))
    print('y_B =', hex(bob_public_key))
    print('c =', hex(c))
    # 现在告诉你大质数 两个人的公钥 以及flag经Alice发出的密文

if __name__ == '__main__':
    #test()
    #main()
    p = 0xbba8eaf686a5cb3acb507a29e7fb852e107dd439a8d7ba7228cd74043c8f12e87af197ef20577b61a508612d96fcc8d8d883b7b552b324312bbb851b1b5b40d7683b44f2dc3ee97cf1e177e4acf2867430ba8d564b6f4899a826ebd4cf668249a900d6d81b3c475ba8c374c741ea5fb019e4e96859f6873ee5c726eb84daf345
    y_A = 0x9e619600689100ef9bad38d607c0b2a148f04d7af65f20d6b4ac056c41a8d0653ee16194fde8bb85aea2e4ebaa493eb5a5b352218e380dc38190010eea7716795ac07a9d5f7a2bc610e0bc5234754e487ee52c76343b182e22242c800ae1cf8ae39788199dc636046c9b734262b0015a71e669d079215e7f91b684b4444200fa
    y_B = 0xa52e458bc2274e412c6a5a51ce82a9612c9bb9fedcdfeeb45e18e7c71075a7761f32cbe1c6a7ea5b960f09d1d85a197bfc08ecb0a209daf67c67020844519f3092122492ef997f7715109ffb922b78346319db770cde83701534a097900f772499c012585c10892fbb70f978fc4f83236adda513c9b5b9c1a4386c1de6e70587
    c = 0x49a1477e673e7ab4794f580ef4b54f23209aaa161e5b0f54709ffd6f647b07b15e3577e49479eeb98ef863c128d05c03fa8d8ca6cdefea4d45a8e201fc042417ea066958b926bfe4cbdd558373de791a6b993becddaf2a336609a0ef89d6e8b2af95d598762de2c6b69588d6473419a8a8dc45a5d4b3194c820c97aa6c94ea730ccaf2240721dfff706e3bc3981630187b610d14add798ff1b9a3bfc1c08b3bb562536e9b26caf809b7a7e2e3aabb12df810fe280a11
    shared_key = y_A * y_A * y_B * y_B * (p + 1) % p
    flag = c // shared_key
    print(ascii(hex(flag)))