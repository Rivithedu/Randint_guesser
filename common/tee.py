import sys
from warnings import deprecated

class Tee:
    # @deprecated('Use Tee instead')

    def __init__(self, f1, f2):
        self.f1, self.f2 = f1, f2
    def write(self, buf):
        try:
            self.f1.write(buf)
            self.f2.write(buf)
        except ValueError:
            print("write error")

    def flush(self):
        try:
            self.f1.flush()
            self.f2.flush()
        except ValueError:
            print("flush error")

    def getvalue(self):
        return self.f1.sys.getvalue()



# class Tee:
#     def __init__(self, f1, f2):
#         self.f1, self.f2 = f1, f2
#
#     def write(self, buf):
#         # Write to f1 if it is not closed
#         if not self._is_closed(self.f1):
#             self.f1.write(buf)
#         # Write to f2 if it is not closed
#         if not self._is_closed(self.f2):
#             self.f2.write(buf)
#
#     def flush(self):
#         # Flush f1 if it is not closed
#         if not self._is_closed(self.f1):
#             self.f1.flush()
#         # Flush f2 if it is not closed
#         if not self._is_closed(self.f2):
#             self.f2.flush()
#
#     def close(self):
#         # Close files safely to ensure resource management
#         if not self._is_closed(self.f1):
#             self.f1.close()
#         if not self._is_closed(self.f2):
#             self.f2.close()
#
#     @staticmethod
#     def _is_closed(file_obj):
#         try:
#             # Check if the file object is closed by checking its 'closed' attribute
#             return file_obj.closed
#         except AttributeError:
#             # For non-standard file-like objects, assume they are not closed
#             return False
