# distutils: language = c++
# cython: language_level = 3

from aimos._core.storage.arrayview cimport ArrayView
from aimos._core.storage.treeview cimport TreeView

cdef class TreeArrayView(ArrayView):
    cdef:
        public TreeView tree
        public object dtype
