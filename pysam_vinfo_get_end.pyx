# cython: language_level=3
from libc.stdlib cimport malloc, free
from libc.stdint cimport int64_t
from pysam.libchtslib cimport *
from pysam.libcbcf cimport *


def vinfo_get_end(VariantRecord record) -> int|None:
    """
    Retrieves the raw 'END' integer value directly from the INFO field of a pysam.VariantRecord.

    This function uses the low-level HTSlib API to extract the 'END' tag.
    Could be useful when direct access to the 'END' INFO tag is required,
    as standard `pysam.VariantRecord` properties (e.g., `record.stop`) might
    derive the end position differently for some VCFs of structural variation.

    Parameters
    ----------
    record : pysam.VariantRecord
        The variant record from which to retrieve the 'END' information.

    Returns
    -------
    int or None
        The integer value of the 'END' tag if found and successfully parsed,
        otherwise None if the tag is not present or cannot be parsed as an integer.
    """
    cdef int v = -1, cap = 1
    cdef int64_t *dst = <int64_t*> malloc(cap)
    if dst == NULL:
        raise RuntimeError("Failed to allocate memory!")
    end_pos = 0
    v = bcf_get_info_values(record.header.ptr, record.ptr, b'END',
                            <void **> &dst, &cap,
                            (BCF_HT_INT | 0x100)) #define BCF_HT_LONG (BCF_HT_INT | 0x100) // BCF_HT_INT, but for int64_t values; VCF only!
    if v >= 0:
        end_pos = dst[0]
    else:
        end_pos = None
    if dst != NULL:
        free(dst)
    return end_pos
