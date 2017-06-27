import crypto


class OreScheme(object):

    def __init__(self, number, key, namespace=256, sec_size=16):
        self.number = number
        self.slots_length = namespace
        self.sec_size = sec_size
        self.slots = ["0"] * self.slots_length
        self.shuffled_slots = self.slots
        self.slots_keys = [0] * self.slots_length
        self.prf_key = key
        #self.prf_key = crypto.generate_random(self.sec_size)
        self.pi_x = self.number

    @staticmethod
    def int_to_bytes(x):
        return x.to_bytes((x.bit_length() + 7) // 8, 'big')

    @staticmethod
    def cmp(x, y):
        if x < y:
            return -1
        elif x > y:
            return 1
        else:
            return 0

    @staticmethod
    def compare(ctl, ctr):
        ctl_l, ctl_r = ctl
        r = ctr[0]

        result = (ctr[ctl_r + 1] - (int.from_bytes(crypto.prf_hmac(ctl_l, r), 'big'))) % 3

        if result == 2:
            return -1
        else:
            return result

    def _setup(self):
        self.key = crypto.generate_random(self.sec_size)
        #self.random_x = int.from_bytes(crypto.generate_random(self.sec_size), byteorder='big') % self.slots_length

        for i in range(0, self.number):
            self.slots[i] = "1"

        #self.shuffled_slots = self.slots
        #random.seed(os.urandom(self.sec_size))
        #random.shuffle(self.shuffled_slots)

        #picked = False
        #while not picked:
        #    slot = random.randint(0, self.slots_length)
        #    if self.shuffled_slots[slot] == '1':
        #        picked = True
        #        self.pi_x = slot

        for i in range(0, self.slots_length):
            self.slots_keys[i] = crypto.generate_random(self.sec_size)
            aes = crypto.AESCipher(self.slots_keys[i])
            self.shuffled_slots[i] = str(int.from_bytes(aes.encrypt(self.shuffled_slots[i]), 'big'))

    def encrypt(self):
        self._setup()
        left_ciphertext = (crypto.prf_hmac(self.prf_key, bytes(self.pi_x)), self.pi_x)

        nonce = crypto.generate_random(self.sec_size)

        right_ciphertext = [nonce]
        for i in range(0, self.slots_length):
            right_ciphertext += [(self.cmp(i, self.number) + int(crypto.prf_hmac(crypto.prf_hmac(self.prf_key, bytes(i)), nonce), 16)) % 3]

        return left_ciphertext, right_ciphertext
