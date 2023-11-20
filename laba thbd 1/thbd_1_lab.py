import struct
import time




class Serializer:

    def encode(self, to_encode, out = b''):

        int_ = 1
        bool_ = 2
        str_ = 3
        float_ = 4
        list_ = 5
        dict_ = 6
        if isinstance(to_encode, int) and isinstance(to_encode, bool) == False:
            out += int_.to_bytes(1, byteorder ='big') + to_encode.to_bytes(4, byteorder ='big')

        if isinstance(to_encode, bool):
            out += bool_.to_bytes(1, byteorder ='big') + to_encode.to_bytes(4, byteorder ='big')

        if isinstance(to_encode, str):
            out += str_.to_bytes(1, byteorder ='big') + len(to_encode).to_bytes(4, byteorder ='big') + bytes(to_encode, 'utf-8')

        if isinstance(to_encode, float):
            out += float_.to_bytes(1, byteorder ='big') + struct.pack('d', to_encode)

        if isinstance(to_encode, list):
            out += list_.to_bytes(1, byteorder ='big') + len(to_encode).to_bytes(4, byteorder ='big')
            for i in to_encode:
                out += self.encode(i)

        if isinstance(to_encode, dict):
            out += dict_.to_bytes(1, byteorder='big') + len(to_encode.keys()).to_bytes(4, byteorder ='big')
            for i in to_encode.keys():
                out += self.encode(i)
            for i in to_encode.values():
                out += self.encode(i)
        return out

    def decode_sost(self, to_decode, bytes_):
        if to_decode[0] == 3:
            len_str = int.from_bytes(to_decode[1:5], 'big')
            res = self.decode(to_decode[:5 + len_str])[0]
            to_decode = to_decode[5 + len_str:]
            bytes_ += 5 + len_str

        elif to_decode[0] == 4:
            res = self.decode(to_decode[0:9])[0]
            to_decode = to_decode[9:]
            bytes_ += 9

        elif to_decode[0] == 1 or to_decode[0] == 2:
            res = self.decode(to_decode[0:5])[0]
            to_decode = to_decode[5:]
            bytes_ += 5

        elif to_decode[0] == 5:
            res = self.decode(to_decode)[0]
            to_decode = to_decode[self.decode(to_decode)[1]:]

        elif to_decode[0] == 6:
            res = self.decode(to_decode)[0]
            to_decode = to_decode[self.decode(to_decode)[1]:]
        return to_decode, res, bytes_

    def decode(self, to_decode):
        bytes_ = 5
        encode_type = to_decode[0]
        out = b''
        if encode_type == 1: #int
            out = int.from_bytes(to_decode[1:], 'big')

        if encode_type == 2: #bool
            out = to_decode[4]
            if out == 1:
                out = True
            else:
                out = False

        if encode_type == 3: #str
            out = to_decode[5:].decode('utf-8')

        if encode_type == 4: #float
            out = struct.unpack('d', to_decode[1:])[0]

        if encode_type == 5: #list
            to_decode = to_decode[1:]
            len_mas = int.from_bytes(to_decode[0:4], 'big')
            i = 0
            mas = []
            to_decode = to_decode[4:]
            while i < len_mas:
                i += 1
                to_decode, res, bytes_ = self.decode_sost(to_decode, bytes_)
                mas.append(res)
            out = mas

        if encode_type == 6: #dict
            to_decode = to_decode[1:]
            len_dict = int.from_bytes(to_decode[0:4], 'big') * 2
            i = 0
            mas = []
            to_decode = to_decode[4:]
            while i < len_dict:
                i += 1
                to_decode, res, bytes_ = self.decode_sost(to_decode, bytes_)
                mas.append(res)

            keys = mas[:int(len_dict/2)]
            values = mas[int(len_dict/2):]
            out = dict(zip(keys, values))
        return out, bytes_


a = Serializer()
dict_file = {"name": '123', "favorite_number": 321, 'favorite_color': 'red'}
b = a.encode(dict_file)
print(b)
print(Serializer().decode(b)[0])


# with open('out.txt','w') as out:
#     for key,val in dict_file.items():
#         out.write('{}:{}\n'.format(key,val))
#
# with open('binary.txt','wb') as bin:
#         bin.write(b)