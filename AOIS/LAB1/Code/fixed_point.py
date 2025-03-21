class Number:
    def __init__(self):
        self.TOTAL_BITS = 32
        self.MAX_BITS = 31
        self.MANTISSA_BITS = 23

    def binary_number(self, dec_num):
        number = abs(int(dec_num))
        binary = ''
        while number > 0:
            binary = str(number % 2) + binary
            number //= 2
        while len(binary) < self.MAX_BITS:
            binary = '0' + binary
        if dec_num >= 0:
            return '0' + binary
        else:
            return '1' + binary.zfill(self.MAX_BITS)

    def transfered_num_for_additional(self, bin_string):
        bin_list = list(bin_string)
        transfer = 1
        for i in range(len(bin_list) - 1, -1, -1):
            if transfer == 0:
                break
            if bin_list[i] == '0':
                bin_list[i] = '1'
                transfer = 0
            else:
                bin_list[i] = '0'
        if transfer:
            bin_list.insert(0, '1')
        return ''.join(bin_list)

    def convert_to_10(self, binary: str) -> int:

        sign = -1 if binary[0] == '1' else 1
        bits = binary[1:] if len(binary) > 1 else binary

        if sign == -1:
            bits = ''.join('1' if b == '0' else '0' for b in bits)
            value = 0
            for i, bit in enumerate(bits):
                if bit == '1':
                    value += 2 ** (len(bits) - i - 1)
            return -1 * (value + 1)

        return sum(
            int(bit) * 2 ** (len(bits) - i - 1)
            for i, bit in enumerate(bits))

    def direct_sum(self, num1, num2):
        bin1 = self.binary_number(num1).zfill(self.TOTAL_BITS)
        bin2 = self.binary_number(num2).zfill(self.TOTAL_BITS)
        result = []
        carry = 0
        for i in range(self.MAX_BITS, -1, -1):
            sum_bit = int(bin1[i]) + int(bin2[i]) + carry
            result.append(str(sum_bit % 2))
            carry = sum_bit // 2
        result = ''.join(reversed(result))
        return result[-self.TOTAL_BITS:]

    def convert_to_reverse_binary(self, dec_num):
        if dec_num >= 0:
            return self.binary_number(dec_num)
        positive = self.binary_number(abs(dec_num))
        inverted = ''.join('1' if b == '0' else '0' for b in positive[1:])
        return '1' + inverted

    def convert_to_additional_binary(self, dec_num):
        if dec_num >= 0:
            return self.convert_to_reverse_binary(dec_num)
        else:
            binary_number = self.convert_to_reverse_binary(dec_num)
            binary_number = self.transfered_num_for_additional(binary_number)
            return binary_number

    def additional_sum(self, num1, num2):
        bin1 = self.convert_to_additional_binary(num1).zfill(self.TOTAL_BITS)
        bin2 = self.convert_to_additional_binary(num2).zfill(self.TOTAL_BITS)

        temp_transfer = 0
        result = []
        for i in range(self.MAX_BITS, -1, -1):
            total = int(bin1[i]) + int(bin2[i]) + temp_transfer
            result.append(str(total % 2))
            temp_transfer = total // 2

        result = ''.join(reversed(result))
        return result[-self.TOTAL_BITS:]

    def additional_subtract(self, number1, number2):
        bin1 = self.convert_to_additional_binary(number1).zfill(self.TOTAL_BITS)
        bin2 = self.convert_to_additional_binary(-number2).zfill(self.TOTAL_BITS)
        carry = 0
        result = []
        for i in range(self.MAX_BITS, -1, -1):
            total = int(bin1[i]) + int(bin2[i]) + carry
            result.append(str(total % 2))
            carry = total // 2
        result = ''.join(reversed(result))
        return result[-self.TOTAL_BITS:]

    def direct_code_to_int(self, bin_str: str) -> int:
        sign = -1 if bin_str[0] == '1' else 1
        magnitude = int(bin_str[1:], 2)
        return sign * magnitude

    def direct_code_multiplication(self, num1, num2):
        if (num1 < 0 and num2 > 0) or (num1 > 0 and num2 < 0):
            result_sign = 1
        else:
            result_sign = 0

        abs_num1 = abs(num1)
        abs_num2 = abs(num2)

        bin_num1 = self.binary_number(abs_num1).zfill(self.TOTAL_BITS)[1:]
        bin_num2 = self.binary_number(abs_num2).zfill(self.TOTAL_BITS)[1:]

        product = [0] * (self.TOTAL_BITS * 2)

        for i in range(len(bin_num2) - 1, -1, -1):
            if bin_num2[i] == '1':
                carry = 0
                for j in range(len(bin_num1) - 1, -1, -1):
                    idx = i + j + 1
                    total = int(bin_num1[j]) + product[idx] + carry
                    product[idx] = total % 2
                    carry = total // 2
                product[i] += carry

        product_str = ''.join(str(bit) for bit in product)[-self.TOTAL_BITS:]

        if product_str.endswith('00'):
            product_str = product_str[:-2]

        result_bin = str(result_sign) + product_str
        result_dec = self.direct_code_to_int(result_bin)
        return f"Результат в прямом коде: [{result_bin}]  Десятичный результат: {result_dec}"

    def divide_bin(self, dividend_dec, divisor_dec):

            if divisor_dec == 0:
                raise ValueError("Делить на ноль нельзя.")
            if (dividend_dec < 0) and (divisor_dec >= 0):
                result_sign_bit = '1'
            elif (dividend_dec >= 0) and (divisor_dec < 0):
                result_sign_bit = '1'
            else:
                result_sign_bit = '0'

            dividend_abs = abs(dividend_dec)
            divisor_abs = abs(divisor_dec)

            dividend_bin = bin(dividend_abs)[2:]
            divisor_bin = bin(divisor_abs)[2:]
            quotient_bin = ''
            current_remainder = ''

            for bit in dividend_bin:
                current_remainder += bit
                current_remainder = current_remainder.lstrip('0') or '0'
                if len(current_remainder) > len(divisor_bin) or (
                        len(current_remainder) == len(divisor_bin) and int(current_remainder, 2) >= int(divisor_bin, 2)
                ):
                    current_remainder = bin(int(current_remainder, 2) - int(divisor_bin, 2))[2:]
                    quotient_bin += '1'
                else:
                    quotient_bin += '0'

            quotient_bin = quotient_bin.lstrip('0') or '0'

            fractional_part_bin = ''
            for _ in range(self.MANTISSA_BITS - 10):
                current_remainder += '0'
                current_remainder = current_remainder.lstrip('0') or '0'
                if len(current_remainder) > len(divisor_bin) or (
                        len(current_remainder) == len(divisor_bin) and int(current_remainder, 2) >= int(divisor_bin, 2)
                ):
                    current_remainder = bin(int(current_remainder, 2) - int(divisor_bin, 2))[2:]
                    fractional_part_bin += '1'
                else:
                    fractional_part_bin += '0'
                if current_remainder == '0':
                    break

            if quotient_bin != '0' :
                quotient_decimal = int(quotient_bin, 2)
            else :
                quotient_decimal = 0

            fractional_decimal = 0

            for i, bit in enumerate(fractional_part_bin):
                if bit == '1':
                    fractional_decimal += 1 / (2 ** (i + 1))

            decimal_result = quotient_decimal + fractional_decimal
            if result_sign_bit == '1':
                decimal_result = -decimal_result

            decimal_result = round(decimal_result, 5)

            binary_result_str = f"{result_sign_bit} {quotient_bin}.{fractional_part_bin}"
            return f"Результат в прямом коде: [{binary_result_str}]  Десятичный результат: {decimal_result}"
