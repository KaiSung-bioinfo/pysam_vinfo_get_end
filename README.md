# pysam_vinfo_get_end

A simple Cython module to retrieve the 'END' value from the INFO field of a VCF record when using `pysam`.

This could be useful for structural variation VCFs where `record.stop` may not directly correspond to the INFO/END tag.

## Dependencies

This module requires the following Python packages:
- `pysam`
- `cython` (for building from source)
- `pyximport` (if you want to import the module on-the-fly)

## Installation

 1. Install using pip:

    ```bash
    git clone https://github.com/KaiSung-bioinfo/pysam_vinfo_get_end.git
    cd pysam_vinfo_get_end
    pip install .
    ```

2. Import on-the-fly using the pyximport module:
    
    **Note:** You should have pysam_vinfo_get_end.pyx and pysam_vinfo_get_end.pyxbld in current home directory
    ```python
    import pyximport
    pyximport.install()
    from pysam_vinfo_get_end import vinfo_get_end
    ```

## Usage

```python
import pysam
from pysam_vinfo_get_end import vinfo_get_end

# Assuming you have a VCF file
vcf = pysam.VariantFile("your_structural_variants.vcf")

# Get the first
record = next(vcf)

# pysam does not allow direct access to the INFO/END
# This will result in KeyError: 'END is a reserved attribute; access is via record.stop'
try:
    print(record.info["END"])
except Exception as e:
    print(e)

# Use the function to get the raw END value
end_pos = vinfo_get_end(record)
if end_pos is not None:
    print(f"Variant at {record.chrom}:{record.pos} has END={end_pos}")
else:
    print(f"Variant at {record.chrom}:{record.pos} has no END in INFO field")
