class SHA:
    possible_versions = [1, 2, 3]

    @staticmethod
    def check_version_sanity(self):
        if self.version not in self.possible_versions:
            raise ValueError("type must be one of {}".format(
                self.possible_types))

    @staticmethod
    def assign_digit_size(self):
        if self.version == 1:
            self.digit_size_bit = 160

    @staticmethod
    def check_input_sanity(element):
        if not isinstance(element, str):
            raise TypeError("input type must be {}".format(str))

    @staticmethod
    def get_binary_wo_prefix_0b(element):
        return bin(element)[2:]

    @staticmethod
    def generate_8bit_binary(ascii_decimal):
        bin_w_prefix_0b = bin(ascii_decimal)
        bin_wo_prefix_0b = bin_w_prefix_0b[2:]
        padding = '0' * (8-len(bin_wo_prefix_0b))
        return padding + bin_wo_prefix_0b

    @staticmethod
    def pad_0_until_512_modulo_448(element):
        while len(element) % 512 != 448:
            element += '0'
        return element

    @staticmethod
    def pad_until_64bit(element):
        num_to_pad = 64-len(element)
        assert num_to_pad >= 0
        return '0' * num_to_pad + element

    @staticmethod
    def chunk_512(element):
        num_chunks = len(element) // 512
        assert len(element) % 512 == 0
        chunks = []
        for chunk_idx in range(num_chunks):
            chunk = element[chunk_idx * 512 : (chunk_idx+1) * 512]
            chunks.append(chunk)
        return chunks

    @staticmethod
    def chunk_16_32(element):
        chunks = []
        for chunk_idx in range(16):
            chunk = element[chunk_idx * 32 : (chunk_idx+1) * 32]
            chunks.append(chunk)
        return chunks

    @staticmethod
    def generate_80_32bit_array(chunk):
        """
        Chunk must be 16 * 32bit
        :return: 80 * 32bit
        """
        def XOR(bin1, bin2):
            xor = int(bin1, 2) ^ int(bin2, 2)
            return '{0:b}'.format(xor)

            return bool(bin1) != bool(bin2)

        def leftRotateBy1(bin):
            return bin[-1] + bin[:-1]

        assert len(chunk) == 16
        for elem in chunk:
            assert len(elem) == 32

        for i in range(16, 80):
            wordA = chunk[i-3]
            wordB = chunk[i-8]
            wordC = chunk[i-14]
            wordD = chunk[i-16]

            xorA = XOR(wordA, wordB)
            xorB = XOR(xorA, wordC)
            xorC = XOR(xorB, wordD)

            leftRotated_xorC = leftRotateBy1(xorC)
            chunk.append(leftRotated_xorC)
        return chunk

    def __init__(self, version=1):
        self.version = version
        self.digit_size = None
        self.check_version_sanity(self)
        self.assign_digit_size(self)

    def hash(self, element):
        self.check_input_sanity(element)
        tokens = [token for token in element]
        ascii_decimals = [ord(token) for token in tokens]
        ascii_bins = [self.generate_8bit_binary(ascii_decimal) for ascii_decimal in ascii_decimals]
        joined_ascii_bins = ''.join(ascii_bins)
        length_of_joined_ascii_bins = len(joined_ascii_bins)
        append_one_to_joined_ascii_bins = joined_ascii_bins + '1'
        padded = self.pad_0_until_512_modulo_448(
            append_one_to_joined_ascii_bins)
        # len_padded = len(padded)
        length_binary = self.get_binary_wo_prefix_0b(
            length_of_joined_ascii_bins)
        length_binary_64bit = self.pad_until_64bit(length_binary)
        length_joined_binary = padded + length_binary_64bit
        len_of_length_joined_binary = len(length_joined_binary)
        chunks_512 = self.chunk_512(length_joined_binary)
        chunks_16_32 = [self.chunk_16_32(chunk_512) for chunk_512 in
                        chunks_512]
        chunks_80_32 = [self.generate_80_32bit_array(chunk_16_32) for
                        chunk_16_32 in chunks_16_32]
        pass

if __name__ == "__main__":
    sha1 = SHA(version=3)
    sha1.hash("A Test")

