from fixed_point import Number

class FloatingPoint(Number):

    def __init__(self):
        self.TOTAL_BITS = 32
        self.MAX_BITS = 31
        self.EXPONENT_BITS = 127
        self.MANTISSA_BITS = 23
        self.IEEE = '01111111'

    def float_to_binary_fraction(self, fraction: float) -> str:
        binary_fraction = ""
        while fraction != 0 and len(binary_fraction) < self.TOTAL_BITS:
            fraction *= 2
            if fraction >= 1:
                binary_fraction += '1'
                fraction -= 1
            else:
                binary_fraction += '0'
        return binary_fraction

    def convert_float_to_bin(self, float_number: float) -> str:
        if float_number == 0.0:
            return '0' * self.TOTAL_BITS

        sign_bit = '0' if float_number >= 0 else '1'
        float_number = abs(float_number)

        exponent_counter = 0
        normalized_float = float_number

        if normalized_float >= 1.0:
            while normalized_float >= 2.0:
                normalized_float /= 2.0
                exponent_counter += 1
        else:
            while normalized_float < 1.0:
                normalized_float *= 2.0
                exponent_counter -= 1

        biased_exponent = exponent_counter + self.EXPONENT_BITS

        exponent_binary_string = ''
        temp_exponent = biased_exponent
        for _ in range(8):
            exponent_binary_string = str(temp_exponent % 2) + exponent_binary_string
            temp_exponent //= 2

        normalized_float -= 1.0
        mantissa_bits = ''
        for _ in range(self.MANTISSA_BITS):
            normalized_float *= 2
            if normalized_float >= 1.0:
                mantissa_bits += '1'
                normalized_float -= 1.0
            else:
                mantissa_bits += '0'

        final_binary_string = sign_bit + exponent_binary_string + mantissa_bits
        return final_binary_string

    def convert_bin_to_float(self, binary_str) -> float:
        sign_char = int(binary_str[0])
        sign = -1 if sign_char else 1

        exponent_bits = ''
        for i in range(1, 9):
            exponent_bits += binary_str[i]
        exponent_value = int(exponent_bits, 2) - self.EXPONENT_BITS

        mantissa_value = 1.0
        for idx in range(9, len(binary_str)):
            if binary_str[idx] == '1':
                mantissa_value += 2 ** -(idx - 8)

        float_result = sign * mantissa_value * (2 ** exponent_value)
        return float_result

    def float_summa(self, float_num1, float_num2):
        FULL_MANTISSA = self.MANTISSA_BITS + 1

        bin_num1 = self.convert_float_to_bin(float_num1)
        bin_num2 = self.convert_float_to_bin(float_num2)

        sign1, exp_bits1, mantissa1 = bin_num1[0], bin_num1[1:9], '1' + bin_num1[9:]
        sign2, exp_bits2, mantissa2 = bin_num2[0], bin_num2[1:9], '1' + bin_num2[9:]

        exp_val1 = int(exp_bits1, 2) - self.EXPONENT_BITS
        exp_val2 = int(exp_bits2, 2) - self.EXPONENT_BITS

        if exp_val1 > exp_val2:
            shift = exp_val1 - exp_val2
            mantissa2 = ('0' * shift) + mantissa2[:-shift]
            exp_val2 = exp_val1
        elif exp_val2 > exp_val1:
            shift = exp_val2 - exp_val1
            mantissa1 = ('0' * shift) + mantissa1[:-shift]
            exp_val1 = exp_val2

        mantissa_val1 = int(mantissa1, 2)
        mantissa_val2 = int(mantissa2, 2)

        if sign1 == sign2:
            mantissa_sum = mantissa_val1 + mantissa_val2
            res_sign = sign1
        else:
            if mantissa_val1 >= mantissa_val2:
                mantissa_sum = mantissa_val1 - mantissa_val2
                res_sign = sign1
            else:
                mantissa_sum = mantissa_val2 - mantissa_val1
                res_sign = sign2

        if mantissa_sum == 0:
            return 0.0

        while mantissa_sum >= (1 << FULL_MANTISSA):
            mantissa_sum >>= 1
            exp_val1 += 1

        while mantissa_sum < (1 << self.MANTISSA_BITS):
            mantissa_sum <<= 1
            exp_val1 -= 1

        final_exp = exp_val1 + self.EXPONENT_BITS
        exp_bits = f"{final_exp:08b}"
        mantissa_bits = f"{mantissa_sum:0{FULL_MANTISSA}b}"[1:]

        result_bin = res_sign + exp_bits + mantissa_bits
        return self.convert_bin_to_float(result_bin)




