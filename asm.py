from ctypes.wintypes import POINT
import mmap
import ctypes
from ctypes import c_int, POINTER


class Asm:
    def __init__(self, ret_type, *arg_types):
        self.codebuf = mmap.mmap(-1, mmap.PAGESIZE, prot=mmap.PROT_READ |
                                 mmap.PROT_WRITE | mmap.PROT_EXEC)
        self.ftype = ctypes.CFUNCTYPE(ret_type, *arg_types)
        self.fptr = ctypes.c_void_p.from_buffer(
            self.codebuf)
        self.f = self.ftype(ctypes.addressof(self.fptr))

    def cleanup(self):
        del self.fptr
        self.codebuf.close()

    def write_fun(self, content: str):
        encoded = bytes(
            content, encoding="raw_unicode_escape")
        self.codebuf.write(encoded)

    def __call__(self, *args):
        return self.f(*args)
    
    # following methods convert python array to ctypes array
    @staticmethod
    def convert_array(basic_type, pyarray):
        tmpty = basic_type * len(pyarray)
        return tmpty(*pyarray)
    
    @staticmethod
    def convert_int_array(pyarray):
        return Asm.convert_array(c_int, pyarray)

# some commonly used functions and their python wrapper
class Asmfun:
    def __getitem__(self, index):
        if index == "sum":
            # sum_arr(int *arr, int size)
            # simple sum over the entire array, but uses SIMD :)
            _sum_arr = Asm(c_int, POINTER(c_int), c_int)
            _sum_arr.write_fun("\x85\xF6\x7E\x0D\x89\xF1\x83\xFE\x08\x73\x09\x31\xD2\x31\xC0\xEB\x56\x31\xC0\xC3\x89\xCA\x83\xE2\xF8\x89\xC8\xC1\xE8\x03\x48\xC1\xE0\x05\x66\x0F\xEF\xC0\x31\xF6\x66\x0F\xEF\xC9\xF3\x0F\x6F\x14\x37\x66\x0F\xFE\xC2\xF3\x0F\x6F\x54\x37\x10\x66\x0F\xFE\xCA\x48\x83\xC6\x20\x48\x39\xF0\x75\xE4\x66\x0F\xFE\xC8\x66\x0F\x70\xC1\xEE\x66\x0F\xFE\xC1\x66\x0F\x70\xC8\x55\x66\x0F\xFE\xC8\x66\x0F\x7E\xC8\x48\x39\xCA\x74\x0B\x03\x04\x97\x48\xFF\xC2\x48\x39\xD1\x75\xF5\xC3")
            sum_arr = lambda a: _sum_arr(a, len(a))
            return sum_arr
        elif index == "binsearch":
            # bin_search(int *arr, int size, target)
            # finds the first occurance of an int, returns the index, -1 if not found
            _bin_search = Asm(c_int, POINTER(c_int), c_int, c_int)
            _bin_search.write_fun("\x85\xF6\x7E\x45\xFF\xCE\x41\xB8\xFF\xFF\xFF\xFF\x31\xC9\xEB\x0A\x8D\x70\xFF\x41\x89\xC0\x39\xF1\x7F\x2E\x44\x8D\x0C\x31\x44\x89\xC8\xC1\xE8\x1F\x44\x01\xC8\xD1\xF8\x4C\x63\xC8\x42\x39\x14\x8F\x74\xDE\x7D\x06\x89\xC1\xFF\xC1\xEB\x04\xFF\xC8\x89\xC6\x44\x89\xC0\x41\x89\xC0\x39\xF1\x7E\xD2\xC3\xB8\xFF\xFF\xFF\xFF\xC3")
            bin_search = lambda a, t : _bin_search(a, len(a), t)
            return bin_search


if __name__ == "__main__":
    af = Asmfun()
    a = Asm.convert_int_array([1,3,5,6,10,11,12])
    print(af["binsearch"](a, 5))
    
